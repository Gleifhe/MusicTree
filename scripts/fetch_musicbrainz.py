#!/usr/bin/env python3
"""
MusicBrainz Fetch Script for MusicTree
=======================================
Fetches Alternative Rock artists from MusicBrainz and generates Hugo content files.

Usage:
    python scripts/fetch_musicbrainz.py [options]

Options:
    --artists N       Number of artists to fetch (default: 10)
    --recordings N    Max recordings per artist (default: 5)
    --output PATH     Hugo content root (default: content/)
    --append          Append to existing graph.json instead of overwriting

Requirements:
    pip install musicbrainzngs pyyaml

MusicBrainz API rate limit: 1 request/second for anonymous users.
Register a free account and set USER_AGENT below to increase the limit.
"""

import os
import re
import sys
import json
import time
import argparse
import unicodedata
from pathlib import Path

try:
    import musicbrainzngs as mb
except ImportError:
    print("ERROR: musicbrainzngs not installed. Run: pip install musicbrainzngs")
    sys.exit(1)

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)

# ── Configuration ────────────────────────────────────────────────────────────

APP_NAME    = "MusicTreeHugo"
APP_VERSION = "1.0"
APP_CONTACT = "musictree@example.com"  # Change to your email

CONTENT_ROOT = Path("content")
DATA_ROOT    = Path("data")

RELATION_TYPE_MAP = {
    "member of band":   "member-of",
    "producer":         "produced-by",
    "lyricist":         "written-by",
    "composer":         "written-by",
    "performer":        "performed-by",
    "lead vocals":      "performed-by",
    "vocals":           "performed-by",
    "drums":            "played",
    "bass guitar":      "played",
    "guitar":           "played",
    "keyboards":        "played",
    "piano":            "played",
}

ROLE_LABEL_MAP = {
    "member of band":   "Member",
    "producer":         "Producer",
    "lyricist":         "Lyricist",
    "composer":         "Composer",
    "lead vocals":      "Lead Vocals",
    "vocals":           "Vocals",
    "drums":            "Drums",
    "bass guitar":      "Bass",
    "guitar":           "Guitar",
    "keyboards":        "Keyboards",
    "piano":            "Piano",
    "mix":              "Mixer",
    "engineer":         "Engineer",
    "recording":        "Engineer",
    "mastering":        "Mastering",
}

# ── Helpers ──────────────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    """Convert text to a URL-safe slug."""
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text).strip("-")
    return text


def write_frontmatter(path: Path, data: dict, body: str = "") -> None:
    """Write a Hugo markdown file with YAML front matter."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        print(f"  [skip] {path} already exists")
        return
    with open(path, "w", encoding="utf-8") as f:
        f.write("---\n")
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        f.write("---\n")
        if body:
            f.write("\n" + body + "\n")
    print(f"  [write] {path}")


def api_get(func, *args, **kwargs):
    """Call a MusicBrainz API function with rate limiting."""
    time.sleep(1.1)
    try:
        return func(*args, **kwargs)
    except mb.ResponseError as e:
        print(f"  [warn] API error: {e}")
        return None
    except Exception as e:
        print(f"  [warn] Unexpected error: {e}")
        return None


# ── Graph data accumulators ──────────────────────────────────────────────────

graph_nodes: dict[str, dict] = {}
graph_links: list[dict] = []


def add_node(node_id: str, label: str, node_type: str, url: str, meta: str = "") -> None:
    if node_id not in graph_nodes:
        graph_nodes[node_id] = {
            "id":    node_id,
            "label": label,
            "type":  node_type,
            "url":   url,
            "meta":  meta,
        }


def add_link(source: str, target: str, relation: str) -> None:
    key = f"{source}|{target}|{relation}"
    if not any(
        l["source"] == source and l["target"] == target and l["relation"] == relation
        for l in graph_links
    ):
        graph_links.append({"source": source, "target": target, "relation": relation})


# ── Fetch functions ──────────────────────────────────────────────────────────

def fetch_artist_details(artist_id: str, artist_slug: str) -> dict | None:
    """Fetch full artist info including members and releases."""
    print(f"  Fetching artist details: {artist_slug} ({artist_id})")
    result = api_get(
        mb.get_artist_by_id,
        artist_id,
        includes=["artist-rels", "release-groups"],
    )
    if not result:
        return None
    return result.get("artist")


def process_artist(artist_data: dict, max_recordings: int) -> None:
    """Process a single artist and write Hugo content."""
    name  = artist_data.get("name", "Unknown")
    mbid  = artist_data.get("id", "")
    slug  = slugify(name)
    atype = artist_data.get("type", "Group")
    country = artist_data.get("area", {}).get("name", "") if artist_data.get("area") else ""

    tags = [t["name"] for t in artist_data.get("tag-list", [])]
    genres = [t for t in tags if t in (
        "alternative rock", "grunge", "indie rock", "post-punk", "art rock",
        "noise rock", "dream pop", "shoegaze", "britpop", "college rock"
    )][:4]
    if not genres:
        genres = ["alternative rock"]

    formed = ""
    if artist_data.get("life-span", {}).get("begin"):
        formed = artist_data["life-span"]["begin"][:4]

    print(f"\nProcessing artist: {name} ({slug})")

    add_node(slug, name, "artist", f"/artists/{slug}/",
             f"{', '.join(genres)} · {formed or '?'}")

    # Members from artist relationships
    members = []
    for rel in artist_data.get("artist-relation-list", []):
        rel_type = rel.get("type", "").lower()
        direction = rel.get("direction", "")
        person = rel.get("artist", {})

        if rel_type == "member of band" and direction == "backward":
            pname = person.get("name", "")
            pslug = slugify(pname)
            pmbid = person.get("id", "")
            attrs = rel.get("attribute-list", [])
            role_label = ", ".join(ROLE_LABEL_MAP.get(a.lower(), a.title()) for a in attrs) if attrs else "Member"

            if pname:
                members.append({"slug": pslug, "name": pname, "role": role_label})
                add_node(pslug, pname, "person", f"/people/{pslug}/", role_label)
                add_link(pslug, slug, "member-of")
                write_frontmatter(
                    CONTENT_ROOT / "people" / f"{pslug}.md",
                    {
                        "title":       pname,
                        "mbid":        pmbid,
                        "roles":       [a.lower() for a in attrs] if attrs else [],
                        "nationality": "",
                        "born":        None,
                        "artist":      name,
                        "artist_slug": slug,
                        "credits":     [],
                        "draft":       False,
                    },
                )

    # Release groups (albums)
    albums_data = []
    rg_list = artist_data.get("release-group-list", [])[:5]
    for rg in rg_list:
        if rg.get("primary-type") not in ("Album", "Single", "EP"):
            continue
        rg_title = rg.get("title", "")
        rg_slug  = slugify(rg_title)
        rg_mbid  = rg.get("id", "")
        rg_year  = rg.get("first-release-date", "")[:4] if rg.get("first-release-date") else ""

        albums_data.append({"slug": rg_slug, "title": rg_title, "year": rg_year})
        add_node(rg_slug, rg_title, "album", f"/albums/{rg_slug}/",
                 f"{name} · {rg_year}")
        add_link(slug, rg_slug, "released")

        # Fetch recordings for this release group
        songs = fetch_release_group_recordings(rg_mbid, rg_slug, rg_title, slug, name, max_recordings)

        write_frontmatter(
            CONTENT_ROOT / "albums" / f"{rg_slug}.md",
            {
                "title":       rg_title,
                "mbid":        rg_mbid,
                "artist":      name,
                "artist_slug": slug,
                "year":        int(rg_year) if rg_year.isdigit() else None,
                "genres":      genres,
                "songs":       songs,
                "draft":       False,
            },
        )

    write_frontmatter(
        CONTENT_ROOT / "artists" / f"{slug}.md",
        {
            "title":     name,
            "mbid":      mbid,
            "country":   country,
            "formed":    int(formed) if formed and formed.isdigit() else None,
            "band_type": atype,
            "genres":    genres,
            "members":   members,
            "albums":    albums_data,
            "draft":     False,
        },
    )


def fetch_release_group_recordings(
    rg_id: str, album_slug: str, album_title: str,
    artist_slug: str, artist_name: str, max_recs: int
) -> list[dict]:
    """Fetch recordings from the first release of a release group."""
    print(f"    Fetching recordings for album: {album_title}")
    result = api_get(mb.get_release_group_by_id, rg_id, includes=["releases"])
    if not result:
        return []

    releases = result.get("release-group", {}).get("release-list", [])
    if not releases:
        return []

    release_id = releases[0].get("id")
    if not release_id:
        return []

    time.sleep(1.1)
    rel_result = api_get(
        mb.get_release_by_id,
        release_id,
        includes=["recordings", "recording-level-rels", "artist-credits"],
    )
    if not rel_result:
        return []

    songs = []
    medium_list = rel_result.get("release", {}).get("medium-list", [])
    for medium in medium_list:
        for track in medium.get("track-list", [])[:max_recs]:
            rec = track.get("recording", {})
            rec_title = rec.get("title", track.get("title", ""))
            rec_mbid  = rec.get("id", "")
            rec_slug  = slugify(rec_title)
            length_ms = rec.get("length")
            duration  = ms_to_duration(int(length_ms)) if length_ms else ""
            position  = track.get("position", track.get("number", ""))

            songs.append({"slug": rec_slug, "title": rec_title, "duration": duration})
            add_node(rec_slug, rec_title, "song", f"/songs/{rec_slug}/",
                     f"{artist_name} · {album_title}")
            add_link(rec_slug, album_slug, "appears-on")

            # Write song file
            write_frontmatter(
                CONTENT_ROOT / "songs" / f"{rec_slug}.md",
                {
                    "title":       rec_title,
                    "mbid":        rec_mbid,
                    "artist":      artist_name,
                    "artist_slug": artist_slug,
                    "album":       album_title,
                    "album_slug":  album_slug,
                    "year":        None,
                    "duration":    duration,
                    "credits":     [],
                    "draft":       False,
                },
            )

            if len(songs) >= max_recs:
                break
        if len(songs) >= max_recs:
            break

    return songs


def ms_to_duration(ms: int) -> str:
    """Convert milliseconds to M:SS format."""
    seconds = ms // 1000
    m, s = divmod(seconds, 60)
    return f"{m}:{s:02d}"


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Fetch Alternative Rock data from MusicBrainz")
    parser.add_argument("--artists",    type=int, default=10,       help="Number of artists to fetch")
    parser.add_argument("--recordings", type=int, default=5,        help="Max recordings per album")
    parser.add_argument("--output",     type=str, default="content", help="Hugo content root directory")
    parser.add_argument("--append",     action="store_true",         help="Append to existing graph.json")
    args = parser.parse_args()

    global CONTENT_ROOT, DATA_ROOT
    CONTENT_ROOT = Path(args.output)
    DATA_ROOT    = CONTENT_ROOT.parent / "data"

    mb.set_useragent(APP_NAME, APP_VERSION, APP_CONTACT)

    print("=" * 60)
    print("MusicTree — MusicBrainz Fetch Script")
    print("=" * 60)
    print(f"Target: {args.artists} Alt Rock artists, {args.recordings} recordings/album")
    print()

    # ── Load existing graph if appending ────────────────────────────────────
    graph_path = DATA_ROOT / "graph.json"
    if args.append and graph_path.exists():
        with open(graph_path, encoding="utf-8") as f:
            existing = json.load(f)
        for n in existing.get("nodes", []):
            graph_nodes[n["id"]] = n
        graph_links.extend(existing.get("links", []))
        print(f"Loaded {len(graph_nodes)} existing nodes, {len(graph_links)} links.")

    # ── Search for alt-rock artists ──────────────────────────────────────────
    print("Searching MusicBrainz for Alternative Rock artists...")
    search_result = api_get(
        mb.search_artists,
        tag="alternative rock",
        type="Group",
        limit=args.artists + 5,
    )

    if not search_result:
        print("ERROR: Failed to search MusicBrainz. Check your internet connection.")
        sys.exit(1)

    artist_list = search_result.get("artist-list", [])
    print(f"Found {len(artist_list)} artists. Processing top {args.artists}...\n")

    processed = 0
    for artist in artist_list:
        if processed >= args.artists:
            break

        artist_id = artist.get("id")
        artist_name = artist.get("name", "")
        if not artist_id or not artist_name:
            continue

        full_artist = fetch_artist_details(artist_id, slugify(artist_name))
        if not full_artist:
            continue

        process_artist(full_artist, args.recordings)
        processed += 1

    # ── Write graph.json ─────────────────────────────────────────────────────
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    graph_data = {
        "nodes": list(graph_nodes.values()),
        "links": graph_links,
    }
    with open(graph_path, "w", encoding="utf-8") as f:
        json.dump(graph_data, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"Done! Wrote {len(graph_nodes)} nodes and {len(graph_links)} links.")
    print(f"Graph data: {graph_path}")
    print(f"Content:    {CONTENT_ROOT}/")
    print(f"\nRun 'hugo server' to preview the site.")


if __name__ == "__main__":
    main()
