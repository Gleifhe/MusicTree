---
description: "Use when creating or editing MusicTree content files: artists, albums, songs, people. Covers exact YAML schemas, field names, slug conventions, and common mistakes to avoid."
applyTo: "content/**"
---
# MusicTree Content Schema

## Artist file — `content/artists/<slug>.md`
```yaml
---
title: "Band Name"
slug: band-slug
band_type: Group          # Group | Solo
genres: [Alternative Rock]
scene: Seattle
members:
  - slug: person-slug
    role: Guitar
albums:
  - slug: album-slug
---
```

## Album file — `content/albums/<slug>.md`
```yaml
---
title: "Album Title"
slug: album-slug
artist: artist-slug
year: 1991
producer: producer-person-slug
songs:
  - slug: song-slug
    title: "Song Title"
---
```
⚠ Use `songs:` — **never** `tracks:`

## Song file — `content/songs/<slug>.md`
```yaml
---
title: "Song Title"
slug: song-slug
artist: artist-slug
album: album-slug
year: 1991
credits:
  - person_slug: dave-grohl
    role: Drums
  - person_slug: butch-vig
    role: Producer
  - person_slug: kurt-cobain
    role: Writer
---
```
⚠ Use `credits: [{person_slug, role}]` — **never** `writers:` / `producers:` / `players:` as separate fields

## Person file — `content/people/<slug>.md`
```yaml
---
title: "Full Name"
slug: person-slug
bands:
  - slug: artist-slug
    role: Guitar
song_credits:
  - slug: song-slug
    title: "Song Title"
    credit: Writer
---
```
⚠ Use `song_credits:` — **never** `credits:` for a person's song references

## Hard rules
1. **No `type:` in front matter** — Hugo uses directory name
2. **Write files with Python** — PowerShell `Set-Content` adds UTF-8 BOM
3. **Song slugs must be globally unique** — suffix with artist code when needed (`come-as-you-are-nv`)
4. **Every song must have at least one credit** — writer, producer, or player
5. **Every artist must have a `scene:` field**
6. **Every album must list all songs in `songs:`**
7. **Run `python scripts/rebuild_graph.py` after any content change**
