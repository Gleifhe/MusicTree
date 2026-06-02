#!/usr/bin/env python3
"""Rebuild data/graph.json from Hugo content files."""
import json, re, sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("pip install pyyaml"); sys.exit(1)

CONTENT = Path("content")
DATA    = Path("data")

nodes = {}
links = []
seen_links = set()

def slugify(s):
    s = re.sub(r"[^\w\s-]", "", s.lower())
    return re.sub(r"[\s_]+", "-", s).strip("-")

def add_node(nid, label, ntype, url, meta="", scene=""):
    if nid not in nodes:
        nodes[nid] = {"id": nid, "label": label, "type": ntype, "url": url, "meta": meta, "scene": scene}

def add_link(src, tgt, rel):
    key = f"{src}|{tgt}|{rel}"
    if key not in seen_links:
        seen_links.add(key)
        links.append({"source": src, "target": tgt, "relation": rel})

def read_fm(path):
    # utf-8-sig strips UTF-8 BOM if present; normalize line endings
    text = path.read_text(encoding="utf-8-sig").replace('\r\n', '\n').replace('\r', '\n')
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except Exception:
        return {}

# ── Artists ──────────────────────────────────────────────────────────────────
for f in sorted((CONTENT / "artists").glob("*.md")):
    fm = read_fm(f)
    if not fm.get("title"):
        continue
    slug = f.stem
    scene  = fm.get("scene", "")
    genres = fm.get("genres", [])
    formed = fm.get("formed", "")
    meta = f"{', '.join(genres[:2])}{' · ' + str(formed) if formed else ''}"
    add_node(slug, fm["title"], "artist", f"/artists/{slug}/", meta, scene)

    for m in fm.get("members", []) or []:
        if m.get("slug"):
            add_link(m["slug"], slug, "member-of")

    for a in fm.get("albums", []) or []:
        if a.get("slug"):
            add_link(slug, a["slug"], "released")

# ── People ────────────────────────────────────────────────────────────────────
for f in sorted((CONTENT / "people").glob("*.md")):
    fm = read_fm(f)
    if not fm.get("title"):
        continue
    slug = f.stem
    roles = fm.get("roles", [])
    meta = ", ".join(r.title() for r in roles[:3])
    add_node(slug, fm["title"], "person", f"/people/{slug}/", meta)

    # bands field (multi-band people like Pat Smear)
    for b in fm.get("bands", []) or []:
        if b.get("slug"):
            add_link(slug, b["slug"], "member-of")

    # single artist_slug
    if fm.get("artist_slug"):
        add_link(slug, fm["artist_slug"], "member-of")

    # credits → songs and albums (old format: credits:[{song_slug, role}])
    for c in fm.get("credits", []) or []:
        rel = "produced-by" if "producer" in (c.get("role", "").lower()) else \
              "written-by"   if any(w in c.get("role","").lower() for w in ["songwriter","lyricist","composer","writer"]) else \
              "performed-by"
        if c.get("song_slug"):
            add_link(slug, c["song_slug"], rel)
        elif c.get("album_slug"):
            add_link(slug, c["album_slug"], rel)

    # new format: song_credits:[{slug, title, credit}]
    for c in fm.get("song_credits", []) or []:
        credit_lc = c.get("credit", "").lower()
        rel = "produced-by" if "producer" in credit_lc else \
              "written-by"  if any(w in credit_lc for w in ["writer","songwriter","wrote","lyricist","composer"]) else \
              "performed-by"
        if c.get("slug"):
            add_link(slug, c["slug"], rel)

# ── Albums ────────────────────────────────────────────────────────────────────
for f in sorted((CONTENT / "albums").glob("*.md")):
    fm = read_fm(f)
    if not fm.get("title"):
        continue
    slug = f.stem
    artist = fm.get("artist", "")
    year   = fm.get("year", "")
    add_node(slug, fm["title"], "album", f"/albums/{slug}/",
             f"{artist}{' · ' + str(year) if year else ''}")

    # Support both `songs:` (new format) and `tracks:` (old format)
    track_list = fm.get("songs", []) or fm.get("tracks", []) or []
    for s in track_list:
        if s.get("slug"):
            add_link(s["slug"], slug, "appears-on")

# ── Songs ─────────────────────────────────────────────────────────────────────
for f in sorted((CONTENT / "songs").glob("*.md")):
    fm = read_fm(f)
    if not fm.get("title"):
        continue
    slug = f.stem
    artist = fm.get("artist", "")
    album  = fm.get("album", "")
    add_node(slug, fm["title"], "song", f"/songs/{slug}/",
             f"{artist}{' · ' + album if album else ''}")

    # Format A: flat credits list [{person_slug, role}]
    for c in fm.get("credits", []) or []:
        if not c.get("person_slug"):
            continue
        role_lc = c.get("role", "").lower()
        if "producer" in role_lc:
            rel = "produced-by"
        elif any(w in role_lc for w in ["songwriter","lyricist","composer","writer"]):
            rel = "written-by"
        elif any(w in role_lc for w in ["drums","bass","guitar","piano","keyboards","keys","violin","trumpet","percussion"]):
            rel = "played"
        else:
            rel = "performed-by"
        add_link(c["person_slug"], slug, rel)

    # Format B: structured writers/producers/players lists [{slug, name}] or [{slug, name, instrument}]
    for w in fm.get("writers", []) or []:
        if w.get("slug"):
            add_link(w["slug"], slug, "written-by")
    for p in fm.get("producers", []) or []:
        if p.get("slug"):
            add_link(p["slug"], slug, "produced-by")
    for p in fm.get("players", []) or []:
        if p.get("slug"):
            add_link(p["slug"], slug, "played")

# ── Ensure artist → album links exist even if not in artist fm ───────────────
for f in sorted((CONTENT / "albums").glob("*.md")):
    fm = read_fm(f)
    aslug = fm.get("artist_slug", "")
    if aslug and f.stem:
        add_link(aslug, f.stem, "released")

# ── Write ─────────────────────────────────────────────────────────────────────
DATA.mkdir(exist_ok=True)
out = {"nodes": list(nodes.values()), "links": links}
graph_json = json.dumps(out, indent=2, ensure_ascii=False)
(DATA / "graph.json").write_text(graph_json, encoding="utf-8")
# Also copy to static/data/ so mini-graph.js can fetch it without inline injection
static_data = Path("static") / "data"
static_data.mkdir(parents=True, exist_ok=True)
(static_data / "graph.json").write_text(graph_json, encoding="utf-8")
print(f"graph.json: {len(nodes)} nodes, {len(links)} links")

# ── Slim graph (no songs) for homepage ────────────────────────────────────────
slim_node_ids = {nid for nid, n in nodes.items() if n["type"] != "song"}
slim_nodes = [n for n in nodes.values() if n["type"] != "song"]
slim_links = [
    l for l in links
    if l["source"] in slim_node_ids and l["target"] in slim_node_ids
]
slim_out = {"nodes": slim_nodes, "links": slim_links}
slim_json = json.dumps(slim_out, indent=2, ensure_ascii=False)
(static_data / "graph-slim.json").write_text(slim_json, encoding="utf-8")
print(f"graph-slim.json: {len(slim_nodes)} nodes, {len(slim_links)} links (songs excluded)")
