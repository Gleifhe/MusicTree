# 🎵 MusicTree

A Hugo-based music family tree that visualizes the connections between musicians, bands, albums, and songs as interactive force-directed graphs. Trace how every drummer, producer, and songwriter is linked across the music world.

![Graph preview — artists, people, albums, and songs as interconnected nodes]

## Live Preview

Run locally:
```bash
hugo server
```
Then open [http://localhost:1313](http://localhost:1313)

---

## What It Does

- **Interactive homepage graph** — every artist, person, album, and song rendered as a D3.js force-directed graph. Pan, zoom, filter by type, and search by name.
- **Per-page relationship maps** — each artist, person, album, or song page has its own mini-graph showing its full connected neighborhood.
- **Zoom-out cluster labels** — artist names and scene names (Seattle, Chicago, etc.) fade in as you zoom out, labeling the clusters.
- **Full credit tracking** — every player, songwriter, and producer on every song is linked, and followed to every other project they've been part of.

---

## Site Structure

```
content/
  artists/    — Bands and solo acts (18)
  albums/     — Studio albums and EPs (39)
  songs/      — Individual tracks (162)
  people/     — Musicians, producers, songwriters (63)
```

**Graph:** 282 nodes · 1,723 links · 412 pages

---

## Content Covered

### Scenes

| Scene | Artists |
|-------|---------|
| Seattle | Nirvana, Pearl Jam, Foo Fighters, Sunny Day Real Estate |
| Boston / Mass | Pixies, Frank Black, The Breeders, Throwing Muses |
| Oxford, UK | Radiohead |
| Athens, GA | R.E.M. |
| San Francisco | 4 Non Blondes |
| Los Angeles | The Germs, Queens of the Stone Age, Them Crooked Vultures |
| London, UK | Led Zeppelin |
| Madison, WI | Garbage |
| Palm Desert | Queens of the Stone Age |
| Pop | Christina Aguilera, Pink |

---

## How It Works

### Data Flow

```
content/**/*.md  (Hugo YAML front matter)
       │
       ▼
scripts/rebuild_graph.py
       │
       ▼
static/data/graph.json  (282 nodes, 1,723 links)
       │
       ▼
D3.js (graph.js / mini-graph.js)  →  browser
```

Every relationship is derived automatically from front matter — no manual graph editing needed. Just add or edit content files and re-run the script.

### Rebuild Graph

After adding or editing any content:

```bash
pip install pyyaml   # only needed once
python scripts/rebuild_graph.py
```

Output: `static/data/graph.json` (and `data/graph.json`)

---

## Content File Format

### Artist (`content/artists/{slug}.md`)
```yaml
---
scene: "Seattle"
title: "Nirvana"
country: "US"
formed: 1987
band_type: "Group"          # Group or Solo
genres: ["grunge", "alternative rock"]
members:
  - slug: "kurt-cobain"
    name: "Kurt Cobain"
    role: "Vocals, Guitar (1987–1994)"
albums:
  - slug: "nevermind"
    title: "Nevermind"
    year: 1991
draft: false
---
Bio paragraph.
```

### Album (`content/albums/{slug}.md`)
```yaml
---
title: "Nevermind"
artist: "Nirvana"
artist_slug: "nirvana"
year: 1991
genres: ["grunge"]
tracks:
  - slug: "smells-like-teen-spirit"
    title: "Smells Like Teen Spirit"
    track_number: 1
draft: false
---
```

### Song (`content/songs/{slug}.md`)
```yaml
---
title: "Smells Like Teen Spirit"
artist: "Nirvana"
artist_slug: "nirvana"
album: "Nevermind"
album_slug: "nevermind"
year: 1991
writers:
  - slug: "kurt-cobain"
    name: "Kurt Cobain"
producers:
  - slug: "butch-vig"
    name: "Butch Vig"
players:
  - slug: "kurt-cobain"
    name: "Kurt Cobain"
    instrument: "Vocals, Guitar"
  - slug: "krist-novoselic"
    name: "Krist Novoselic"
    instrument: "Bass"
  - slug: "dave-grohl"
    name: "Dave Grohl"
    instrument: "Drums"
draft: false
---
```

### Person (`content/people/{slug}.md`)
```yaml
---
title: "Butch Vig"
born: 1955
nationality: "American"
roles: ["Producer", "Drums"]
bands:
  - slug: "garbage"
    name: "Garbage"
    years: "1993–present"
song_credits:
  - slug: "smells-like-teen-spirit"
    title: "Smells Like Teen Spirit"
    credit: "Producer"
draft: false
---
```

> **Note:** Do NOT use `type:` in front matter — Hugo infers content type from the directory name. Use `band_type:` for Solo/Group distinction on artists.

---

## Theme & Tech Stack

| Layer | Technology |
|-------|-----------|
| Static site | [Hugo](https://gohugo.io) v0.153+ |
| Graph rendering | [D3.js](https://d3js.org) v7 (force simulation) |
| Styling | Custom dark CSS (`themes/musictree/assets/css/main.css`) |
| Data | YAML front matter → Python → JSON |
| Python dep | `pyyaml` |

### Theme Layout

```
themes/musictree/
  layouts/
    baseof.html          — base shell (nav, footer)
    home.html            — full D3 graph + filters
    section.html         — listing pages (artists, songs, etc.)
    _partials/
      mini-graph.html    — mini-graph partial included on all content pages
    artists/page.html
    albums/page.html
    songs/page.html
    people/page.html
  static/js/
    graph.js             — homepage D3 force graph with cluster labels
    mini-graph.js        — per-page BFS mini-graph (fetches /data/graph.json)
  assets/css/
    main.css             — dark theme
```

### Graph Node Colors

| Type | Color |
|------|-------|
| Artist | Blue `#4e79a7` |
| Person | Green `#59a14f` |
| Album | Purple `#b07aa1` |
| Song | Orange `#f28e2b` |

### Graph Edge Types

| Relation | Meaning |
|----------|---------|
| `member-of` | Person is a member of an artist/band |
| `released` | Artist released an album |
| `appears-on` | Song appears on an album |
| `performed-by` | Person performed on a song |
| `written-by` | Person wrote a song |
| `produced-by` | Person produced a song |
| `played` | Person played an instrument on a song |

---

## Development

### Prerequisites

- [Hugo](https://gohugo.io/installation/) v0.100+
- Python 3.8+ with `pyyaml` (`pip install pyyaml`)

### Run Locally

```bash
hugo server
# Opens at http://localhost:1313
```

### Add New Content

1. Create content files in `content/artists/`, `content/albums/`, `content/songs/`, or `content/people/`
2. Rebuild the graph: `python scripts/rebuild_graph.py`
3. Hugo will hot-reload automatically (or restart `hugo server`)

### Build for Production

```bash
hugo --minify
# Output in public/
```

---

## Adding a New Scene

1. Add `scene: "Your Scene"` to each artist's front matter
2. The scene centroid label appears automatically on the homepage graph when zoomed out past ~38% scale
3. Run `python scripts/rebuild_graph.py` to include the scene field in `graph.json`

---

## Performance Notes

- `static/data/graph.json` is fetched once by the browser and cached — it is **not** embedded inline on every page
- Mini-graph BFS is capped at 80 nodes to prevent browser freeze
- The D3 simulation on mini-graphs auto-stops after 4 seconds
- The homepage graph runs the full simulation against all nodes

---

## Repository Structure

```
MusicTree/
├── content/
│   ├── artists/       # 18 artist .md files
│   ├── albums/        # 39 album .md files
│   ├── songs/         # 162 song .md files
│   └── people/        # 63 person .md files
├── scripts/
│   └── rebuild_graph.py   # Generates graph.json from content
├── static/
│   └── data/
│       └── graph.json     # Served at /data/graph.json
├── data/
│   └── graph.json         # Hugo data dir copy
├── themes/
│   └── musictree/         # Custom Hugo theme
└── hugo.toml              # Site config
```
