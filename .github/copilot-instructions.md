# MusicTree Project Guidelines

## Overview
Hugo-based music family tree site. Content lives in `content/` as Markdown files with YAML front matter. A Python script (`scripts/rebuild_graph.py`) reads all content and builds `static/data/graph.json` for the D3.js visualization.

## Architecture
- `content/artists/` — one `.md` per artist/band
- `content/albums/` — one `.md` per album
- `content/songs/` — one `.md` per song
- `content/people/` — one `.md` per person (musicians, producers, writers)
- `scripts/rebuild_graph.py` — derives `graph.json` from all content (run after any change)
- `themes/musictree/static/js/graph.js` — D3 homepage force graph with scene clustering
- `themes/musictree/static/js/mini-graph.js` — per-page mini relationship graph

## Build and Test
```
# After any content change:
python scripts/rebuild_graph.py

# Quality audit:
python scripts/quality_check.py

# Local dev server:
hugo server

# Full build:
hugo
```

## Conventions

### CRITICAL: Canonical YAML Schemas — always use these exact field names

**Artist** (`content/artists/<slug>.md`):
```yaml
---
title: "Band Name"
slug: band-slug
band_type: Group          # or Solo
genres: [Alternative Rock]
scene: Seattle            # required — see scene list below
members:
  - slug: person-slug
    role: Guitar
albums:
  - slug: album-slug
---
```

**Album** (`content/albums/<slug>.md`):
```yaml
---
title: "Album Title"
slug: album-slug
artist: artist-slug
year: 1991
producer: producer-person-slug
songs:                    # ALWAYS use 'songs:' — never 'tracks:'
  - slug: song-slug
    title: "Song Title"
---
```

**Song** (`content/songs/<slug>.md`):
```yaml
---
title: "Song Title"
slug: song-slug
artist: artist-slug
album: album-slug
year: 1991
credits:                  # ALWAYS use 'credits:' list — never 'writers:/producers:/players:' separate fields
  - person_slug: person-slug
    role: Writer          # Writer | Producer | Guitar | Bass | Drums | Vocals | Keyboards | etc.
  - person_slug: other-slug
    role: Producer
---
```

**Person** (`content/people/<slug>.md`):
```yaml
---
title: "Full Name"
slug: person-slug
bands:
  - slug: artist-slug
    role: Guitar
song_credits:             # ALWAYS use 'song_credits:' — never 'credits:' for people
  - slug: song-slug
    title: "Song Title"
    credit: Writer        # Writer | Producer | Guitar | Bass | Drums | Vocals | etc.
---
```

### Schema rules (never break these)
- Albums use `songs:` (not `tracks:`)
- Songs use `credits: [{person_slug, role}]` (not `writers:/producers:/players:`)
- People use `song_credits: [{slug, title, credit}]` (not `credits:` for song refs)
- `type:` must NEVER appear in front matter — Hugo infers type from directory name
- All file writes must use Python `Path(...).write_text(content, encoding="utf-8")` — PowerShell `Set-Content` adds a UTF-8 BOM that breaks Hugo

### Slug conventions
- Slugs are kebab-case, globally unique
- Song slugs: add artist suffix for disambiguation (`shake-it-off-tsw`, not `shake-it-off`)
- Person slugs: `firstname-lastname` (`dave-grohl`, `jack-antonoff`)
- Album slugs: `album-name-artistabbrev` when needed for uniqueness

### Scenes (use exact strings)
```
Seattle | Chicago | Boston | Alternative Rock | Indie Rock | Indie Pop
Pop | Hip-Hop | R&B | Rock | Country | Folk | Latin
Los Angeles | Palm Desert | Athens, GA | Providence
Oxford, UK | London, UK | Madison, WI | San Francisco | Gospel/Funk
Canadian | Punk Rock
```
Avoid creating new scene names — map to the nearest existing scene.
