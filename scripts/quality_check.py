#!/usr/bin/env python3
"""
MusicTree Quality Check
Validates all content files for consistency and completeness.
Usage: python scripts/quality_check.py [--fix-scenes] [--verbose]
"""
import json, re, sys, argparse
from pathlib import Path
from collections import defaultdict

try:
    import yaml
except ImportError:
    print("pip install pyyaml"); sys.exit(1)

CONTENT = Path("content")
STATIC  = Path("static/data/graph.json")

PASS = "\033[92m✓\033[0m"
WARN = "\033[93m⚠\033[0m"
FAIL = "\033[91m✗\033[0m"

parser = argparse.ArgumentParser()
parser.add_argument("--verbose", action="store_true")
args = parser.parse_args()

issues   = []
warnings = []

def read_fm(path):
    text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except Exception as e:
        issues.append(f"YAML parse error in {path}: {e}")
        return {}

def load_all(section):
    result = {}
    for f in sorted((CONTENT / section).glob("*.md")):
        fm = read_fm(f)
        if fm.get("title"):
            result[f.stem] = fm
    return result

# ── Load everything ───────────────────────────────────────────────────────────
print("Loading content...")
artists = load_all("artists")
albums  = load_all("albums")
songs   = load_all("songs")
people  = load_all("people")

print(f"  {len(artists)} artists, {len(albums)} albums, {len(songs)} songs, {len(people)} people\n")

# ── 1. Artists: missing fields ────────────────────────────────────────────────
print("── 1. Artist completeness ──────────────────────────────────────────────")
for slug, fm in artists.items():
    if not fm.get("scene"):
        warnings.append(f"Artist {slug}: missing scene field")
    if fm.get("band_type","Group") == "Group" and not fm.get("members"):
        warnings.append(f"Artist {slug}: Group with no members listed")
    if not fm.get("albums"):
        warnings.append(f"Artist {slug}: no albums listed")
artist_issues = [w for w in warnings if w.startswith("Artist")]
print(f"  {PASS if not artist_issues else WARN} {len(artist_issues)} issues")
for w in artist_issues[:10]:
    print(f"    {WARN} {w}")
if len(artist_issues) > 10:
    print(f"    ... and {len(artist_issues)-10} more")

# ── 2. Albums: broken artist_slug, missing songs ──────────────────────────────
print("\n── 2. Album completeness ───────────────────────────────────────────────")
album_issues = []
for slug, fm in albums.items():
    aslug = fm.get("artist_slug","")
    if not aslug:
        album_issues.append(f"Album {slug}: missing artist_slug")
    elif aslug not in artists:
        album_issues.append(f"Album {slug}: artist_slug '{aslug}' has no artist file")
    track_list = fm.get("songs") or fm.get("tracks") or []
    if not track_list:
        album_issues.append(f"Album {slug}: no track listing (songs/tracks field empty)")
print(f"  {PASS if not album_issues else WARN} {len(album_issues)} issues")
for w in album_issues[:10]:
    print(f"    {WARN} {w}")
if len(album_issues) > 10:
    print(f"    ... and {len(album_issues)-10} more")
issues.extend(album_issues)

# ── 3. Songs: missing credits ─────────────────────────────────────────────────
print("\n── 3. Song credit completeness ─────────────────────────────────────────")
song_issues = []
for slug, fm in songs.items():
    has_credits = bool(
        fm.get("credits") or fm.get("writers") or
        fm.get("producers") or fm.get("players")
    )
    if not has_credits:
        song_issues.append(f"Song {slug}: no credits (writers/producers/players)")
    # Check artist_slug exists
    aslug = fm.get("artist_slug","")
    if aslug and aslug not in artists:
        song_issues.append(f"Song {slug}: artist_slug '{aslug}' has no artist file")
    # Check album_slug exists
    alslug = fm.get("album_slug","")
    if alslug and alslug not in albums:
        song_issues.append(f"Song {slug}: album_slug '{alslug}' has no album file")

no_credits_count = sum(1 for s, fm in songs.items() if not (fm.get("credits") or fm.get("writers") or fm.get("producers") or fm.get("players")))
print(f"  {PASS if no_credits_count == 0 else FAIL} {no_credits_count}/{len(songs)} songs missing all credits")
broken_refs = [x for x in song_issues if "has no" in x]
print(f"  {PASS if not broken_refs else WARN} {len(broken_refs)} broken slug references in songs")
for w in broken_refs[:5]:
    print(f"    {WARN} {w}")
issues.extend(song_issues)

# ── 4. People: missing bands / song_credits ───────────────────────────────────
print("\n── 4. People completeness ──────────────────────────────────────────────")
people_issues = []
for slug, fm in people.items():
    has_band = bool(fm.get("bands") or fm.get("artist_slug"))
    if not has_band:
        people_issues.append(f"Person {slug}: no bands association")
    has_credits = bool(fm.get("song_credits") or fm.get("credits"))
    if not has_credits:
        people_issues.append(f"Person {slug}: no song credits")
    # Check band slugs exist
    for b in fm.get("bands",[]) or []:
        if b.get("slug") and b["slug"] not in artists:
            people_issues.append(f"Person {slug}: band slug '{b['slug']}' has no artist file")

no_bands = sum(1 for _, fm in people.items() if not (fm.get("bands") or fm.get("artist_slug")))
no_sc    = sum(1 for _, fm in people.items() if not (fm.get("song_credits") or fm.get("credits")))
broken_bands = [x for x in people_issues if "band slug" in x]
print(f"  {PASS if no_bands == 0 else WARN} {no_bands}/{len(people)} people with no band")
print(f"  {PASS if no_sc == 0 else WARN} {no_sc}/{len(people)} people with no song credits")
print(f"  {PASS if not broken_bands else WARN} {len(broken_bands)} broken band slug refs")
for w in broken_bands[:5]:
    print(f"    {WARN} {w}")
issues.extend(people_issues)

# ── 5. Cross-reference: album tracks → song files ────────────────────────────
print("\n── 5. Album tracks → song file cross-references ────────────────────────")
missing_song_files = []
for slug, fm in albums.items():
    track_list = fm.get("songs") or fm.get("tracks") or []
    for t in track_list:
        tslug = t.get("slug","")
        if tslug and tslug not in songs:
            missing_song_files.append(f"Album {slug}: track '{tslug}' has no song file")
print(f"  {PASS if not missing_song_files else WARN} {len(missing_song_files)} track slugs with no matching song file")
for w in missing_song_files[:10]:
    print(f"    {WARN} {w}")
if len(missing_song_files) > 10:
    print(f"    ... and {len(missing_song_files)-10} more")
issues.extend(missing_song_files)

# ── 6. Cross-reference: person credits → song files ──────────────────────────
print("\n── 6. Person song_credits → song file cross-references ─────────────────")
missing_credit_files = []
for slug, fm in people.items():
    for c in fm.get("song_credits",[]) or []:
        cslug = c.get("slug","")
        if cslug and cslug not in songs:
            missing_credit_files.append(f"Person {slug}: credit slug '{cslug}' has no song file")
    for c in fm.get("credits",[]) or []:
        cslug = c.get("song_slug","")
        if cslug and cslug not in songs:
            missing_credit_files.append(f"Person {slug}: credit song_slug '{cslug}' has no song file")
print(f"  {PASS if not missing_credit_files else WARN} {len(missing_credit_files)} credit slugs with no matching song file")
for w in missing_credit_files[:5]:
    print(f"    {WARN} {w}")
issues.extend(missing_credit_files)

# ── 7. Graph connectivity ─────────────────────────────────────────────────────
print("\n── 7. Graph connectivity ───────────────────────────────────────────────")
if STATIC.exists():
    g = json.loads(STATIC.read_text(encoding="utf-8"))
    adj = defaultdict(set)
    for lnk in g["links"]:
        s = lnk["source"] if isinstance(lnk["source"],str) else lnk["source"]["id"]
        t = lnk["target"] if isinstance(lnk["target"],str) else lnk["target"]["id"]
        adj[s].add(t); adj[t].add(s)

    orphans = [n for n in g["nodes"] if len(adj[n["id"]]) == 0]
    low_conn = [n for n in g["nodes"] if 1 <= len(adj[n["id"]]) <= 2]

    # Find connected components
    visited = set()
    components = []
    id_to_node = {n["id"]: n for n in g["nodes"]}
    for n in g["nodes"]:
        if n["id"] not in visited:
            comp = []
            stack = [n["id"]]
            while stack:
                cur = stack.pop()
                if cur in visited: continue
                visited.add(cur)
                comp.append(cur)
                stack.extend(adj[cur] - visited)
            components.append(comp)
    components.sort(key=len, reverse=True)

    print(f"  {PASS if not orphans else FAIL} {len(orphans)} orphaned nodes (0 links)")
    for o in orphans[:5]:
        node = id_to_node.get(o["id"] if isinstance(o,dict) else o, {})
        print(f"    {FAIL} {o['id'] if isinstance(o,dict) else o} ({o.get('type','') if isinstance(o,dict) else ''})")
    print(f"  {WARN if len(low_conn)>20 else PASS} {len(low_conn)} nodes with only 1-2 connections")
    print(f"  {PASS if len(components)==1 else WARN} {len(components)} connected components")
    print(f"    Largest: {len(components[0])} nodes ({100*len(components[0])//len(g['nodes'])}% of total)")
    if len(components) > 1:
        print(f"    Smallest components: {[len(c) for c in components[-5:]]}")
    
    # Top 10 most connected
    by_links = sorted(g["nodes"], key=lambda n: len(adj[n["id"]]), reverse=True)
    print(f"\n  Top 10 most connected nodes:")
    for n in by_links[:10]:
        print(f"    {len(adj[n['id']]):4d} links  [{n['type']:6s}]  {n['label']}")
else:
    print(f"  {WARN} graph.json not found — run scripts/rebuild_graph.py first")

# ── 8. Scene coverage ─────────────────────────────────────────────────────────
print("\n── 8. Scene coverage ───────────────────────────────────────────────────")
scene_counts = defaultdict(list)
for slug, fm in artists.items():
    sc = fm.get("scene","")
    scene_counts[sc].append(slug)
missing_scene = scene_counts.get("", [])
print(f"  {PASS if not missing_scene else WARN} {len(missing_scene)} artists missing scene field")
for s in missing_scene[:5]:
    print(f"    {WARN} {s}")
print(f"  Scene distribution:")
for sc, slugs in sorted(scene_counts.items(), key=lambda x: -len(x[1])):
    if sc:
        flag = PASS if len(slugs) >= 3 else WARN
        print(f"    {flag} {sc:<25} {len(slugs)} artists")

# ── 9. Duplicate detection ────────────────────────────────────────────────────
print("\n── 9. Duplicate detection ──────────────────────────────────────────────")
# O(n) dict-based grouping — avoids nested loops over all songs
title_map = {}
for slug, fm in songs.items():
    title = fm.get('title', '').lower().strip()
    if not title:
        continue
    if title not in title_map:
        title_map[title] = []
    title_map[title].append(slug)

duplicates = {t: slugs for t, slugs in title_map.items() if len(slugs) > 1}
print(f"  {PASS if not duplicates else WARN} {len(duplicates)} duplicate song titles (any artist)")
for title, slugs in list(duplicates.items())[:5]:
    print(f"    {WARN} '{title}': {slugs}")

# ── Summary ───────────────────────────────────────────────────────────────────
total_issues = len([x for x in issues if "missing artist_slug" in x or "has no artist file" in x or "has no album file" in x or "has no song file" in x])
print(f"\n{'═'*70}")
print(f"SUMMARY: {len(songs)} songs ({no_credits_count} missing credits), {len(albums)} albums, {len(artists)} artists, {len(people)} people")
print(f"  {FAIL if no_credits_count > 0 else PASS} Songs missing all credits: {no_credits_count}")
print(f"  {FAIL if missing_song_files else PASS} Broken track→song refs:    {len(missing_song_files)}")
print(f"  {WARN if no_bands > 0 else PASS} People without bands:      {no_bands}")
print(f"  {WARN if missing_scene else PASS} Artists without scene:     {len(missing_scene)}")
print(f"  {WARN if duplicates else PASS} Duplicate song titles:     {len(duplicates)}")
print(f"{'═'*70}")
print("\nRun 'python scripts/rebuild_graph.py' after fixing content to update the graph.")
