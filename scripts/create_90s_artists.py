#!/usr/bin/env python3
"""Create Hugo content files for 25 alternative/indie/britpop artists."""
from pathlib import Path

BASE = Path(r"c:\repo\MusicTree\content")
ARTISTS_DIR = BASE / "artists"
ALBUMS_DIR = BASE / "albums"
SONGS_DIR = BASE / "songs"
PEOPLE_DIR = BASE / "people"

for d in [ARTISTS_DIR, ALBUMS_DIR, SONGS_DIR, PEOPLE_DIR]:
    d.mkdir(parents=True, exist_ok=True)

created = 0
skipped = 0


def write_file(path, content):
    global created, skipped
    if path.exists():
        print(f"  SKIP: {path.name}")
        skipped += 1
    else:
        path.write_text(content, encoding="utf-8")
        print(f"  CREATE: {path.name}")
        created += 1


def artist(slug, title, band_type, genres, scene, formed, members, albums):
    lines = ["---"]
    lines.append(f'title: "{title}"')
    lines.append(f"slug: {slug}")
    lines.append(f"band_type: {band_type}")
    lines.append(f"genres: [{', '.join(genres)}]")
    lines.append(f"scene: {scene}")
    lines.append(f"formed: {formed}")
    lines.append("members:")
    for m in members:
        lines.append(f'  - slug: {m["slug"]}')
        lines.append(f'    role: {m["role"]}')
    lines.append("albums:")
    for a in albums:
        lines.append(f'  - slug: {a["slug"]}')
        lines.append(f'    title: "{a["title"]}"')
        lines.append(f'    year: {a["year"]}')
    lines.append("---")
    return "\n".join(lines) + "\n"


def album(slug, title, artist_slug, year, producer, songs):
    lines = ["---"]
    lines.append(f'title: "{title}"')
    lines.append(f"slug: {slug}")
    lines.append(f"artist: {artist_slug}")
    lines.append(f"year: {year}")
    lines.append(f"producer: {producer}")
    lines.append("songs:")
    for s in songs:
        lines.append(f'  - slug: {s["slug"]}')
        lines.append(f'    title: "{s["title"]}"')
    lines.append("---")
    return "\n".join(lines) + "\n"


def song(slug, title, artist_slug, album_slug, year, credits):
    lines = ["---"]
    lines.append(f'title: "{title}"')
    lines.append(f"slug: {slug}")
    lines.append(f"artist: {artist_slug}")
    lines.append(f"album: {album_slug}")
    lines.append(f"year: {year}")
    lines.append("credits:")
    for c in credits:
        lines.append(f'  - person_slug: {c["person_slug"]}')
        lines.append(f'    role: {c["role"]}')
    lines.append("---")
    return "\n".join(lines) + "\n"


def person(slug, title, bands, song_credits):
    lines = ["---"]
    lines.append(f'title: "{title}"')
    lines.append(f"slug: {slug}")
    lines.append("bands:")
    for b in bands:
        lines.append(f'  - slug: {b["slug"]}')
        lines.append(f'    role: {b["role"]}')
    lines.append("song_credits:")
    for sc in song_credits:
        lines.append(f'  - slug: {sc["slug"]}')
        lines.append(f'    title: "{sc["title"]}"')
        lines.append(f'    credit: {sc["credit"]}')
    lines.append("---")
    return "\n".join(lines) + "\n"


# ============================================================
# 1. Stone Temple Pilots
# ============================================================
print("\n=== Stone Temple Pilots ===")
write_file(ARTISTS_DIR / "stone-temple-pilots.md", artist(
    "stone-temple-pilots", "Stone Temple Pilots", "Group",
    ["Alternative Rock"], "Alternative Rock", 1987,
    [{"slug": "scott-weiland", "role": "Vocals"},
     {"slug": "robert-deleo", "role": "Bass"},
     {"slug": "dean-deleo", "role": "Guitar"},
     {"slug": "eric-kretz", "role": "Drums"}],
    [{"slug": "core-stp", "title": "Core", "year": 1992},
     {"slug": "purple-stp", "title": "Purple", "year": 1994},
     {"slug": "tiny-music-stp", "title": "Tiny Music... Songs from the Vatican Gift Shop", "year": 1996},
     {"slug": "no-4-stp", "title": "No. 4", "year": 1999}]
))

stp_core_songs = [
    ("plush-stp", "Plush"), ("creep-stp", "Creep"),
    ("wicked-garden-stp", "Wicked Garden"), ("sex-type-thing-stp", "Sex Type Thing"),
]
stp_purple_songs = [
    ("vasoline-stp", "Vasoline"), ("tumble-in-the-rough-stp", "Tumble in the Rough"),
    ("still-remains-stp", "Still Remains"), ("lady-picture-show-stp", "Lady Picture Show"),
]
stp_tiny_songs = [("trippin-on-a-hole-stp", "Trippin' on a Hole in a Paper Heart")]

write_file(ALBUMS_DIR / "core-stp.md", album("core-stp", "Core", "stone-temple-pilots", 1992, "brendan-obrien",
    [{"slug": s[0], "title": s[1]} for s in stp_core_songs]))
write_file(ALBUMS_DIR / "purple-stp.md", album("purple-stp", "Purple", "stone-temple-pilots", 1994, "brendan-obrien",
    [{"slug": s[0], "title": s[1]} for s in stp_purple_songs]))
write_file(ALBUMS_DIR / "tiny-music-stp.md", album("tiny-music-stp", "Tiny Music... Songs from the Vatican Gift Shop",
    "stone-temple-pilots", 1996, "brendan-obrien", [{"slug": s[0], "title": s[1]} for s in stp_tiny_songs]))
write_file(ALBUMS_DIR / "no-4-stp.md", album("no-4-stp", "No. 4", "stone-temple-pilots", 1999, "brendan-obrien", []))

for s in stp_core_songs:
    write_file(SONGS_DIR / f"{s[0]}.md", song(s[0], s[1], "stone-temple-pilots", "core-stp", 1992,
        [{"person_slug": "scott-weiland", "role": "Writer"}, {"person_slug": "brendan-obrien", "role": "Producer"}]))
for s in stp_purple_songs:
    write_file(SONGS_DIR / f"{s[0]}.md", song(s[0], s[1], "stone-temple-pilots", "purple-stp", 1994,
        [{"person_slug": "scott-weiland", "role": "Writer"}, {"person_slug": "brendan-obrien", "role": "Producer"}]))
for s in stp_tiny_songs:
    write_file(SONGS_DIR / f"{s[0]}.md", song(s[0], s[1], "stone-temple-pilots", "tiny-music-stp", 1996,
        [{"person_slug": "scott-weiland", "role": "Writer"}, {"person_slug": "brendan-obrien", "role": "Producer"}]))

stp_all = [{"slug": s[0], "title": s[1]} for s in stp_core_songs + stp_purple_songs + stp_tiny_songs]
write_file(PEOPLE_DIR / "scott-weiland.md", person("scott-weiland", "Scott Weiland",
    [{"slug": "stone-temple-pilots", "role": "Vocals"}],
    [{"slug": s["slug"], "title": s["title"], "credit": "Writer"} for s in stp_all]))
write_file(PEOPLE_DIR / "robert-deleo.md", person("robert-deleo", "Robert DeLeo",
    [{"slug": "stone-temple-pilots", "role": "Bass"}], []))
write_file(PEOPLE_DIR / "dean-deleo.md", person("dean-deleo", "Dean DeLeo",
    [{"slug": "stone-temple-pilots", "role": "Guitar"}], []))
write_file(PEOPLE_DIR / "eric-kretz.md", person("eric-kretz", "Eric Kretz",
    [{"slug": "stone-temple-pilots", "role": "Drums"}], []))
write_file(PEOPLE_DIR / "brendan-obrien.md", person("brendan-obrien", "Brendan O'Brien", [],
    [{"slug": s["slug"], "title": s["title"], "credit": "Producer"} for s in stp_all]))


# ============================================================
# 2. Nine Inch Nails
# ============================================================
print("\n=== Nine Inch Nails ===")
write_file(ARTISTS_DIR / "nine-inch-nails.md", artist(
    "nine-inch-nails", "Nine Inch Nails", "Solo",
    ["Industrial Rock", "Alternative Rock"], "Alternative Rock", 1988,
    [{"slug": "trent-reznor", "role": "Vocals/Everything"},
     {"slug": "robin-finck", "role": "Guitar"},
     {"slug": "charlie-clouser", "role": "Keyboards"}],
    [{"slug": "pretty-hate-machine-nin", "title": "Pretty Hate Machine", "year": 1989},
     {"slug": "broken-nin", "title": "Broken", "year": 1992},
     {"slug": "downward-spiral-nin", "title": "The Downward Spiral", "year": 1994},
     {"slug": "fragile-nin", "title": "The Fragile", "year": 1999},
     {"slug": "with-teeth-nin", "title": "With Teeth", "year": 2005},
     {"slug": "year-zero-nin", "title": "Year Zero", "year": 2007},
     {"slug": "ghosts-i-iv-nin", "title": "Ghosts I-IV", "year": 2008},
     {"slug": "the-slip-nin", "title": "The Slip", "year": 2008},
     {"slug": "hesitation-marks-nin", "title": "Hesitation Marks", "year": 2013}]
))

nin_albums = [
    ("pretty-hate-machine-nin", "Pretty Hate Machine", 1989,
     [("head-like-a-hole-nin", "Head Like a Hole"), ("terrible-lie-nin", "Terrible Lie")]),
    ("broken-nin", "Broken", 1992,
     [("wish-nin", "Wish"), ("march-of-the-pigs-nin", "March of the Pigs")]),
    ("downward-spiral-nin", "The Downward Spiral", 1994,
     [("hurt-nin", "Hurt"), ("closer-nin", "Closer")]),
    ("fragile-nin", "The Fragile", 1999,
     [("were-in-this-together-nin", "We're in This Together")]),
    ("with-teeth-nin", "With Teeth", 2005,
     [("the-hand-that-feeds-nin", "The Hand That Feeds")]),
    ("year-zero-nin", "Year Zero", 2007, []),
    ("ghosts-i-iv-nin", "Ghosts I-IV", 2008, []),
    ("the-slip-nin", "The Slip", 2008, []),
    ("hesitation-marks-nin", "Hesitation Marks", 2013, []),
]

nin_all_songs = []
for alb_slug, alb_title, alb_year, songs_list in nin_albums:
    song_dicts = [{"slug": s[0], "title": s[1]} for s in songs_list]
    write_file(ALBUMS_DIR / f"{alb_slug}.md", album(alb_slug, alb_title, "nine-inch-nails", alb_year, "trent-reznor", song_dicts))
    for s in songs_list:
        write_file(SONGS_DIR / f"{s[0]}.md", song(s[0], s[1], "nine-inch-nails", alb_slug, alb_year,
            [{"person_slug": "trent-reznor", "role": "Writer"}, {"person_slug": "trent-reznor", "role": "Producer"}]))
        nin_all_songs.append({"slug": s[0], "title": s[1]})

write_file(PEOPLE_DIR / "robin-finck.md", person("robin-finck", "Robin Finck",
    [{"slug": "nine-inch-nails", "role": "Guitar"}], []))
write_file(PEOPLE_DIR / "charlie-clouser.md", person("charlie-clouser", "Charlie Clouser",
    [{"slug": "nine-inch-nails", "role": "Keyboards"}], []))
write_file(PEOPLE_DIR / "alan-moulder.md", person("alan-moulder", "Alan Moulder", [], []))


# ============================================================
# 3. Rage Against the Machine
# ============================================================
print("\n=== Rage Against the Machine ===")
write_file(ARTISTS_DIR / "rage-against-the-machine.md", artist(
    "rage-against-the-machine", "Rage Against the Machine", "Group",
    ["Alternative Metal", "Rap Metal"], "Los Angeles", 1991,
    [{"slug": "zack-de-la-rocha", "role": "Vocals"},
     {"slug": "tom-morello", "role": "Guitar"},
     {"slug": "tim-commerford", "role": "Bass"},
     {"slug": "brad-wilk", "role": "Drums"}],
    [{"slug": "ratm-self-titled", "title": "Rage Against the Machine", "year": 1992},
     {"slug": "evil-empire-ratm", "title": "Evil Empire", "year": 1996},
     {"slug": "battle-of-la-ratm", "title": "The Battle of Los Angeles", "year": 1999},
     {"slug": "renegades-ratm", "title": "Renegades", "year": 2000}]
))

ratm_albums = [
    ("ratm-self-titled", "Rage Against the Machine", 1992, [
        ("killing-in-the-name-ratm", "Killing in the Name"),
        ("bullet-in-the-head-ratm", "Bullet in the Head"),
        ("bombtrack-ratm", "Bombtrack"),
        ("wake-up-ratm", "Wake Up"),
    ]),
    ("evil-empire-ratm", "Evil Empire", 1996, [("bulls-on-parade-ratm", "Bulls on Parade")]),
    ("battle-of-la-ratm", "The Battle of Los Angeles", 1999, [
        ("guerrilla-radio-ratm", "Guerrilla Radio"),
        ("sleep-now-in-the-fire-ratm", "Sleep Now in the Fire"),
        ("testify-ratm", "Testify"),
    ]),
    ("renegades-ratm", "Renegades", 2000, [("renegades-ratm-s", "Renegades")]),
]

ratm_all_songs = []
for alb_slug, alb_title, alb_year, songs_list in ratm_albums:
    song_dicts = [{"slug": s[0], "title": s[1]} for s in songs_list]
    write_file(ALBUMS_DIR / f"{alb_slug}.md", album(alb_slug, alb_title, "rage-against-the-machine", alb_year, "brendan-obrien", song_dicts))
    for s in songs_list:
        write_file(SONGS_DIR / f"{s[0]}.md", song(s[0], s[1], "rage-against-the-machine", alb_slug, alb_year,
            [{"person_slug": "zack-de-la-rocha", "role": "Writer"}, {"person_slug": "brendan-obrien", "role": "Producer"}]))
        ratm_all_songs.append({"slug": s[0], "title": s[1]})

write_file(PEOPLE_DIR / "zack-de-la-rocha.md", person("zack-de-la-rocha", "Zack de la Rocha",
    [{"slug": "rage-against-the-machine", "role": "Vocals"}],
    [{"slug": s["slug"], "title": s["title"], "credit": "Writer"} for s in ratm_all_songs]))
write_file(PEOPLE_DIR / "ggarth-richardson.md", person("ggarth-richardson", "GGGarth Richardson", [], []))


# ============================================================
# 4. Faith No More
# ============================================================
print("\n=== Faith No More ===")
write_file(ARTISTS_DIR / "faith-no-more.md", artist(
    "faith-no-more", "Faith No More", "Group",
    ["Alternative Metal", "Art Rock"], "San Francisco", 1979,
    [{"slug": "mike-patton", "role": "Vocals"},
     {"slug": "roddy-bottum", "role": "Keyboards"},
     {"slug": "billy-gould", "role": "Bass"},
     {"slug": "mike-bordin", "role": "Drums"},
     {"slug": "jim-martin-fnm", "role": "Guitar"}],
    [{"slug": "we-care-a-lot-fnm", "title": "We Care a Lot", "year": 1985},
     {"slug": "introduce-yourself-fnm", "title": "Introduce Yourself", "year": 1987},
     {"slug": "the-real-thing-fnm", "title": "The Real Thing", "year": 1989},
     {"slug": "angel-dust-fnm", "title": "Angel Dust", "year": 1992},
     {"slug": "king-for-a-day-fnm", "title": "King for a Day... Fool for a Lifetime", "year": 1995},
     {"slug": "album-of-the-year-fnm", "title": "Album of the Year", "year": 1997}]
))

fnm_albums = [
    ("we-care-a-lot-fnm", "We Care a Lot", 1985, "matt-wallace",
     [("we-care-a-lot-fnm-s", "We Care a Lot")]),
    ("introduce-yourself-fnm", "Introduce Yourself", 1987, "matt-wallace", []),
    ("the-real-thing-fnm", "The Real Thing", 1989, "matt-wallace",
     [("epic-fnm", "Epic"), ("falling-to-pieces-fnm", "Falling to Pieces")]),
    ("angel-dust-fnm", "Angel Dust", 1992, "matt-wallace",
     [("midlife-crisis-fnm", "Midlife Crisis"), ("a-small-victory-fnm", "A Small Victory"), ("easy-fnm", "Easy")]),
    ("king-for-a-day-fnm", "King for a Day... Fool for a Lifetime", 1995, "billy-gould",
     [("digging-the-grave-fnm", "Digging the Grave")]),
    ("album-of-the-year-fnm", "Album of the Year", 1997, "billy-gould",
     [("ashes-to-ashes-fnm", "Ashes to Ashes")]),
]

fnm_all_songs = []
fnm_matt_songs = []
fnm_billy_songs = []
for alb_slug, alb_title, alb_year, prod, songs_list in fnm_albums:
    song_dicts = [{"slug": s[0], "title": s[1]} for s in songs_list]
    write_file(ALBUMS_DIR / f"{alb_slug}.md", album(alb_slug, alb_title, "faith-no-more", alb_year, prod, song_dicts))
    for s in songs_list:
        write_file(SONGS_DIR / f"{s[0]}.md", song(s[0], s[1], "faith-no-more", alb_slug, alb_year,
            [{"person_slug": "mike-patton", "role": "Writer"}, {"person_slug": prod, "role": "Producer"}]))
        fnm_all_songs.append({"slug": s[0], "title": s[1]})
        if prod == "matt-wallace":
            fnm_matt_songs.append({"slug": s[0], "title": s[1]})
        else:
            fnm_billy_songs.append({"slug": s[0], "title": s[1]})

write_file(PEOPLE_DIR / "roddy-bottum.md", person("roddy-bottum", "Roddy Bottum",
    [{"slug": "faith-no-more", "role": "Keyboards"}], []))
write_file(PEOPLE_DIR / "billy-gould.md", person("billy-gould", "Billy Gould",
    [{"slug": "faith-no-more", "role": "Bass"}],
    [{"slug": s["slug"], "title": s["title"], "credit": "Producer"} for s in fnm_billy_songs]))
write_file(PEOPLE_DIR / "mike-bordin.md", person("mike-bordin", "Mike Bordin",
    [{"slug": "faith-no-more", "role": "Drums"}], []))
write_file(PEOPLE_DIR / "jim-martin-fnm.md", person("jim-martin-fnm", "Jim Martin",
    [{"slug": "faith-no-more", "role": "Guitar"}], []))
write_file(PEOPLE_DIR / "matt-wallace.md", person("matt-wallace", "Matt Wallace", [],
    [{"slug": s["slug"], "title": s["title"], "credit": "Producer"} for s in fnm_matt_songs]))


# ============================================================
# 5. Bush
# ============================================================
print("\n=== Bush ===")
write_file(ARTISTS_DIR / "bush.md", artist(
    "bush", "Bush", "Group",
    ["Alternative Rock", "Post-Grunge"], "Alternative Rock", 1992,
    [{"slug": "gavin-rossdale", "role": "Vocals/Guitar"},
     {"slug": "nigel-pulsford", "role": "Guitar"},
     {"slug": "dave-parsons", "role": "Bass"},
     {"slug": "robin-goodridge", "role": "Drums"}],
    [{"slug": "sixteen-stone-bush", "title": "Sixteen Stone", "year": 1994},
     {"slug": "razorblade-suitcase-bush", "title": "Razorblade Suitcase", "year": 1996},
     {"slug": "science-of-things-bush", "title": "The Science of Things", "year": 1999},
     {"slug": "golden-state-bush", "title": "Golden State", "year": 2001}]
))

bush_ss = [("everything-zen-bush", "Everything Zen"), ("glycerine-bush", "Glycerine"),
           ("machinehead-bush", "Machinehead"), ("comedown-bush", "Comedown")]
bush_rz = [("swallowed-bush", "Swallowed"), ("greedy-fly-bush", "Greedy Fly")]
bush_st = [("chemicals-between-us-bush", "The Chemicals Between Us")]

write_file(ALBUMS_DIR / "sixteen-stone-bush.md", album("sixteen-stone-bush", "Sixteen Stone", "bush", 1994, "brendan-obrien",
    [{"slug": s[0], "title": s[1]} for s in bush_ss]))
write_file(ALBUMS_DIR / "razorblade-suitcase-bush.md", album("razorblade-suitcase-bush", "Razorblade Suitcase", "bush", 1996, "steve-albini",
    [{"slug": s[0], "title": s[1]} for s in bush_rz]))
write_file(ALBUMS_DIR / "science-of-things-bush.md", album("science-of-things-bush", "The Science of Things", "bush", 1999, "gavin-rossdale",
    [{"slug": s[0], "title": s[1]} for s in bush_st]))
write_file(ALBUMS_DIR / "golden-state-bush.md", album("golden-state-bush", "Golden State", "bush", 2001, "gavin-rossdale", []))

for s in bush_ss:
    write_file(SONGS_DIR / f"{s[0]}.md", song(s[0], s[1], "bush", "sixteen-stone-bush", 1994,
        [{"person_slug": "gavin-rossdale", "role": "Writer"}, {"person_slug": "brendan-obrien", "role": "Producer"}]))
for s in bush_rz:
    write_file(SONGS_DIR / f"{s[0]}.md", song(s[0], s[1], "bush", "razorblade-suitcase-bush", 1996,
        [{"person_slug": "gavin-rossdale", "role": "Writer"}, {"person_slug": "steve-albini", "role": "Producer"}]))
for s in bush_st:
    write_file(SONGS_DIR / f"{s[0]}.md", song(s[0], s[1], "bush", "science-of-things-bush", 1999,
        [{"person_slug": "gavin-rossdale", "role": "Writer"}, {"person_slug": "gavin-rossdale", "role": "Producer"}]))

bush_all = [{"slug": s[0], "title": s[1]} for s in bush_ss + bush_rz + bush_st]
write_file(PEOPLE_DIR / "gavin-rossdale.md", person("gavin-rossdale", "Gavin Rossdale",
    [{"slug": "bush", "role": "Vocals/Guitar"}],
    [{"slug": s["slug"], "title": s["title"], "credit": "Writer"} for s in bush_all]))
write_file(PEOPLE_DIR / "nigel-pulsford.md", person("nigel-pulsford", "Nigel Pulsford",
    [{"slug": "bush", "role": "Guitar"}], []))
write_file(PEOPLE_DIR / "dave-parsons.md", person("dave-parsons", "Dave Parsons",
    [{"slug": "bush", "role": "Bass"}], []))
write_file(PEOPLE_DIR / "robin-goodridge.md", person("robin-goodridge", "Robin Goodridge",
    [{"slug": "bush", "role": "Drums"}], []))


# ============================================================
# 6. Oasis
# ============================================================
print("\n=== Oasis ===")
write_file(ARTISTS_DIR / "oasis.md", artist(
    "oasis", "Oasis", "Group",
    ["Britpop", "Alternative Rock"], "Alternative Rock", 1991,
    [{"slug": "liam-gallagher", "role": "Vocals"},
     {"slug": "noel-gallagher", "role": "Guitar/Vocals"},
     {"slug": "paul-arthurs", "role": "Guitar"},
     {"slug": "paul-mcguigan", "role": "Bass"},
     {"slug": "tony-mccarroll", "role": "Drums"},
     {"slug": "alan-white-oasis", "role": "Drums"}],
    [{"slug": "definitely-maybe-oas", "title": "Definitely Maybe", "year": 1994},
     {"slug": "morning-glory-oas", "title": "(What's the Story) Morning Glory?", "year": 1995},
     {"slug": "be-here-now-oas", "title": "Be Here Now", "year": 1997},
     {"slug": "standing-on-shoulders-oas", "title": "Standing on the Shoulder of Giants", "year": 2000},
     {"slug": "heathen-chemistry-oas", "title": "Heathen Chemistry", "year": 2002},
     {"slug": "dont-believe-the-truth-oas", "title": "Don't Believe the Truth", "year": 2005},
     {"slug": "dig-out-your-soul-oas", "title": "Dig Out Your Soul", "year": 2008}]
))

oas_dm = [("supersonic-oas", "Supersonic"), ("live-forever-oas", "Live Forever")]
oas_mg = [("wonderwall-oas", "Wonderwall"), ("dont-look-back-in-anger-oas", "Don't Look Back in Anger"),
          ("champagne-supernova-oas", "Champagne Supernova"), ("some-might-say-oas", "Some Might Say"),
          ("morning-glory-oas-s", "Morning Glory")]
oas_bhn = [("dykwim-oas", "D'You Know What I Mean?")]

write_file(ALBUMS_DIR / "definitely-maybe-oas.md", album("definitely-maybe-oas", "Definitely Maybe", "oasis", 1994, "owen-morris",
    [{"slug": s[0], "title": s[1]} for s in oas_dm]))
write_file(ALBUMS_DIR / "morning-glory-oas.md", album("morning-glory-oas", "(What's the Story) Morning Glory?", "oasis", 1995, "owen-morris",
    [{"slug": s[0], "title": s[1]} for s in oas_mg]))
write_file(ALBUMS_DIR / "be-here-now-oas.md", album("be-here-now-oas", "Be Here Now", "oasis", 1997, "owen-morris",
    [{"slug": s[0], "title": s[1]} for s in oas_bhn]))
write_file(ALBUMS_DIR / "standing-on-shoulders-oas.md", album("standing-on-shoulders-oas", "Standing on the Shoulder of Giants", "oasis", 2000, "mark-stent", []))
write_file(ALBUMS_DIR / "heathen-chemistry-oas.md", album("heathen-chemistry-oas", "Heathen Chemistry", "oasis", 2002, "noel-gallagher", []))
write_file(ALBUMS_DIR / "dont-believe-the-truth-oas.md", album("dont-believe-the-truth-oas", "Don't Believe the Truth", "oasis", 2005, "noel-gallagher", []))
write_file(ALBUMS_DIR / "dig-out-your-soul-oas.md", album("dig-out-your-soul-oas", "Dig Out Your Soul", "oasis", 2008, "noel-gallagher", []))

for s in oas_dm:
    write_file(SONGS_DIR / f"{s[0]}.md", song(s[0], s[1], "oasis", "definitely-maybe-oas", 1994,
        [{"person_slug": "noel-gallagher", "role": "Writer"}, {"person_slug": "owen-morris", "role": "Producer"}]))
for s in oas_mg:
    write_file(SONGS_DIR / f"{s[0]}.md", song(s[0], s[1], "oasis", "morning-glory-oas", 1995,
        [{"person_slug": "noel-gallagher", "role": "Writer"}, {"person_slug": "owen-morris", "role": "Producer"}]))
for s in oas_bhn:
    write_file(SONGS_DIR / f"{s[0]}.md", song(s[0], s[1], "oasis", "be-here-now-oas", 1997,
        [{"person_slug": "noel-gallagher", "role": "Writer"}, {"person_slug": "owen-morris", "role": "Producer"}]))

oas_all = [{"slug": s[0], "title": s[1]} for s in oas_dm + oas_mg + oas_bhn]
write_file(PEOPLE_DIR / "liam-gallagher.md", person("liam-gallagher", "Liam Gallagher",
    [{"slug": "oasis", "role": "Vocals"}], []))
write_file(PEOPLE_DIR / "noel-gallagher.md", person("noel-gallagher", "Noel Gallagher",
    [{"slug": "oasis", "role": "Guitar/Vocals"}],
    [{"slug": s["slug"], "title": s["title"], "credit": "Writer"} for s in oas_all]))
write_file(PEOPLE_DIR / "paul-arthurs.md", person("paul-arthurs", "Paul Arthurs",
    [{"slug": "oasis", "role": "Guitar"}], []))
write_file(PEOPLE_DIR / "paul-mcguigan.md", person("paul-mcguigan", "Paul McGuigan",
    [{"slug": "oasis", "role": "Bass"}], []))
write_file(PEOPLE_DIR / "tony-mccarroll.md", person("tony-mccarroll", "Tony McCarroll",
    [{"slug": "oasis", "role": "Drums"}], []))
write_file(PEOPLE_DIR / "alan-white-oasis.md", person("alan-white-oasis", "Alan White",
    [{"slug": "oasis", "role": "Drums"}], []))
write_file(PEOPLE_DIR / "owen-morris.md", person("owen-morris", "Owen Morris", [],
    [{"slug": s["slug"], "title": s["title"], "credit": "Producer"} for s in oas_all]))


# ============================================================
# 7. Blur
# ============================================================
print("\n=== Blur ===")
write_file(ARTISTS_DIR / "blur.md", artist(
    "blur", "Blur", "Group",
    ["Britpop", "Alternative Rock"], "Alternative Rock", 1988,
    [{"slug": "damon-albarn", "role": "Vocals"},
     {"slug": "graham-coxon", "role": "Guitar"},
     {"slug": "alex-james", "role": "Bass"},
     {"slug": "dave-rowntree", "role": "Drums"}],
    [{"slug": "leisure-blur", "title": "Leisure", "year": 1991},
     {"slug": "modern-life-blur", "title": "Modern Life Is Rubbish", "year": 1993},
     {"slug": "parklife-blur", "title": "Parklife", "year": 1994},
     {"slug": "great-escape-blur", "title": "The Great Escape", "year": 1995},
     {"slug": "blur-self-titled", "title": "Blur", "year": 1997},
     {"slug": "thirteen-blur", "title": "13", "year": 1999},
     {"slug": "think-tank-blur", "title": "Think Tank", "year": 2003},
     {"slug": "magic-whip-blur", "title": "The Magic Whip", "year": 2015}]
))

blur_albums = [
    ("leisure-blur", "Leisure", 1991, "stephen-street", [("for-tomorrow-blur", "For Tomorrow")]),
    ("modern-life-blur", "Modern Life Is Rubbish", 1993, "stephen-street", [("girls-and-boys-blur", "Girls and Boys")]),
    ("parklife-blur", "Parklife", 1994, "stephen-street",
     [("parklife-blur-s", "Parklife"), ("end-of-a-century-blur", "End of a Century"), ("charmless-man-blur", "Charmless Man")]),
    ("great-escape-blur", "The Great Escape", 1995, "stephen-street",
     [("country-house-blur", "Country House"), ("the-universal-blur", "The Universal")]),
    ("blur-self-titled", "Blur", 1997, "stephen-street",
     [("song-2-blur", "Song 2"), ("beetlebum-blur", "Beetlebum")]),
    ("thirteen-blur", "13", 1999, "william-orbit",
     [("tender-blur", "Tender"), ("coffee-and-tv-blur", "Coffee and TV")]),
    ("think-tank-blur", "Think Tank", 2003, "norman-cook", []),
    ("magic-whip-blur", "The Magic Whip", 2015, "stephen-street", []),
]

blur_all_songs = []
for alb_slug, alb_title, alb_year, prod, songs_list in blur_albums:
    song_dicts = [{"slug": s[0], "title": s[1]} for s in songs_list]
    write_file(ALBUMS_DIR / f"{alb_slug}.md", album(alb_slug, alb_title, "blur", alb_year, prod, song_dicts))
    for s in songs_list:
        write_file(SONGS_DIR / f"{s[0]}.md", song(s[0], s[1], "blur", alb_slug, alb_year,
            [{"person_slug": "damon-albarn", "role": "Writer"}, {"person_slug": prod, "role": "Producer"}]))
        blur_all_songs.append({"slug": s[0], "title": s[1]})

write_file(PEOPLE_DIR / "damon-albarn.md", person("damon-albarn", "Damon Albarn",
    [{"slug": "blur", "role": "Vocals"}],
    [{"slug": s["slug"], "title": s["title"], "credit": "Writer"} for s in blur_all_songs]))
write_file(PEOPLE_DIR / "graham-coxon.md", person("graham-coxon", "Graham Coxon",
    [{"slug": "blur", "role": "Guitar"}], []))
write_file(PEOPLE_DIR / "alex-james.md", person("alex-james", "Alex James",
    [{"slug": "blur", "role": "Bass"}], []))
write_file(PEOPLE_DIR / "dave-rowntree.md", person("dave-rowntree", "Dave Rowntree",
    [{"slug": "blur", "role": "Drums"}], []))
write_file(PEOPLE_DIR / "norman-cook.md", person("norman-cook", "Norman Cook", [], []))


# ============================================================
# 8. Pulp
# ============================================================
print("\n=== Pulp ===")
write_file(ARTISTS_DIR / "pulp.md", artist(
    "pulp", "Pulp", "Group",
    ["Britpop", "Indie Rock"], "Alternative Rock", 1978,
    [{"slug": "jarvis-cocker", "role": "Vocals"},
     {"slug": "russell-senior", "role": "Guitar"},
     {"slug": "nick-banks", "role": "Drums"},
     {"slug": "candida-doyle", "role": "Keyboards"},
     {"slug": "steve-mackey", "role": "Bass"},
     {"slug": "mark-webber", "role": "Guitar"}],
    [{"slug": "his-n-hers-pulp", "title": "His 'n' Hers", "year": 1994},
     {"slug": "different-class-pulp", "title": "Different Class", "year": 1995},
     {"slug": "this-is-hardcore-pulp", "title": "This Is Hardcore", "year": 1998},
     {"slug": "we-love-life-pulp", "title": "We Love Life", "year": 2001}]
))

pulp_albums = [
    ("his-n-hers-pulp", "His 'n' Hers", 1994, "ed-buller",
     [("babies-pulp", "Babies"), ("lipgloss-pulp", "Lipgloss"), ("do-you-remember-pulp", "Do You Remember the First Time?")]),
    ("different-class-pulp", "Different Class", 1995, "ed-buller",
     [("common-people-pulp", "Common People"), ("disco-2000-pulp", "Disco 2000"),
      ("mis-shapes-pulp", "Mis-Shapes"), ("sorted-for-es-and-wizz-pulp", "Sorted for E's and Wizz")]),
    ("this-is-hardcore-pulp", "This Is Hardcore", 1998, "chris-thomas-pulp",
     [("help-the-aged-pulp", "Help the Aged")]),
    ("we-love-life-pulp", "We Love Life", 2001, "ed-buller", []),
]

pulp_all_songs = []
pulp_ed_songs = []
pulp_ct_songs = []
for alb_slug, alb_title, alb_year, prod, songs_list in pulp_albums:
    song_dicts = [{"slug": s[0], "title": s[1]} for s in songs_list]
    write_file(ALBUMS_DIR / f"{alb_slug}.md", album(alb_slug, alb_title, "pulp", alb_year, prod, song_dicts))
    for s in songs_list:
        write_file(SONGS_DIR / f"{s[0]}.md", song(s[0], s[1], "pulp", alb_slug, alb_year,
            [{"person_slug": "jarvis-cocker", "role": "Writer"}, {"person_slug": prod, "role": "Producer"}]))
        pulp_all_songs.append({"slug": s[0], "title": s[1]})
        if prod == "ed-buller":
            pulp_ed_songs.append({"slug": s[0], "title": s[1]})
        else:
            pulp_ct_songs.append({"slug": s[0], "title": s[1]})

write_file(PEOPLE_DIR / "jarvis-cocker.md", person("jarvis-cocker", "Jarvis Cocker",
    [{"slug": "pulp", "role": "Vocals"}],
    [{"slug": s["slug"], "title": s["title"], "credit": "Writer"} for s in pulp_all_songs]))
write_file(PEOPLE_DIR / "russell-senior.md", person("russell-senior", "Russell Senior",
    [{"slug": "pulp", "role": "Guitar"}], []))
write_file(PEOPLE_DIR / "nick-banks.md", person("nick-banks", "Nick Banks",
    [{"slug": "pulp", "role": "Drums"}], []))
write_file(PEOPLE_DIR / "candida-doyle.md", person("candida-doyle", "Candida Doyle",
    [{"slug": "pulp", "role": "Keyboards"}], []))
write_file(PEOPLE_DIR / "steve-mackey.md", person("steve-mackey", "Steve Mackey",
    [{"slug": "pulp", "role": "Bass"}], []))
write_file(PEOPLE_DIR / "mark-webber.md", person("mark-webber", "Mark Webber",
    [{"slug": "pulp", "role": "Guitar"}], []))
write_file(PEOPLE_DIR / "ed-buller.md", person("ed-buller", "Ed Buller", [],
    [{"slug": s["slug"], "title": s["title"], "credit": "Producer"} for s in pulp_ed_songs]))
write_file(PEOPLE_DIR / "chris-thomas-pulp.md", person("chris-thomas-pulp", "Chris Thomas", [],
    [{"slug": s["slug"], "title": s["title"], "credit": "Producer"} for s in pulp_ct_songs]))


# ============================================================
# 9. The Cranberries
# ============================================================
print("\n=== The Cranberries ===")
write_file(ARTISTS_DIR / "the-cranberries.md", artist(
    "the-cranberries", "The Cranberries", "Group",
    ["Alternative Rock", "Indie Rock"], "Alternative Rock", 1989,
    [{"slug": "dolores-oriordan", "role": "Vocals"},
     {"slug": "noel-hogan", "role": "Guitar"},
     {"slug": "mike-hogan", "role": "Bass"},
     {"slug": "fergal-lawler", "role": "Drums"}],
    [{"slug": "everybody-else-cranberries", "title": "Everybody Else Is Doing It, So Why Can't We?", "year": 1993},
     {"slug": "no-need-to-argue-cranberries", "title": "No Need to Argue", "year": 1994},
     {"slug": "faithful-departed-cranberries", "title": "To the Faithful Departed", "year": 1996},
     {"slug": "bury-the-hatchet-cranberries", "title": "Bury the Hatchet", "year": 1999}]
))

cran_albums = [
    ("everybody-else-cranberries", "Everybody Else Is Doing It, So Why Can't We?", 1993, "stephen-street",
     [("linger-cranberries", "Linger"), ("dreams-cranberries", "Dreams")]),
    ("no-need-to-argue-cranberries", "No Need to Argue", 1994, "stephen-street",
     [("zombie-cranberries", "Zombie"), ("ode-to-my-family-cranberries", "Ode to My Family"),
      ("ridiculous-thoughts-cranberries", "Ridiculous Thoughts")]),
    ("faithful-departed-cranberries", "To the Faithful Departed", 1996, "stephen-street",
     [("salvation-cranberries", "Salvation"), ("when-youre-gone-cranberries", "When You're Gone")]),
    ("bury-the-hatchet-cranberries", "Bury the Hatchet", 1999, "stephen-street",
     [("animal-instinct-cranberries", "Animal Instinct")]),
]

cran_all_songs = []
for alb_slug, alb_title, alb_year, prod, songs_list in cran_albums:
    song_dicts = [{"slug": s[0], "title": s[1]} for s in songs_list]
    write_file(ALBUMS_DIR / f"{alb_slug}.md", album(alb_slug, alb_title, "the-cranberries", alb_year, prod, song_dicts))
    for s in songs_list:
        write_file(SONGS_DIR / f"{s[0]}.md", song(s[0], s[1], "the-cranberries", alb_slug, alb_year,
            [{"person_slug": "dolores-oriordan", "role": "Writer"}, {"person_slug": prod, "role": "Producer"}]))
        cran_all_songs.append({"slug": s[0], "title": s[1]})

write_file(PEOPLE_DIR / "dolores-oriordan.md", person("dolores-oriordan", "Dolores O'Riordan",
    [{"slug": "the-cranberries", "role": "Vocals"}],
    [{"slug": s["slug"], "title": s["title"], "credit": "Writer"} for s in cran_all_songs]))
write_file(PEOPLE_DIR / "noel-hogan.md", person("noel-hogan", "Noel Hogan",
    [{"slug": "the-cranberries", "role": "Guitar"}], []))
write_file(PEOPLE_DIR / "mike-hogan.md", person("mike-hogan", "Mike Hogan",
    [{"slug": "the-cranberries", "role": "Bass"}], []))
write_file(PEOPLE_DIR / "fergal-lawler.md", person("fergal-lawler", "Fergal Lawler",
    [{"slug": "the-cranberries", "role": "Drums"}], []))


# ============================================================
# 10. PJ Harvey
# ============================================================
print("\n=== PJ Harvey ===")
write_file(ARTISTS_DIR / "pj-harvey.md", artist(
    "pj-harvey", "PJ Harvey", "Solo",
    ["Alternative Rock", "Art Rock"], "Alternative Rock", 1991,
    [{"slug": "polly-jean-harvey", "role": "Vocals/Guitar"}],
    [{"slug": "dry-pjh", "title": "Dry", "year": 1992},
     {"slug": "rid-of-me-pjh", "title": "Rid of Me", "year": 1993},
     {"slug": "to-bring-you-my-love-pjh", "title": "To Bring You My Love", "year": 1995},
     {"slug": "is-this-desire-pjh", "title": "Is This Desire?", "year": 1998},
     {"slug": "stories-from-the-city-pjh", "title": "Stories from the City, Stories from the Sea", "year": 2000},
     {"slug": "uh-huh-her-pjh", "title": "Uh Huh Her", "year": 2004},
     {"slug": "white-chalk-pjh", "title": "White Chalk", "year": 2007},
     {"slug": "let-england-shake-pjh", "title": "Let England Shake", "year": 2011},
     {"slug": "hope-six-pjh", "title": "The Hope Six Demolition Project", "year": 2016}]
))

pjh_albums = [
    ("dry-pjh", "Dry", 1992, "john-parish", [("sheela-na-gig-pjh", "Sheela-Na-Gig")]),
    ("rid-of-me-pjh", "Rid of Me", 1993, "steve-albini", [("fifty-ft-queenie-pjh", "50ft Queenie")]),
    ("to-bring-you-my-love-pjh", "To Bring You My Love", 1995, "flood-producer",
     [("down-by-the-water-pjh", "Down by the Water"), ("cmon-billy-pjh", "C'mon Billy"),
      ("send-his-love-to-me-pjh", "Send His Love to Me")]),
    ("is-this-desire-pjh", "Is This Desire?", 1998, "flood-producer", []),
    ("stories-from-the-city-pjh", "Stories from the City, Stories from the Sea", 2000, "flood-producer", []),
    ("uh-huh-her-pjh", "Uh Huh Her", 2004, "polly-jean-harvey", []),
    ("white-chalk-pjh", "White Chalk", 2007, "john-parish", []),
    ("let-england-shake-pjh", "Let England Shake", 2011, "john-parish",
     [("words-that-maketh-murder-pjh", "The Words That Maketh Murder"),
      ("let-england-shake-pjh-s", "Let England Shake")]),
    ("hope-six-pjh", "The Hope Six Demolition Project", 2016, "john-parish", []),
]

pjh_all_songs = []
pjh_parish_songs = []
for alb_slug, alb_title, alb_year, prod, songs_list in pjh_albums:
    song_dicts = [{"slug": s[0], "title": s[1]} for s in songs_list]
    write_file(ALBUMS_DIR / f"{alb_slug}.md", album(alb_slug, alb_title, "pj-harvey", alb_year, prod, song_dicts))
    for s in songs_list:
        write_file(SONGS_DIR / f"{s[0]}.md", song(s[0], s[1], "pj-harvey", alb_slug, alb_year,
            [{"person_slug": "polly-jean-harvey", "role": "Writer"}, {"person_slug": prod, "role": "Producer"}]))
        pjh_all_songs.append({"slug": s[0], "title": s[1]})
        if prod == "john-parish":
            pjh_parish_songs.append({"slug": s[0], "title": s[1]})

write_file(PEOPLE_DIR / "polly-jean-harvey.md", person("polly-jean-harvey", "PJ Harvey",
    [{"slug": "pj-harvey", "role": "Vocals/Guitar"}],
    [{"slug": s["slug"], "title": s["title"], "credit": "Writer"} for s in pjh_all_songs]))
write_file(PEOPLE_DIR / "john-parish.md", person("john-parish", "John Parish", [],
    [{"slug": s["slug"], "title": s["title"], "credit": "Producer"} for s in pjh_parish_songs]))


# ============================================================
# 11. Tori Amos
# ============================================================
print("\n=== Tori Amos ===")
write_file(ARTISTS_DIR / "tori-amos.md", artist(
    "tori-amos", "Tori Amos", "Solo",
    ["Alternative Rock", "Art Pop"], "Alternative Rock", 1988,
    [{"slug": "tori-amos-person", "role": "Vocals/Piano"}],
    [{"slug": "little-earthquakes-ta", "title": "Little Earthquakes", "year": 1992},
     {"slug": "under-the-pink-ta", "title": "Under the Pink", "year": 1994},
     {"slug": "boys-for-pele-ta", "title": "Boys for Pele", "year": 1996},
     {"slug": "from-the-choirgirl-hotel-ta", "title": "From the Choirgirl Hotel", "year": 1998},
     {"slug": "to-venus-and-back-ta", "title": "To Venus and Back", "year": 1999},
     {"slug": "strange-little-girls-ta", "title": "Strange Little Girls", "year": 2001},
     {"slug": "scarlets-walk-ta", "title": "Scarlet's Walk", "year": 2002}]
))

ta_albums = [
    ("little-earthquakes-ta", "Little Earthquakes", 1992, "eric-rosse",
     [("crucify-ta", "Crucify"), ("silent-all-these-years-ta", "Silent All These Years"), ("winter-ta", "Winter")]),
    ("under-the-pink-ta", "Under the Pink", 1994, "tori-amos-person",
     [("god-ta", "God"), ("cornflake-girl-ta", "Cornflake Girl")]),
    ("boys-for-pele-ta", "Boys for Pele", 1996, "tori-amos-person",
     [("caught-a-lite-sneeze-ta", "Caught a Lite Sneeze"), ("professional-widow-ta", "Professional Widow")]),
    ("from-the-choirgirl-hotel-ta", "From the Choirgirl Hotel", 1998, "tori-amos-person",
     [("spark-ta", "Spark")]),
    ("to-venus-and-back-ta", "To Venus and Back", 1999, "tori-amos-person",
     [("thousand-oceans-ta", "1000 Oceans")]),
    ("strange-little-girls-ta", "Strange Little Girls", 2001, "tori-amos-person", []),
    ("scarlets-walk-ta", "Scarlet's Walk", 2002, "tori-amos-person", []),
]

ta_all_songs = []
ta_rosse_songs = []
for alb_slug, alb_title, alb_year, prod, songs_list in ta_albums:
    song_dicts = [{"slug": s[0], "title": s[1]} for s in songs_list]
    write_file(ALBUMS_DIR / f"{alb_slug}.md", album(alb_slug, alb_title, "tori-amos", alb_year, prod, song_dicts))
    for s in songs_list:
        write_file(SONGS_DIR / f"{s[0]}.md", song(s[0], s[1], "tori-amos", alb_slug, alb_year,
            [{"person_slug": "tori-amos-person", "role": "Writer"}, {"person_slug": prod, "role": "Producer"}]))
        ta_all_songs.append({"slug": s[0], "title": s[1]})
        if prod == "eric-rosse":
            ta_rosse_songs.append({"slug": s[0], "title": s[1]})

write_file(PEOPLE_DIR / "tori-amos-person.md", person("tori-amos-person", "Tori Amos",
    [{"slug": "tori-amos", "role": "Vocals/Piano"}],
    [{"slug": s["slug"], "title": s["title"], "credit": "Writer"} for s in ta_all_songs]))
write_file(PEOPLE_DIR / "eric-rosse.md", person("eric-rosse", "Eric Rosse", [],
    [{"slug": s["slug"], "title": s["title"], "credit": "Producer"} for s in ta_rosse_songs]))


# ============================================================
# 12. Beck
# ============================================================
print("\n=== Beck ===")
write_file(ARTISTS_DIR / "beck.md", artist(
    "beck", "Beck", "Solo",
    ["Alternative Rock", "Lo-Fi"], "Los Angeles", 1989,
    [{"slug": "beck-person", "role": "Vocals/Guitar"}],
    [{"slug": "mellow-gold-beck", "title": "Mellow Gold", "year": 1994},
     {"slug": "odelay-beck", "title": "Odelay", "year": 1996},
     {"slug": "mutations-beck", "title": "Mutations", "year": 1998},
     {"slug": "midnite-vultures-beck", "title": "Midnite Vultures", "year": 1999},
     {"slug": "sea-change-beck", "title": "Sea Change", "year": 2002},
     {"slug": "guero-beck", "title": "Guero", "year": 2005},
     {"slug": "modern-guilt-beck", "title": "Modern Guilt", "year": 2008},
     {"slug": "morning-phase-beck", "title": "Morning Phase", "year": 2014}]
))

beck_albums = [
    ("mellow-gold-beck", "Mellow Gold", 1994, "the-dust-brothers",
     [("loser-beck", "Loser"), ("hotwax-beck", "Hotwax")]),
    ("odelay-beck", "Odelay", 1996, "the-dust-brothers",
     [("where-its-at-beck", "Where It's At"), ("devils-haircut-beck", "Devils Haircut"),
      ("new-pollution-beck", "The New Pollution")]),
    ("mutations-beck", "Mutations", 1998, "nigel-godrich", []),
    ("midnite-vultures-beck", "Midnite Vultures", 1999, "beck-person",
     [("debra-beck", "Debra"), ("sexx-laws-beck", "Sexx Laws")]),
    ("sea-change-beck", "Sea Change", 2002, "nigel-godrich",
     [("lost-cause-beck", "Lost Cause")]),
    ("guero-beck", "Guero", 2005, "the-dust-brothers",
     [("e-pro-beck", "E-Pro"), ("que-onda-guero-beck", "Que Onda Guero")]),
    ("modern-guilt-beck", "Modern Guilt", 2008, "danger-mouse-bk", []),
    ("morning-phase-beck", "Morning Phase", 2014, "beck-person", []),
]

beck_all_songs = []
beck_dust_songs = []
for alb_slug, alb_title, alb_year, prod, songs_list in beck_albums:
    song_dicts = [{"slug": s[0], "title": s[1]} for s in songs_list]
    write_file(ALBUMS_DIR / f"{alb_slug}.md", album(alb_slug, alb_title, "beck", alb_year, prod, song_dicts))
    for s in songs_list:
        write_file(SONGS_DIR / f"{s[0]}.md", song(s[0], s[1], "beck", alb_slug, alb_year,
            [{"person_slug": "beck-person", "role": "Writer"}, {"person_slug": prod, "role": "Producer"}]))
        beck_all_songs.append({"slug": s[0], "title": s[1]})
        if prod == "the-dust-brothers":
            beck_dust_songs.append({"slug": s[0], "title": s[1]})

write_file(PEOPLE_DIR / "beck-person.md", person("beck-person", "Beck",
    [{"slug": "beck", "role": "Vocals/Guitar"}],
    [{"slug": s["slug"], "title": s["title"], "credit": "Writer"} for s in beck_all_songs]))
write_file(PEOPLE_DIR / "the-dust-brothers.md", person("the-dust-brothers", "The Dust Brothers", [],
    [{"slug": s["slug"], "title": s["title"], "credit": "Producer"} for s in beck_dust_songs]))


# ============================================================
# 13. Sheryl Crow
# ============================================================
print("\n=== Sheryl Crow ===")
write_file(ARTISTS_DIR / "sheryl-crow.md", artist(
    "sheryl-crow", "Sheryl Crow", "Solo",
    ["Rock", "Alternative Rock"], "Rock", 1991,
    [{"slug": "sheryl-crow-person", "role": "Vocals/Guitar"}],
    [{"slug": "tuesday-night-music-club-sc", "title": "Tuesday Night Music Club", "year": 1993},
     {"slug": "sheryl-crow-album", "title": "Sheryl Crow", "year": 1996},
     {"slug": "globe-sessions-sc", "title": "The Globe Sessions", "year": 1998},
     {"slug": "cmon-cmon-sc", "title": "C'mon, C'mon", "year": 2002},
     {"slug": "wildflower-sc", "title": "Wildflower", "year": 2005}]
))

sc_albums = [
    ("tuesday-night-music-club-sc", "Tuesday Night Music Club", 1993, "bill-bottrell",
     [("all-i-wanna-do-sc", "All I Wanna Do"), ("everyday-is-a-winding-road-sc", "Everyday Is a Winding Road"),
      ("strong-enough-sc", "Strong Enough")]),
    ("sheryl-crow-album", "Sheryl Crow", 1996, "sheryl-crow-person",
     [("if-it-makes-you-happy-sc", "If It Makes You Happy"), ("my-favorite-mistake-sc", "My Favorite Mistake")]),
    ("globe-sessions-sc", "The Globe Sessions", 1998, "sheryl-crow-person", []),
    ("cmon-cmon-sc", "C'mon, C'mon", 2002, "sheryl-crow-person",
     [("soak-up-the-sun-sc", "Soak Up the Sun")]),
    ("wildflower-sc", "Wildflower", 2005, "sheryl-crow-person", []),
]

sc_all_songs = []
sc_bottrell_songs = []
for alb_slug, alb_title, alb_year, prod, songs_list in sc_albums:
    song_dicts = [{"slug": s[0], "title": s[1]} for s in songs_list]
    write_file(ALBUMS_DIR / f"{alb_slug}.md", album(alb_slug, alb_title, "sheryl-crow", alb_year, prod, song_dicts))
    for s in songs_list:
        write_file(SONGS_DIR / f"{s[0]}.md", song(s[0], s[1], "sheryl-crow", alb_slug, alb_year,
            [{"person_slug": "sheryl-crow-person", "role": "Writer"}, {"person_slug": prod, "role": "Producer"}]))
        sc_all_songs.append({"slug": s[0], "title": s[1]})
        if prod == "bill-bottrell":
            sc_bottrell_songs.append({"slug": s[0], "title": s[1]})

write_file(PEOPLE_DIR / "sheryl-crow-person.md", person("sheryl-crow-person", "Sheryl Crow",
    [{"slug": "sheryl-crow", "role": "Vocals/Guitar"}],
    [{"slug": s["slug"], "title": s["title"], "credit": "Writer"} for s in sc_all_songs]))
write_file(PEOPLE_DIR / "bill-bottrell.md", person("bill-bottrell", "Bill Bottrell", [],
    [{"slug": s["slug"], "title": s["title"], "credit": "Producer"} for s in sc_bottrell_songs]))


# ============================================================
# 14. No Doubt
# ============================================================
print("\n=== No Doubt ===")
write_file(ARTISTS_DIR / "no-doubt.md", artist(
    "no-doubt", "No Doubt", "Group",
    ["Alternative Rock", "Ska Punk"], "Alternative Rock", 1986,
    [{"slug": "gwen-stefani", "role": "Vocals"},
     {"slug": "tom-dumont", "role": "Guitar"},
     {"slug": "tony-kanal", "role": "Bass"},
     {"slug": "adrian-young-nd", "role": "Drums"}],
    [{"slug": "no-doubt-debut", "title": "No Doubt", "year": 1992},
     {"slug": "beacon-street-nd", "title": "The Beacon Street Collection", "year": 1995},
     {"slug": "tragic-kingdom-nd", "title": "Tragic Kingdom", "year": 1995},
     {"slug": "return-of-saturn-nd", "title": "Return of Saturn", "year": 2000},
     {"slug": "rock-steady-nd", "title": "Rock Steady", "year": 2001}]
))

nd_albums = [
    ("no-doubt-debut", "No Doubt", 1992, "eric-stefani", []),
    ("beacon-street-nd", "The Beacon Street Collection", 1995, "gwen-stefani", []),
    ("tragic-kingdom-nd", "Tragic Kingdom", 1995, "matthew-wilder",
     [("dont-speak-nd", "Don't Speak"), ("just-a-girl-nd", "Just a Girl"), ("spiderwebs-nd", "Spiderwebs"),
      ("sunday-morning-nd", "Sunday Morning"), ("simple-kind-of-life-nd", "Simple Kind of Life")]),
    ("return-of-saturn-nd", "Return of Saturn", 2000, "matthew-wilder",
     [("running-nd", "Running")]),
    ("rock-steady-nd", "Rock Steady", 2001, "gwen-stefani",
     [("hella-good-nd", "Hella Good"), ("hey-baby-nd", "Hey Baby")]),
]

nd_all_songs = []
nd_wilder_songs = []
for alb_slug, alb_title, alb_year, prod, songs_list in nd_albums:
    song_dicts = [{"slug": s[0], "title": s[1]} for s in songs_list]
    write_file(ALBUMS_DIR / f"{alb_slug}.md", album(alb_slug, alb_title, "no-doubt", alb_year, prod, song_dicts))
    for s in songs_list:
        write_file(SONGS_DIR / f"{s[0]}.md", song(s[0], s[1], "no-doubt", alb_slug, alb_year,
            [{"person_slug": "gwen-stefani", "role": "Writer"}, {"person_slug": prod, "role": "Producer"}]))
        nd_all_songs.append({"slug": s[0], "title": s[1]})
        if prod == "matthew-wilder":
            nd_wilder_songs.append({"slug": s[0], "title": s[1]})

write_file(PEOPLE_DIR / "gwen-stefani.md", person("gwen-stefani", "Gwen Stefani",
    [{"slug": "no-doubt", "role": "Vocals"}],
    [{"slug": s["slug"], "title": s["title"], "credit": "Writer"} for s in nd_all_songs]))
write_file(PEOPLE_DIR / "tom-dumont.md", person("tom-dumont", "Tom Dumont",
    [{"slug": "no-doubt", "role": "Guitar"}], []))
write_file(PEOPLE_DIR / "tony-kanal.md", person("tony-kanal", "Tony Kanal",
    [{"slug": "no-doubt", "role": "Bass"}], []))
write_file(PEOPLE_DIR / "adrian-young-nd.md", person("adrian-young-nd", "Adrian Young",
    [{"slug": "no-doubt", "role": "Drums"}], []))
write_file(PEOPLE_DIR / "matthew-wilder.md", person("matthew-wilder", "Matthew Wilder", [],
    [{"slug": s["slug"], "title": s["title"], "credit": "Producer"} for s in nd_wilder_songs]))
write_file(PEOPLE_DIR / "eric-stefani.md", person("eric-stefani", "Eric Stefani",
    [{"slug": "no-doubt", "role": "Keyboards"}], []))


# ============================================================
# 15. Dave Matthews Band
# ============================================================
print("\n=== Dave Matthews Band ===")
write_file(ARTISTS_DIR / "dave-matthews-band.md", artist(
    "dave-matthews-band", "Dave Matthews Band", "Group",
    ["Rock", "Jam Rock"], "Rock", 1991,
    [{"slug": "dave-matthews", "role": "Vocals/Guitar"},
     {"slug": "carter-beauford", "role": "Drums"},
     {"slug": "stefan-lessard", "role": "Bass"},
     {"slug": "boyd-tinsley", "role": "Violin"},
     {"slug": "leroi-moore", "role": "Saxophone"}],
    [{"slug": "remember-two-things-dmb", "title": "Remember Two Things", "year": 1993},
     {"slug": "under-the-table-dmb", "title": "Under the Table and Dreaming", "year": 1994},
     {"slug": "crash-dmb", "title": "Crash", "year": 1996},
     {"slug": "before-these-crowded-streets-dmb", "title": "Before These Crowded Streets", "year": 1998},
     {"slug": "everyday-dmb", "title": "Everyday", "year": 2001},
     {"slug": "busted-stuff-dmb", "title": "Busted Stuff", "year": 2002}]
))

dmb_albums = [
    ("remember-two-things-dmb", "Remember Two Things", 1993, "john-alagia", []),
    ("under-the-table-dmb", "Under the Table and Dreaming", 1994, "steve-lillywhite",
     [("what-would-you-say-dmb", "What Would You Say"), ("ants-marching-dmb", "Ants Marching"),
      ("dancing-nancies-dmb", "Dancing Nancies"), ("satellite-dmb", "Satellite")]),
    ("crash-dmb", "Crash", 1996, "steve-lillywhite",
     [("crash-into-me-dmb", "Crash Into Me"), ("too-much-dmb", "Too Much"), ("so-much-to-say-dmb", "So Much to Say")]),
    ("before-these-crowded-streets-dmb", "Before These Crowded Streets", 1998, "steve-lillywhite",
     [("forty-one-dmb", "#41")]),
    ("everyday-dmb", "Everyday", 2001, "glen-ballard",
     [("space-between-dmb", "The Space Between"), ("everyday-dmb-s", "Everyday")]),
    ("busted-stuff-dmb", "Busted Stuff", 2002, "john-alagia", []),
]

dmb_all_songs = []
dmb_ballard_songs = []
for alb_slug, alb_title, alb_year, prod, songs_list in dmb_albums:
    song_dicts = [{"slug": s[0], "title": s[1]} for s in songs_list]
    write_file(ALBUMS_DIR / f"{alb_slug}.md", album(alb_slug, alb_title, "dave-matthews-band", alb_year, prod, song_dicts))
    for s in songs_list:
        write_file(SONGS_DIR / f"{s[0]}.md", song(s[0], s[1], "dave-matthews-band", alb_slug, alb_year,
            [{"person_slug": "dave-matthews", "role": "Writer"}, {"person_slug": prod, "role": "Producer"}]))
        dmb_all_songs.append({"slug": s[0], "title": s[1]})
        if prod == "glen-ballard":
            dmb_ballard_songs.append({"slug": s[0], "title": s[1]})

write_file(PEOPLE_DIR / "dave-matthews.md", person("dave-matthews", "Dave Matthews",
    [{"slug": "dave-matthews-band", "role": "Vocals/Guitar"}],
    [{"slug": s["slug"], "title": s["title"], "credit": "Writer"} for s in dmb_all_songs]))
write_file(PEOPLE_DIR / "carter-beauford.md", person("carter-beauford", "Carter Beauford",
    [{"slug": "dave-matthews-band", "role": "Drums"}], []))
write_file(PEOPLE_DIR / "stefan-lessard.md", person("stefan-lessard", "Stefan Lessard",
    [{"slug": "dave-matthews-band", "role": "Bass"}], []))
write_file(PEOPLE_DIR / "boyd-tinsley.md", person("boyd-tinsley", "Boyd Tinsley",
    [{"slug": "dave-matthews-band", "role": "Violin"}], []))
write_file(PEOPLE_DIR / "leroi-moore.md", person("leroi-moore", "LeRoi Moore",
    [{"slug": "dave-matthews-band", "role": "Saxophone"}], []))
write_file(PEOPLE_DIR / "john-alagia.md", person("john-alagia", "John Alagia", [], []))
write_file(PEOPLE_DIR / "glen-ballard.md", person("glen-ballard", "Glen Ballard", [],
    [{"slug": s["slug"], "title": s["title"], "credit": "Producer"} for s in dmb_ballard_songs]))
write_file(PEOPLE_DIR / "stephen-harris-dmb.md", person("stephen-harris-dmb", "Stephen Harris", [], []))


# ============================================================
# 16. Counting Crows
# ============================================================
print("\n=== Counting Crows ===")
write_file(ARTISTS_DIR / "counting-crows.md", artist(
    "counting-crows", "Counting Crows", "Group",
    ["Alternative Rock", "Folk Rock"], "San Francisco", 1991,
    [{"slug": "adam-duritz", "role": "Vocals"},
     {"slug": "david-bryson", "role": "Guitar"},
     {"slug": "matt-malley", "role": "Bass"},
     {"slug": "charlie-gillingham", "role": "Keyboards"},
     {"slug": "dan-vickrey", "role": "Guitar"}],
    [{"slug": "august-and-everything-after-cc", "title": "August and Everything After", "year": 1993},
     {"slug": "recovering-the-satellites-cc", "title": "Recovering the Satellites", "year": 1996},
     {"slug": "this-desert-life-cc", "title": "This Desert Life", "year": 1999},
     {"slug": "hard-candy-cc", "title": "Hard Candy", "year": 2003}]
))

cc_albums = [
    ("august-and-everything-after-cc", "August and Everything After", 1993, "t-bone-burnett",
     [("mr-jones-cc", "Mr. Jones"), ("round-here-cc", "Round Here"),
      ("rain-king-cc", "Rain King"), ("anna-begins-cc", "Anna Begins")]),
    ("recovering-the-satellites-cc", "Recovering the Satellites", 1996, "gil-norton",
     [("long-december-cc", "A Long December"), ("hangin-around-cc", "Hangin' Around")]),
    ("this-desert-life-cc", "This Desert Life", 1999, "gil-norton",
     [("colorblind-cc", "Colorblind")]),
    ("hard-candy-cc", "Hard Candy", 2003, "gil-norton", []),
]

cc_all_songs = []
cc_burnett_songs = []
cc_norton_songs = []
for alb_slug, alb_title, alb_year, prod, songs_list in cc_albums:
    song_dicts = [{"slug": s[0], "title": s[1]} for s in songs_list]
    write_file(ALBUMS_DIR / f"{alb_slug}.md", album(alb_slug, alb_title, "counting-crows", alb_year, prod, song_dicts))
    for s in songs_list:
        write_file(SONGS_DIR / f"{s[0]}.md", song(s[0], s[1], "counting-crows", alb_slug, alb_year,
            [{"person_slug": "adam-duritz", "role": "Writer"}, {"person_slug": prod, "role": "Producer"}]))
        cc_all_songs.append({"slug": s[0], "title": s[1]})
        if prod == "t-bone-burnett":
            cc_burnett_songs.append({"slug": s[0], "title": s[1]})
        else:
            cc_norton_songs.append({"slug": s[0], "title": s[1]})

write_file(PEOPLE_DIR / "adam-duritz.md", person("adam-duritz", "Adam Duritz",
    [{"slug": "counting-crows", "role": "Vocals"}],
    [{"slug": s["slug"], "title": s["title"], "credit": "Writer"} for s in cc_all_songs]))
write_file(PEOPLE_DIR / "david-bryson.md", person("david-bryson", "David Bryson",
    [{"slug": "counting-crows", "role": "Guitar"}], []))
write_file(PEOPLE_DIR / "matt-malley.md", person("matt-malley", "Matt Malley",
    [{"slug": "counting-crows", "role": "Bass"}], []))
write_file(PEOPLE_DIR / "charlie-gillingham.md", person("charlie-gillingham", "Charlie Gillingham",
    [{"slug": "counting-crows", "role": "Keyboards"}], []))
write_file(PEOPLE_DIR / "dan-vickrey.md", person("dan-vickrey", "Dan Vickrey",
    [{"slug": "counting-crows", "role": "Guitar"}], []))
write_file(PEOPLE_DIR / "t-bone-burnett.md", person("t-bone-burnett", "T Bone Burnett", [],
    [{"slug": s["slug"], "title": s["title"], "credit": "Producer"} for s in cc_burnett_songs]))
# gil-norton already exists - skip


# ============================================================
# 17. Hole
# ============================================================
print("\n=== Hole ===")
write_file(ARTISTS_DIR / "hole.md", artist(
    "hole", "Hole", "Group",
    ["Alternative Rock", "Grunge"], "Los Angeles", 1989,
    [{"slug": "courtney-love", "role": "Vocals/Guitar"},
     {"slug": "eric-erlandson", "role": "Guitar"},
     {"slug": "melissa-auf-der-maur", "role": "Bass"},
     {"slug": "patty-schemel", "role": "Drums"}],
    [{"slug": "pretty-on-the-inside-hole", "title": "Pretty on the Inside", "year": 1991},
     {"slug": "live-through-this-hole", "title": "Live Through This", "year": 1994},
     {"slug": "celebrity-skin-hole", "title": "Celebrity Skin", "year": 1998}]
))

hole_albums = [
    ("pretty-on-the-inside-hole", "Pretty on the Inside", 1991, "don-fleming", []),
    ("live-through-this-hole", "Live Through This", 1994, "paul-q-kolderie",
     [("violet-hole", "Violet"), ("doll-parts-hole", "Doll Parts"),
      ("miss-world-hole", "Miss World"), ("asking-for-it-hole", "Asking for It")]),
    ("celebrity-skin-hole", "Celebrity Skin", 1998, "michael-beinhorn",
     [("celebrity-skin-hole-s", "Celebrity Skin"), ("malibu-hole", "Malibu"),
      ("boys-on-the-radio-hole", "Boys on the Radio")]),
]

hole_all_songs = []
hole_kolderie_songs = []
for alb_slug, alb_title, alb_year, prod, songs_list in hole_albums:
    song_dicts = [{"slug": s[0], "title": s[1]} for s in songs_list]
    write_file(ALBUMS_DIR / f"{alb_slug}.md", album(alb_slug, alb_title, "hole", alb_year, prod, song_dicts))
    for s in songs_list:
        write_file(SONGS_DIR / f"{s[0]}.md", song(s[0], s[1], "hole", alb_slug, alb_year,
            [{"person_slug": "courtney-love", "role": "Writer"}, {"person_slug": prod, "role": "Producer"}]))
        hole_all_songs.append({"slug": s[0], "title": s[1]})
        if prod == "paul-q-kolderie":
            hole_kolderie_songs.append({"slug": s[0], "title": s[1]})

write_file(PEOPLE_DIR / "courtney-love.md", person("courtney-love", "Courtney Love",
    [{"slug": "hole", "role": "Vocals/Guitar"}],
    [{"slug": s["slug"], "title": s["title"], "credit": "Writer"} for s in hole_all_songs]))
write_file(PEOPLE_DIR / "eric-erlandson.md", person("eric-erlandson", "Eric Erlandson",
    [{"slug": "hole", "role": "Guitar"}], []))
write_file(PEOPLE_DIR / "melissa-auf-der-maur.md", person("melissa-auf-der-maur", "Melissa Auf der Maur",
    [{"slug": "hole", "role": "Bass"}], []))
write_file(PEOPLE_DIR / "patty-schemel.md", person("patty-schemel", "Patty Schemel",
    [{"slug": "hole", "role": "Drums"}], []))
write_file(PEOPLE_DIR / "paul-q-kolderie.md", person("paul-q-kolderie", "Paul Q. Kolderie", [],
    [{"slug": s["slug"], "title": s["title"], "credit": "Producer"} for s in hole_kolderie_songs]))


# ============================================================
# 18. Pavement
# ============================================================
print("\n=== Pavement ===")
write_file(ARTISTS_DIR / "pavement.md", artist(
    "pavement", "Pavement", "Group",
    ["Indie Rock", "Lo-Fi"], "Alternative Rock", 1989,
    [{"slug": "stephen-malkmus", "role": "Vocals/Guitar"},
     {"slug": "scott-kannberg", "role": "Guitar"},
     {"slug": "mark-ibold", "role": "Bass"},
     {"slug": "steve-west", "role": "Drums"},
     {"slug": "bob-nastanovich", "role": "Percussion"}],
    [{"slug": "slanted-and-enchanted-pav", "title": "Slanted and Enchanted", "year": 1992},
     {"slug": "crooked-rain-pav", "title": "Crooked Rain, Crooked Rain", "year": 1994},
     {"slug": "wowee-zowee-pav", "title": "Wowee Zowee", "year": 1995},
     {"slug": "brighten-corners-pav", "title": "Brighten the Corners", "year": 1997},
     {"slug": "terror-twilight-pav", "title": "Terror Twilight", "year": 1999}]
))

pav_albums = [
    ("slanted-and-enchanted-pav", "Slanted and Enchanted", 1992, "stephen-malkmus",
     [("summer-babe-pav", "Summer Babe"), ("silence-kit-pav", "Silence Kit")]),
    ("crooked-rain-pav", "Crooked Rain, Crooked Rain", 1994, "stephen-malkmus",
     [("cut-your-hair-pav", "Cut Your Hair"), ("range-life-pav", "Range Life")]),
    ("wowee-zowee-pav", "Wowee Zowee", 1995, "stephen-malkmus",
     [("here-pav", "Here")]),
    ("brighten-corners-pav", "Brighten the Corners", 1997, "stephen-malkmus",
     [("stereo-pav", "Stereo"), ("spit-on-a-stranger-pav", "Spit on a Stranger")]),
    ("terror-twilight-pav", "Terror Twilight", 1999, "nigel-godrich",
     [("carrot-rope-pav", "Carrot Rope")]),
]

pav_all_songs = []
for alb_slug, alb_title, alb_year, prod, songs_list in pav_albums:
    song_dicts = [{"slug": s[0], "title": s[1]} for s in songs_list]
    write_file(ALBUMS_DIR / f"{alb_slug}.md", album(alb_slug, alb_title, "pavement", alb_year, prod, song_dicts))
    for s in songs_list:
        write_file(SONGS_DIR / f"{s[0]}.md", song(s[0], s[1], "pavement", alb_slug, alb_year,
            [{"person_slug": "stephen-malkmus", "role": "Writer"}, {"person_slug": prod, "role": "Producer"}]))
        pav_all_songs.append({"slug": s[0], "title": s[1]})

write_file(PEOPLE_DIR / "stephen-malkmus.md", person("stephen-malkmus", "Stephen Malkmus",
    [{"slug": "pavement", "role": "Vocals/Guitar"}],
    [{"slug": s["slug"], "title": s["title"], "credit": "Writer"} for s in pav_all_songs]))
write_file(PEOPLE_DIR / "scott-kannberg.md", person("scott-kannberg", "Scott Kannberg",
    [{"slug": "pavement", "role": "Guitar"}], []))
write_file(PEOPLE_DIR / "mark-ibold.md", person("mark-ibold", "Mark Ibold",
    [{"slug": "pavement", "role": "Bass"}], []))
write_file(PEOPLE_DIR / "steve-west.md", person("steve-west", "Steve West",
    [{"slug": "pavement", "role": "Drums"}], []))
write_file(PEOPLE_DIR / "bob-nastanovich.md", person("bob-nastanovich", "Bob Nastanovich",
    [{"slug": "pavement", "role": "Percussion"}], []))


# ============================================================
# 19. Bjork
# ============================================================
print("\n=== Bjork ===")
write_file(ARTISTS_DIR / "bjork.md", artist(
    "bjork", "Bjork", "Solo",
    ["Art Pop", "Electronic"], "Alternative Rock", 1977,
    [{"slug": "bjork-person", "role": "Vocals"}],
    [{"slug": "debut-bjork", "title": "Debut", "year": 1993},
     {"slug": "post-bjork", "title": "Post", "year": 1995},
     {"slug": "homogenic-bjork", "title": "Homogenic", "year": 1997},
     {"slug": "vespertine-bjork", "title": "Vespertine", "year": 2001},
     {"slug": "medulla-bjork", "title": "Medulla", "year": 2004},
     {"slug": "volta-bjork", "title": "Volta", "year": 2007},
     {"slug": "biophilia-bjork", "title": "Biophilia", "year": 2011},
     {"slug": "vulnicura-bjork", "title": "Vulnicura", "year": 2015},
     {"slug": "utopia-bjork", "title": "Utopia", "year": 2017}]
))

bjork_albums = [
    ("debut-bjork", "Debut", 1993, "nellee-hooper",
     [("human-behaviour-bjork", "Human Behaviour"), ("venus-as-a-boy-bjork", "Venus as a Boy")]),
    ("post-bjork", "Post", 1995, "nellee-hooper",
     [("army-of-me-bjork", "Army of Me")]),
    ("homogenic-bjork", "Homogenic", 1997, "mark-bell-bjork",
     [("hyperballad-bjork", "Hyperballad"), ("joga-bjork", "Joga"), ("bachelorette-bjork", "Bachelorette")]),
    ("vespertine-bjork", "Vespertine", 2001, "mark-bell-bjork",
     [("all-is-full-of-love-bjork", "All Is Full of Love"), ("cocoon-bjork", "Cocoon")]),
    ("medulla-bjork", "Medulla", 2004, "bjork-person", []),
    ("volta-bjork", "Volta", 2007, "bjork-person",
     [("declare-independence-bjork", "Declare Independence")]),
    ("biophilia-bjork", "Biophilia", 2011, "bjork-person", []),
    ("vulnicura-bjork", "Vulnicura", 2015, "bjork-person", []),
    ("utopia-bjork", "Utopia", 2017, "bjork-person", []),
]

bjork_all_songs = []
bjork_hooper_songs = []
bjork_bell_songs = []
for alb_slug, alb_title, alb_year, prod, songs_list in bjork_albums:
    song_dicts = [{"slug": s[0], "title": s[1]} for s in songs_list]
    write_file(ALBUMS_DIR / f"{alb_slug}.md", album(alb_slug, alb_title, "bjork", alb_year, prod, song_dicts))
    for s in songs_list:
        write_file(SONGS_DIR / f"{s[0]}.md", song(s[0], s[1], "bjork", alb_slug, alb_year,
            [{"person_slug": "bjork-person", "role": "Writer"}, {"person_slug": prod, "role": "Producer"}]))
        bjork_all_songs.append({"slug": s[0], "title": s[1]})
        if prod == "nellee-hooper":
            bjork_hooper_songs.append({"slug": s[0], "title": s[1]})
        elif prod == "mark-bell-bjork":
            bjork_bell_songs.append({"slug": s[0], "title": s[1]})

write_file(PEOPLE_DIR / "bjork-person.md", person("bjork-person", "Bjork",
    [{"slug": "bjork", "role": "Vocals"}],
    [{"slug": s["slug"], "title": s["title"], "credit": "Writer"} for s in bjork_all_songs]))
write_file(PEOPLE_DIR / "nellee-hooper.md", person("nellee-hooper", "Nellee Hooper", [],
    [{"slug": s["slug"], "title": s["title"], "credit": "Producer"} for s in bjork_hooper_songs]))
write_file(PEOPLE_DIR / "mark-bell-bjork.md", person("mark-bell-bjork", "Mark Bell", [],
    [{"slug": s["slug"], "title": s["title"], "credit": "Producer"} for s in bjork_bell_songs]))


# ============================================================
# 20. Primus
# ============================================================
print("\n=== Primus ===")
write_file(ARTISTS_DIR / "primus.md", artist(
    "primus", "Primus", "Group",
    ["Alternative Metal", "Funk Metal"], "San Francisco", 1984,
    [{"slug": "les-claypool", "role": "Vocals/Bass"},
     {"slug": "larry-lalonde", "role": "Guitar"},
     {"slug": "tim-alexander", "role": "Drums"}],
    [{"slug": "frizzle-fry-primus", "title": "Frizzle Fry", "year": 1990},
     {"slug": "sailing-the-seas-primus", "title": "Sailing the Seas of Cheese", "year": 1991},
     {"slug": "pork-soda-primus", "title": "Pork Soda", "year": 1993},
     {"slug": "tales-from-punchbowl-primus", "title": "Tales from the Punchbowl", "year": 1995},
     {"slug": "brown-album-primus", "title": "The Brown Album", "year": 1997}]
))

primus_albums = [
    ("frizzle-fry-primus", "Frizzle Fry", 1990, "les-claypool",
     [("too-many-puppies-primus", "Too Many Puppies")]),
    ("sailing-the-seas-primus", "Sailing the Seas of Cheese", 1991, "les-claypool",
     [("jerry-was-a-race-car-driver-primus", "Jerry Was a Race Car Driver"),
      ("tommy-the-cat-primus", "Tommy the Cat")]),
    ("pork-soda-primus", "Pork Soda", 1993, "les-claypool",
     [("my-name-is-mud-primus", "My Name Is Mud")]),
    ("tales-from-punchbowl-primus", "Tales from the Punchbowl", 1995, "les-claypool",
     [("wynonas-big-brown-beaver-primus", "Wynona's Big Brown Beaver")]),
    ("brown-album-primus", "The Brown Album", 1997, "les-claypool",
     [("shake-hands-with-beef-primus", "Shake Hands with Beef")]),
]

primus_all_songs = []
for alb_slug, alb_title, alb_year, prod, songs_list in primus_albums:
    song_dicts = [{"slug": s[0], "title": s[1]} for s in songs_list]
    write_file(ALBUMS_DIR / f"{alb_slug}.md", album(alb_slug, alb_title, "primus", alb_year, prod, song_dicts))
    for s in songs_list:
        write_file(SONGS_DIR / f"{s[0]}.md", song(s[0], s[1], "primus", alb_slug, alb_year,
            [{"person_slug": "les-claypool", "role": "Writer"}, {"person_slug": prod, "role": "Producer"}]))
        primus_all_songs.append({"slug": s[0], "title": s[1]})

write_file(PEOPLE_DIR / "les-claypool.md", person("les-claypool", "Les Claypool",
    [{"slug": "primus", "role": "Vocals/Bass"}],
    [{"slug": s["slug"], "title": s["title"], "credit": "Writer"} for s in primus_all_songs]))
write_file(PEOPLE_DIR / "larry-lalonde.md", person("larry-lalonde", "Larry LaLonde",
    [{"slug": "primus", "role": "Guitar"}], []))
write_file(PEOPLE_DIR / "tim-alexander.md", person("tim-alexander", "Tim Alexander",
    [{"slug": "primus", "role": "Drums"}], []))


# ============================================================
# 21. Hootie and the Blowfish
# ============================================================
print("\n=== Hootie and the Blowfish ===")
write_file(ARTISTS_DIR / "hootie-and-the-blowfish.md", artist(
    "hootie-and-the-blowfish", "Hootie and the Blowfish", "Group",
    ["Rock", "Alternative Rock"], "Rock", 1986,
    [{"slug": "darius-rucker", "role": "Vocals"},
     {"slug": "mark-bryan", "role": "Guitar"},
     {"slug": "dean-felber", "role": "Bass"},
     {"slug": "jim-sonefeld", "role": "Drums"}],
    [{"slug": "cracked-rear-view-hootie", "title": "Cracked Rear View", "year": 1994},
     {"slug": "fairweather-johnson-hootie", "title": "Fairweather Johnson", "year": 1996},
     {"slug": "musical-chairs-hootie", "title": "Musical Chairs", "year": 1998}]
))

hootie_albums = [
    ("cracked-rear-view-hootie", "Cracked Rear View", 1994, "don-gehman",
     [("hold-my-hand-hootie", "Hold My Hand"), ("let-her-cry-hootie", "Let Her Cry"),
      ("only-wanna-be-with-you-hootie", "Only Wanna Be with You"), ("time-hootie", "Time")]),
    ("fairweather-johnson-hootie", "Fairweather Johnson", 1996, "don-gehman",
     [("old-man-and-me-hootie", "Old Man and Me")]),
    ("musical-chairs-hootie", "Musical Chairs", 1998, "don-gehman",
     [("tuckers-town-hootie", "Tucker's Town")]),
]

hootie_all_songs = []
for alb_slug, alb_title, alb_year, prod, songs_list in hootie_albums:
    song_dicts = [{"slug": s[0], "title": s[1]} for s in songs_list]
    write_file(ALBUMS_DIR / f"{alb_slug}.md", album(alb_slug, alb_title, "hootie-and-the-blowfish", alb_year, prod, song_dicts))
    for s in songs_list:
        write_file(SONGS_DIR / f"{s[0]}.md", song(s[0], s[1], "hootie-and-the-blowfish", alb_slug, alb_year,
            [{"person_slug": "darius-rucker", "role": "Writer"}, {"person_slug": prod, "role": "Producer"}]))
        hootie_all_songs.append({"slug": s[0], "title": s[1]})

write_file(PEOPLE_DIR / "darius-rucker.md", person("darius-rucker", "Darius Rucker",
    [{"slug": "hootie-and-the-blowfish", "role": "Vocals"}],
    [{"slug": s["slug"], "title": s["title"], "credit": "Writer"} for s in hootie_all_songs]))
write_file(PEOPLE_DIR / "mark-bryan.md", person("mark-bryan", "Mark Bryan",
    [{"slug": "hootie-and-the-blowfish", "role": "Guitar"}], []))
write_file(PEOPLE_DIR / "dean-felber.md", person("dean-felber", "Dean Felber",
    [{"slug": "hootie-and-the-blowfish", "role": "Bass"}], []))
write_file(PEOPLE_DIR / "jim-sonefeld.md", person("jim-sonefeld", "Jim Sonefeld",
    [{"slug": "hootie-and-the-blowfish", "role": "Drums"}], []))
write_file(PEOPLE_DIR / "don-gehman.md", person("don-gehman", "Don Gehman", [],
    [{"slug": s["slug"], "title": s["title"], "credit": "Producer"} for s in hootie_all_songs]))


# ============================================================
# 22. Cake
# ============================================================
print("\n=== Cake ===")
write_file(ARTISTS_DIR / "cake.md", artist(
    "cake", "Cake", "Group",
    ["Alternative Rock", "Indie Rock"], "San Francisco", 1991,
    [{"slug": "john-mccrea", "role": "Vocals/Guitar"},
     {"slug": "vince-di-fiore", "role": "Trumpet"},
     {"slug": "greg-brown-cake", "role": "Guitar"},
     {"slug": "todd-roper", "role": "Drums"}],
    [{"slug": "motorcade-of-generosity-cake", "title": "Motorcade of Generosity", "year": 1994},
     {"slug": "fashion-nugget-cake", "title": "Fashion Nugget", "year": 1996},
     {"slug": "prolonging-the-magic-cake", "title": "Prolonging the Magic", "year": 1998},
     {"slug": "comfort-eagle-cake", "title": "Comfort Eagle", "year": 2001}]
))

cake_albums = [
    ("motorcade-of-generosity-cake", "Motorcade of Generosity", 1994, "john-mccrea", []),
    ("fashion-nugget-cake", "Fashion Nugget", 1996, "john-mccrea",
     [("the-distance-cake", "The Distance"), ("i-will-survive-cake", "I Will Survive"),
      ("sheep-go-to-heaven-cake", "Sheep Go to Heaven")]),
    ("prolonging-the-magic-cake", "Prolonging the Magic", 1998, "john-mccrea",
     [("never-there-cake", "Never There")]),
    ("comfort-eagle-cake", "Comfort Eagle", 2001, "john-mccrea",
     [("short-skirt-long-jacket-cake", "Short Skirt Long Jacket"),
      ("comfort-eagle-cake-s", "Comfort Eagle")]),
]

cake_all_songs = []
for alb_slug, alb_title, alb_year, prod, songs_list in cake_albums:
    song_dicts = [{"slug": s[0], "title": s[1]} for s in songs_list]
    write_file(ALBUMS_DIR / f"{alb_slug}.md", album(alb_slug, alb_title, "cake", alb_year, prod, song_dicts))
    for s in songs_list:
        write_file(SONGS_DIR / f"{s[0]}.md", song(s[0], s[1], "cake", alb_slug, alb_year,
            [{"person_slug": "john-mccrea", "role": "Writer"}, {"person_slug": prod, "role": "Producer"}]))
        cake_all_songs.append({"slug": s[0], "title": s[1]})

write_file(PEOPLE_DIR / "john-mccrea.md", person("john-mccrea", "John McCrea",
    [{"slug": "cake", "role": "Vocals/Guitar"}],
    [{"slug": s["slug"], "title": s["title"], "credit": "Writer"} for s in cake_all_songs]))
write_file(PEOPLE_DIR / "vince-di-fiore.md", person("vince-di-fiore", "Vince Di Fiore",
    [{"slug": "cake", "role": "Trumpet"}], []))
write_file(PEOPLE_DIR / "greg-brown-cake.md", person("greg-brown-cake", "Greg Brown",
    [{"slug": "cake", "role": "Guitar"}], []))
write_file(PEOPLE_DIR / "todd-roper.md", person("todd-roper", "Todd Roper",
    [{"slug": "cake", "role": "Drums"}], []))


# ============================================================
# 23. Sublime
# ============================================================
print("\n=== Sublime ===")
write_file(ARTISTS_DIR / "sublime.md", artist(
    "sublime", "Sublime", "Group",
    ["Alternative Rock", "Ska Punk"], "Alternative Rock", 1988,
    [{"slug": "bradley-nowell", "role": "Vocals/Guitar"},
     {"slug": "eric-wilson-sub", "role": "Bass"},
     {"slug": "bud-gaugh", "role": "Drums"}],
    [{"slug": "forty-oz-to-freedom-sublime", "title": "40oz. to Freedom", "year": 1992},
     {"slug": "robbins-the-hood-sublime", "title": "Robbin' the Hood", "year": 1994},
     {"slug": "sublime-self-titled", "title": "Sublime", "year": 1996}]
))

sub_albums = [
    ("forty-oz-to-freedom-sublime", "40oz. to Freedom", 1992, "david-kahne",
     [("date-rape-sublime", "Date Rape"), ("badfish-sublime", "Badfish"),
      ("smoke-two-joints-sublime", "Smoke Two Joints")]),
    ("robbins-the-hood-sublime", "Robbin' the Hood", 1994, "bradley-nowell", []),
    ("sublime-self-titled", "Sublime", 1996, "david-kahne",
     [("what-i-got-sublime", "What I Got"), ("santeria-sublime", "Santeria"),
      ("wrong-way-sublime", "Wrong Way"), ("caress-me-down-sublime", "Caress Me Down"),
      ("same-in-the-end-sublime", "Same in the End")]),
]

sub_all_songs = []
sub_kahne_songs = []
for alb_slug, alb_title, alb_year, prod, songs_list in sub_albums:
    song_dicts = [{"slug": s[0], "title": s[1]} for s in songs_list]
    write_file(ALBUMS_DIR / f"{alb_slug}.md", album(alb_slug, alb_title, "sublime", alb_year, prod, song_dicts))
    for s in songs_list:
        write_file(SONGS_DIR / f"{s[0]}.md", song(s[0], s[1], "sublime", alb_slug, alb_year,
            [{"person_slug": "bradley-nowell", "role": "Writer"}, {"person_slug": prod, "role": "Producer"}]))
        sub_all_songs.append({"slug": s[0], "title": s[1]})
        if prod == "david-kahne":
            sub_kahne_songs.append({"slug": s[0], "title": s[1]})

write_file(PEOPLE_DIR / "bradley-nowell.md", person("bradley-nowell", "Bradley Nowell",
    [{"slug": "sublime", "role": "Vocals/Guitar"}],
    [{"slug": s["slug"], "title": s["title"], "credit": "Writer"} for s in sub_all_songs]))
write_file(PEOPLE_DIR / "eric-wilson-sub.md", person("eric-wilson-sub", "Eric Wilson",
    [{"slug": "sublime", "role": "Bass"}], []))
write_file(PEOPLE_DIR / "bud-gaugh.md", person("bud-gaugh", "Bud Gaugh",
    [{"slug": "sublime", "role": "Drums"}], []))
write_file(PEOPLE_DIR / "david-kahne.md", person("david-kahne", "David Kahne", [],
    [{"slug": s["slug"], "title": s["title"], "credit": "Producer"} for s in sub_kahne_songs]))


# ============================================================
# 24. Everclear
# ============================================================
print("\n=== Everclear ===")
write_file(ARTISTS_DIR / "everclear.md", artist(
    "everclear", "Everclear", "Group",
    ["Alternative Rock", "Post-Grunge"], "Alternative Rock", 1992,
    [{"slug": "art-alexakis", "role": "Vocals/Guitar"},
     {"slug": "craig-montoya", "role": "Bass"},
     {"slug": "greg-eklund", "role": "Drums"}],
    [{"slug": "world-of-noise-everclear", "title": "World of Noise", "year": 1993},
     {"slug": "sparkle-and-fade-everclear", "title": "Sparkle and Fade", "year": 1995},
     {"slug": "so-much-for-afterglow-everclear", "title": "So Much for the Afterglow", "year": 1997}]
))

ec_albums = [
    ("world-of-noise-everclear", "World of Noise", 1993, "rob-schnapf", []),
    ("sparkle-and-fade-everclear", "Sparkle and Fade", 1995, "rob-schnapf",
     [("heroin-girl-everclear", "Heroin Girl"), ("santa-monica-everclear", "Santa Monica")]),
    ("so-much-for-afterglow-everclear", "So Much for the Afterglow", 1997, "rob-schnapf",
     [("i-will-buy-you-a-new-life-everclear", "I Will Buy You a New Life"),
      ("father-of-mine-everclear", "Father of Mine"),
      ("everything-to-everyone-everclear", "Everything to Everyone"),
      ("wonderful-everclear", "Wonderful")]),
]

ec_all_songs = []
for alb_slug, alb_title, alb_year, prod, songs_list in ec_albums:
    song_dicts = [{"slug": s[0], "title": s[1]} for s in songs_list]
    write_file(ALBUMS_DIR / f"{alb_slug}.md", album(alb_slug, alb_title, "everclear", alb_year, prod, song_dicts))
    for s in songs_list:
        write_file(SONGS_DIR / f"{s[0]}.md", song(s[0], s[1], "everclear", alb_slug, alb_year,
            [{"person_slug": "art-alexakis", "role": "Writer"}, {"person_slug": prod, "role": "Producer"}]))
        ec_all_songs.append({"slug": s[0], "title": s[1]})

write_file(PEOPLE_DIR / "art-alexakis.md", person("art-alexakis", "Art Alexakis",
    [{"slug": "everclear", "role": "Vocals/Guitar"}],
    [{"slug": s["slug"], "title": s["title"], "credit": "Writer"} for s in ec_all_songs]))
write_file(PEOPLE_DIR / "craig-montoya.md", person("craig-montoya", "Craig Montoya",
    [{"slug": "everclear", "role": "Bass"}], []))
write_file(PEOPLE_DIR / "greg-eklund.md", person("greg-eklund", "Greg Eklund",
    [{"slug": "everclear", "role": "Drums"}], []))
write_file(PEOPLE_DIR / "rob-schnapf.md", person("rob-schnapf", "Rob Schnapf", [],
    [{"slug": s["slug"], "title": s["title"], "credit": "Producer"} for s in ec_all_songs]))


# ============================================================
# 25. Dinosaur Jr
# ============================================================
print("\n=== Dinosaur Jr ===")
write_file(ARTISTS_DIR / "dinosaur-jr.md", artist(
    "dinosaur-jr", "Dinosaur Jr", "Group",
    ["Alternative Rock", "Indie Rock"], "Alternative Rock", 1984,
    [{"slug": "j-mascis", "role": "Vocals/Guitar"},
     {"slug": "lou-barlow", "role": "Bass"},
     {"slug": "murph-dinosaur", "role": "Drums"}],
    [{"slug": "dinosaur-dj", "title": "Dinosaur", "year": 1985},
     {"slug": "youre-living-all-over-me-dj", "title": "You're Living All Over Me", "year": 1987},
     {"slug": "bug-dj", "title": "Bug", "year": 1988},
     {"slug": "where-you-been-dj", "title": "Where You Been", "year": 1993},
     {"slug": "without-a-sound-dj", "title": "Without a Sound", "year": 1994},
     {"slug": "hand-it-over-dj", "title": "Hand It Over", "year": 1997},
     {"slug": "beyond-dj", "title": "Beyond", "year": 2007}]
))

dj_albums = [
    ("dinosaur-dj", "Dinosaur", 1985, "j-mascis", []),
    ("youre-living-all-over-me-dj", "You're Living All Over Me", 1987, "j-mascis",
     [("freak-scene-dj", "Freak Scene")]),
    ("bug-dj", "Bug", 1988, "j-mascis", []),
    ("where-you-been-dj", "Where You Been", 1993, "j-mascis",
     [("start-choppin-dj", "Start Choppin'"), ("the-wagon-dj", "The Wagon")]),
    ("without-a-sound-dj", "Without a Sound", 1994, "j-mascis",
     [("feel-the-pain-dj", "Feel the Pain"), ("i-dont-think-so-dj", "I Don't Think So")]),
    ("hand-it-over-dj", "Hand It Over", 1997, "j-mascis",
     [("out-there-dj", "Out There")]),
    ("beyond-dj", "Beyond", 2007, "j-mascis",
     [("almost-ready-dj", "Almost Ready")]),
]

dj_all_songs = []
for alb_slug, alb_title, alb_year, prod, songs_list in dj_albums:
    song_dicts = [{"slug": s[0], "title": s[1]} for s in songs_list]
    write_file(ALBUMS_DIR / f"{alb_slug}.md", album(alb_slug, alb_title, "dinosaur-jr", alb_year, prod, song_dicts))
    for s in songs_list:
        write_file(SONGS_DIR / f"{s[0]}.md", song(s[0], s[1], "dinosaur-jr", alb_slug, alb_year,
            [{"person_slug": "j-mascis", "role": "Writer"}, {"person_slug": prod, "role": "Producer"}]))
        dj_all_songs.append({"slug": s[0], "title": s[1]})

write_file(PEOPLE_DIR / "j-mascis.md", person("j-mascis", "J Mascis",
    [{"slug": "dinosaur-jr", "role": "Vocals/Guitar"}],
    [{"slug": s["slug"], "title": s["title"], "credit": "Writer"} for s in dj_all_songs]))
write_file(PEOPLE_DIR / "lou-barlow.md", person("lou-barlow", "Lou Barlow",
    [{"slug": "dinosaur-jr", "role": "Bass"}], []))
write_file(PEOPLE_DIR / "murph-dinosaur.md", person("murph-dinosaur", "Murph",
    [{"slug": "dinosaur-jr", "role": "Drums"}], []))


print(f"\n=== DONE: {created} files created, {skipped} skipped ===")
