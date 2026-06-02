"""
create_rock_2024.py — Creates content files for 25 rock acts.
Usage: python scripts/create_rock_2024.py
"""
from pathlib import Path

try:
    import yaml as _yaml
    def to_yaml(data):
        return _yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False)
except ImportError:
    raise RuntimeError("PyYAML not available. Install with: pip install pyyaml")

BASE = Path(r"c:\repo\MusicTree\content")
ARTISTS_DIR = BASE / "artists"
ALBUMS_DIR  = BASE / "albums"
SONGS_DIR   = BASE / "songs"
PEOPLE_DIR  = BASE / "people"

for d in [ARTISTS_DIR, ALBUMS_DIR, SONGS_DIR, PEOPLE_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ── People registry ──────────────────────────────────────────────────────────
_people = {}
_stats  = {"created": 0, "skipped": 0}


def _person(slug, title=None):
    if slug not in _people:
        _people[slug] = {"title": title or slug, "slug": slug, "bands": [], "song_credits": []}
    if title:
        _people[slug]["title"] = title
    return _people[slug]


def _add_member(person_slug, person_title, band_slug, role):
    p = _person(person_slug, person_title)
    entry = {"slug": band_slug, "role": role}
    if entry not in p["bands"]:
        p["bands"].append(entry)


def _add_credit(person_slug, person_title, song_slug, song_title, credit):
    p = _person(person_slug, person_title)
    entry = {"slug": song_slug, "title": song_title, "credit": credit}
    if entry not in p["song_credits"]:
        p["song_credits"].append(entry)


# ── File writer ───────────────────────────────────────────────────────────────
def _write(path, data):
    if path.exists():
        _stats["skipped"] += 1
        print(f"  skipped : {path.name}")
        return
    content = "---\n" + to_yaml(data) + "---\n"
    path.write_text(content, encoding="utf-8")
    _stats["created"] += 1
    print(f"  created : {path.name}")


# ── Domain helpers ────────────────────────────────────────────────────────────
def mk_artist(slug, title, band_type, genres, scene, formed, members, albums):
    """
    members : [(slug, title, role), ...]
    albums  : [(slug, title, year), ...]
    """
    _write(ARTISTS_DIR / f"{slug}.md", {
        "title": title, "slug": slug, "band_type": band_type,
        "genres": genres, "scene": scene, "formed": formed,
        "members": [{"slug": m[0], "role": m[2]} for m in members],
        "albums":  [{"slug": a[0], "title": a[1], "year": a[2]} for a in albums],
    })
    for m_slug, m_title, m_role in members:
        _add_member(m_slug, m_title, slug, m_role)


def mk_album(slug, title, artist, year, producer, songs):
    """songs : [(slug, title), ...]"""
    _write(ALBUMS_DIR / f"{slug}.md", {
        "title": title, "slug": slug, "artist": artist,
        "year": year, "producer": producer,
        "songs": [{"slug": s[0], "title": s[1]} for s in songs],
    })


def mk_song(slug, title, artist, album, year, credits):
    """credits : [(person_slug, person_title, role), ...]"""
    _write(SONGS_DIR / f"{slug}.md", {
        "title": title, "slug": slug, "artist": artist,
        "album": album, "year": year,
        "credits": [{"person_slug": c[0], "role": c[2]} for c in credits],
    })
    for c_slug, c_title, c_role in credits:
        _add_credit(c_slug, c_title, slug, title, c_role)


# =============================================================================
# 1. SLIPKNOT
# =============================================================================
print("\n=== 1. Slipknot ===")
_SLP = "slipknot"
mk_artist(_SLP, "Slipknot", "Group", ["Alternative Rock", "Metal"],
          "Alternative Rock", 1995,
          [("corey-taylor",    "Corey Taylor",    "Vocals"),
           ("mick-thomson",    "Mick Thomson",    "Guitar"),
           ("jim-root",        "Jim Root",        "Guitar"),
           ("craig-jones-sk",  "Craig Jones",     "Samples"),
           ("sid-wilson",      "Sid Wilson",      "DJ"),
           ("shawn-crahan",    "Shawn Crahan",    "Percussion"),
           ("jay-weinberg",    "Jay Weinberg",    "Drums"),
           ("eloy-casagrande", "Eloy Casagrande", "Drums")],
          [("slipknot-1999",           "Slipknot",                      1999),
           ("iowa-slp",                "Iowa",                          2001),
           ("vol-3-subliminal-verses", "Vol. 3: The Subliminal Verses", 2004),
           ("all-hope-is-gone-slp",    "All Hope Is Gone",              2008),
           ("dot5-the-gray-chapter",   ".5: The Gray Chapter",          2014),
           ("we-are-not-your-kind",    "We Are Not Your Kind",          2019),
           ("the-end-so-far",          "The End, So Far",               2022)])

mk_album("slipknot-1999", "Slipknot", _SLP, 1999, "ross-robinson",
         [("wait-and-bleed-slp", "Wait and Bleed")])
mk_album("iowa-slp", "Iowa", _SLP, 2001, "ross-robinson", [])
mk_album("vol-3-subliminal-verses", "Vol. 3: The Subliminal Verses", _SLP, 2004, "corey-taylor",
         [("duality-slp", "Duality"), ("before-i-forget-slp", "Before I Forget")])
mk_album("all-hope-is-gone-slp", "All Hope Is Gone", _SLP, 2008, "corey-taylor",
         [("psychosocial-slp", "Psychosocial")])
mk_album("dot5-the-gray-chapter", ".5: The Gray Chapter", _SLP, 2014, "corey-taylor",
         [("the-devil-in-i-slp", "The Devil in I")])
mk_album("we-are-not-your-kind", "We Are Not Your Kind", _SLP, 2019, "corey-taylor",
         [("unsainted-slp", "Unsainted")])
mk_album("the-end-so-far", "The End, So Far", _SLP, 2022, "corey-taylor", [])

mk_song("wait-and-bleed-slp",   "Wait and Bleed",   _SLP, "slipknot-1999",           1999,
        [("corey-taylor", "Corey Taylor", "Vocals"), ("ross-robinson", "Ross Robinson", "Producer")])
mk_song("duality-slp",          "Duality",          _SLP, "vol-3-subliminal-verses", 2004,
        [("corey-taylor", "Corey Taylor", "Vocals")])
mk_song("before-i-forget-slp",  "Before I Forget",  _SLP, "vol-3-subliminal-verses", 2004,
        [("corey-taylor", "Corey Taylor", "Vocals")])
mk_song("psychosocial-slp",     "Psychosocial",     _SLP, "all-hope-is-gone-slp",    2008,
        [("corey-taylor", "Corey Taylor", "Vocals")])
mk_song("the-devil-in-i-slp",   "The Devil in I",   _SLP, "dot5-the-gray-chapter",   2014,
        [("corey-taylor", "Corey Taylor", "Vocals")])
mk_song("unsainted-slp",        "Unsainted",        _SLP, "we-are-not-your-kind",    2019,
        [("corey-taylor", "Corey Taylor", "Vocals")])

_person("ross-robinson", "Ross Robinson")


# =============================================================================
# 2. GHOST
# =============================================================================
print("\n=== 2. Ghost ===")
_GHO = "ghost"
mk_artist(_GHO, "Ghost", "Group", ["Rock", "Metal"], "Rock", 2006,
          [("tobias-forge", "Tobias Forge", "Vocals")],
          [("opus-eponymous",    "Opus Eponymous", 2010),
           ("infestissumam-gho", "Infestissumam",  2013),
           ("meliora-gho",       "Meliora",        2015),
           ("prequelle-gho",     "Prequelle",      2018),
           ("impera-gho",        "Impera",         2022)])

mk_album("opus-eponymous",    "Opus Eponymous", _GHO, 2010, "tobias-forge", [])
mk_album("infestissumam-gho", "Infestissumam",  _GHO, 2013, "klas-ahlund",  [])
mk_album("meliora-gho",       "Meliora",        _GHO, 2015, "klas-ahlund",
         [("square-hammer-gho", "Square Hammer"), ("cirice-gho", "Cirice")])
mk_album("prequelle-gho",     "Prequelle",      _GHO, 2018, "klas-ahlund",
         [("rats-gho", "Rats"), ("dance-macabre-gho", "Dance Macabre"), ("mary-on-a-cross-gho", "Mary on a Cross")])
mk_album("impera-gho",        "Impera",         _GHO, 2022, "klas-ahlund",
         [("spillways-gho", "Spillways")])

mk_song("square-hammer-gho",   "Square Hammer",   _GHO, "meliora-gho",   2015,
        [("tobias-forge", "Tobias Forge", "Vocals"), ("klas-ahlund", "Klas Ahlund", "Producer")])
mk_song("cirice-gho",          "Cirice",          _GHO, "meliora-gho",   2015,
        [("tobias-forge", "Tobias Forge", "Vocals")])
mk_song("rats-gho",            "Rats",            _GHO, "prequelle-gho", 2018,
        [("tobias-forge", "Tobias Forge", "Vocals"), ("klas-ahlund", "Klas Ahlund", "Producer")])
mk_song("dance-macabre-gho",   "Dance Macabre",   _GHO, "prequelle-gho", 2018,
        [("tobias-forge", "Tobias Forge", "Vocals")])
mk_song("mary-on-a-cross-gho", "Mary on a Cross", _GHO, "prequelle-gho", 2018,
        [("tobias-forge", "Tobias Forge", "Vocals")])
mk_song("spillways-gho",       "Spillways",       _GHO, "impera-gho",    2022,
        [("tobias-forge", "Tobias Forge", "Vocals")])

_person("klas-ahlund", "Klas Ahlund")


# =============================================================================
# 3. BRING ME THE HORIZON
# =============================================================================
print("\n=== 3. Bring Me the Horizon ===")
_BMTH = "bring-me-the-horizon"
mk_artist(_BMTH, "Bring Me the Horizon", "Group", ["Alternative Rock"], "Alternative Rock", 2004,
          [("oliver-sykes",  "Oliver Sykes",  "Vocals"),
           ("lee-malia",     "Lee Malia",     "Guitar"),
           ("matt-kean",     "Matt Kean",     "Bass"),
           ("matt-nicholls", "Matt Nicholls", "Drums"),
           ("jordan-fish",   "Jordan Fish",   "Keys")],
          [("sempiternal-bmth",          "Sempiternal",                  2013),
           ("thats-the-spirit-bmth",     "That's the Spirit",            2015),
           ("amo-bmth",                  "amo",                          2019),
           ("post-human-survival-horror","POST HUMAN: SURVIVAL HORROR",  2020)])

mk_album("sempiternal-bmth",           "Sempiternal",               _BMTH, 2013, "tom-dalgety",
         [("can-you-feel-my-heart-bmth", "Can You Feel My Heart"), ("sleepwalking-bmth", "Sleepwalking")])
mk_album("thats-the-spirit-bmth",      "That's the Spirit",         _BMTH, 2015, "tom-dalgety",
         [("throne-bmth", "Throne"), ("follow-you-bmth", "Follow You")])
mk_album("amo-bmth",                   "amo",                       _BMTH, 2019, "oliver-sykes",
         [("mantra-bmth", "Mantra"), ("teardrops-bmth", "Teardrops")])
mk_album("post-human-survival-horror", "POST HUMAN: SURVIVAL HORROR", _BMTH, 2020, "oliver-sykes", [])

mk_song("can-you-feel-my-heart-bmth", "Can You Feel My Heart", _BMTH, "sempiternal-bmth",      2013,
        [("oliver-sykes", "Oliver Sykes", "Vocals"), ("tom-dalgety", "Tom Dalgety", "Producer")])
mk_song("sleepwalking-bmth",          "Sleepwalking",          _BMTH, "sempiternal-bmth",      2013,
        [("oliver-sykes", "Oliver Sykes", "Vocals")])
mk_song("throne-bmth",                "Throne",                _BMTH, "thats-the-spirit-bmth", 2015,
        [("oliver-sykes", "Oliver Sykes", "Vocals"), ("tom-dalgety", "Tom Dalgety", "Producer")])
mk_song("follow-you-bmth",            "Follow You",            _BMTH, "thats-the-spirit-bmth", 2015,
        [("oliver-sykes", "Oliver Sykes", "Vocals")])
mk_song("mantra-bmth",                "Mantra",                _BMTH, "amo-bmth",              2019,
        [("oliver-sykes", "Oliver Sykes", "Vocals")])
mk_song("teardrops-bmth",             "Teardrops",             _BMTH, "amo-bmth",              2019,
        [("oliver-sykes", "Oliver Sykes", "Vocals")])

_person("tom-dalgety", "Tom Dalgety")


# =============================================================================
# 4. MASTODON
# =============================================================================
print("\n=== 4. Mastodon ===")
_MAST = "mastodon"
mk_artist(_MAST, "Mastodon", "Group", ["Alternative Rock", "Metal"], "Alternative Rock", 2000,
          [("brann-dailor",  "Brann Dailor",  "Drums"),
           ("bill-kelliher", "Bill Kelliher", "Guitar"),
           ("brent-hinds",   "Brent Hinds",   "Guitar"),
           ("troy-sanders",  "Troy Sanders",  "Bass")],
          [("leviathan-mast",    "Leviathan",       2004),
           ("blood-mountain-mast","Blood Mountain", 2006),
           ("crack-the-skye",    "Crack the Skye",  2009),
           ("the-hunter-mast",   "The Hunter",      2011),
           ("emperor-of-sand",   "Emperor of Sand", 2017),
           ("hushed-and-grim",   "Hushed and Grim", 2021)])

mk_album("leviathan-mast",     "Leviathan",       _MAST, 2004, "brann-dailor",
         [("blood-and-thunder-mast", "Blood and Thunder"), ("iron-tusk-mast", "Iron Tusk")])
mk_album("blood-mountain-mast","Blood Mountain",  _MAST, 2006, "brann-dailor", [])
mk_album("crack-the-skye",     "Crack the Skye",  _MAST, 2009, "brann-dailor",
         [("oblivion-mast", "Oblivion")])
mk_album("the-hunter-mast",    "The Hunter",      _MAST, 2011, "brann-dailor",
         [("curl-of-the-burl-mast", "Curl of the Burl")])
mk_album("emperor-of-sand",    "Emperor of Sand", _MAST, 2017, "brann-dailor",
         [("show-yourself-mast", "Show Yourself")])
mk_album("hushed-and-grim",    "Hushed and Grim", _MAST, 2021, "brann-dailor", [])

mk_song("blood-and-thunder-mast", "Blood and Thunder",  _MAST, "leviathan-mast",  2004,
        [("brent-hinds",  "Brent Hinds",  "Vocals")])
mk_song("iron-tusk-mast",         "Iron Tusk",          _MAST, "leviathan-mast",  2004,
        [("troy-sanders", "Troy Sanders", "Vocals")])
mk_song("oblivion-mast",          "Oblivion",           _MAST, "crack-the-skye",  2009,
        [("brent-hinds",  "Brent Hinds",  "Vocals")])
mk_song("curl-of-the-burl-mast",  "Curl of the Burl",   _MAST, "the-hunter-mast", 2011,
        [("brent-hinds",  "Brent Hinds",  "Vocals")])
mk_song("show-yourself-mast",     "Show Yourself",      _MAST, "emperor-of-sand", 2017,
        [("brann-dailor", "Brann Dailor", "Vocals")])


# =============================================================================
# 5. AVENGED SEVENFOLD
# =============================================================================
print("\n=== 5. Avenged Sevenfold ===")
_A7X = "avenged-sevenfold"
mk_artist(_A7X, "Avenged Sevenfold", "Group", ["Alternative Rock", "Metal"], "Alternative Rock", 1999,
          [("m-shadows",        "M. Shadows",        "Vocals"),
           ("zacky-vengeance",  "Zacky Vengeance",   "Guitar"),
           ("synyster-gates",   "Synyster Gates",    "Guitar"),
           ("johnny-christ",    "Johnny Christ",     "Bass"),
           ("brooks-wackerman", "Brooks Wackerman",  "Drums")],
          [("city-of-evil-a7x",        "City of Evil",          2005),
           ("avenged-sevenfold-2007",  "Avenged Sevenfold",     2007),
           ("nightmare-a7x",           "Nightmare",             2010),
           ("hail-to-the-king-a7x",    "Hail to the King",      2013),
           ("the-stage-a7x",           "The Stage",             2016),
           ("life-is-but-a-dream-a7x", "Life Is But a Dream...",2023)])

mk_album("city-of-evil-a7x",        "City of Evil",           _A7X, 2005, "joe-barresi",
         [("bat-country-a7x", "Bat Country"), ("beast-and-the-harlot-a7x", "Beast and the Harlot")])
mk_album("avenged-sevenfold-2007",  "Avenged Sevenfold",      _A7X, 2007, "joe-barresi", [])
mk_album("nightmare-a7x",           "Nightmare",              _A7X, 2010, "joe-barresi",
         [("nightmare-song-a7x", "Nightmare")])
mk_album("hail-to-the-king-a7x",    "Hail to the King",       _A7X, 2013, "joe-barresi",
         [("hail-to-the-king-song-a7x", "Hail to the King")])
mk_album("the-stage-a7x",           "The Stage",              _A7X, 2016, "joe-barresi",
         [("the-stage-song-a7x", "The Stage")])
mk_album("life-is-but-a-dream-a7x", "Life Is But a Dream...", _A7X, 2023, "m-shadows", [])

mk_song("bat-country-a7x",           "Bat Country",      _A7X, "city-of-evil-a7x",       2005,
        [("m-shadows", "M. Shadows", "Vocals"), ("joe-barresi", "Joe Barresi", "Producer")])
mk_song("beast-and-the-harlot-a7x",  "Beast and the Harlot", _A7X, "city-of-evil-a7x",  2005,
        [("m-shadows", "M. Shadows", "Vocals")])
mk_song("nightmare-song-a7x",        "Nightmare",        _A7X, "nightmare-a7x",           2010,
        [("m-shadows", "M. Shadows", "Vocals")])
mk_song("hail-to-the-king-song-a7x", "Hail to the King", _A7X, "hail-to-the-king-a7x",  2013,
        [("m-shadows", "M. Shadows", "Vocals")])
mk_song("the-stage-song-a7x",        "The Stage",        _A7X, "the-stage-a7x",           2016,
        [("m-shadows", "M. Shadows", "Vocals")])

_person("joe-barresi", "Joe Barresi")


# =============================================================================
# 6. SHINEDOWN
# =============================================================================
print("\n=== 6. Shinedown ===")
_SDN = "shinedown"
mk_artist(_SDN, "Shinedown", "Group", ["Rock"], "Rock", 2001,
          [("brent-smith", "Brent Smith", "Vocals"),
           ("zach-myers",  "Zach Myers",  "Guitar"),
           ("eric-bass",   "Eric Bass",   "Bass"),
           ("barry-kerch", "Barry Kerch", "Drums")],
          [("the-sound-of-madness-sdn",  "The Sound of Madness", 2008),
           ("amaryllis-sdn",             "Amaryllis",            2012),
           ("attention-attention-sdn",   "ATTENTION ATTENTION",  2018),
           ("planet-zero-sdn",           "Planet Zero",          2022)])

mk_album("the-sound-of-madness-sdn",  "The Sound of Madness", _SDN, 2008, "eric-bass",
         [("second-chance-sdn", "Second Chance"), ("the-sound-of-madness-song-sdn", "The Sound of Madness")])
mk_album("amaryllis-sdn",             "Amaryllis",            _SDN, 2012, "eric-bass",
         [("bully-sdn", "Bully")])
mk_album("attention-attention-sdn",   "ATTENTION ATTENTION",  _SDN, 2018, "eric-bass",
         [("cut-the-cord-sdn", "Cut the Cord")])
mk_album("planet-zero-sdn",           "Planet Zero",          _SDN, 2022, "eric-bass", [])

mk_song("second-chance-sdn",              "Second Chance",        _SDN, "the-sound-of-madness-sdn", 2008,
        [("brent-smith", "Brent Smith", "Vocals")])
mk_song("the-sound-of-madness-song-sdn",  "The Sound of Madness", _SDN, "the-sound-of-madness-sdn", 2008,
        [("brent-smith", "Brent Smith", "Vocals")])
mk_song("bully-sdn",                      "Bully",                _SDN, "amaryllis-sdn",             2012,
        [("brent-smith", "Brent Smith", "Vocals")])
mk_song("cut-the-cord-sdn",               "Cut the Cord",         _SDN, "attention-attention-sdn",   2018,
        [("brent-smith", "Brent Smith", "Vocals")])


# =============================================================================
# 7. JIMMY EAT WORLD
# =============================================================================
print("\n=== 7. Jimmy Eat World ===")
_JEW = "jimmy-eat-world"
mk_artist(_JEW, "Jimmy Eat World", "Group", ["Alternative Rock"], "Alternative Rock", 1993,
          [("jim-adkins",  "Jim Adkins",  "Vocals"),
           ("tom-linton",  "Tom Linton",  "Guitar"),
           ("rick-burch",  "Rick Burch",  "Bass"),
           ("zach-lind",   "Zach Lind",   "Drums")],
          [("bleed-american-jew",    "Bleed American",  2001),
           ("futures-jew",           "Futures",         2004),
           ("chase-this-light-jew",  "Chase This Light",2007),
           ("surviving-jew",         "Surviving",       2019)])

mk_album("bleed-american-jew",   "Bleed American",   _JEW, 2001, "jim-adkins",
         [("the-middle-jew", "The Middle"), ("sweetness-jew", "Sweetness")])
mk_album("futures-jew",          "Futures",          _JEW, 2004, "jim-adkins",
         [("pain-jew", "Pain"), ("futures-song-jew", "Futures")])
mk_album("chase-this-light-jew", "Chase This Light", _JEW, 2007, "jim-adkins",
         [("work-jew", "Work")])
mk_album("surviving-jew",        "Surviving",        _JEW, 2019, "jim-adkins", [])

mk_song("the-middle-jew",    "The Middle", _JEW, "bleed-american-jew",   2001,
        [("jim-adkins", "Jim Adkins", "Vocals")])
mk_song("sweetness-jew",     "Sweetness",  _JEW, "bleed-american-jew",   2001,
        [("jim-adkins", "Jim Adkins", "Vocals")])
mk_song("pain-jew",          "Pain",       _JEW, "futures-jew",          2004,
        [("jim-adkins", "Jim Adkins", "Vocals")])
mk_song("futures-song-jew",  "Futures",    _JEW, "futures-jew",          2004,
        [("jim-adkins", "Jim Adkins", "Vocals")])
mk_song("work-jew",          "Work",       _JEW, "chase-this-light-jew", 2007,
        [("jim-adkins", "Jim Adkins", "Vocals")])


# =============================================================================
# 8. TAKING BACK SUNDAY
# =============================================================================
print("\n=== 8. Taking Back Sunday ===")
_TBS = "taking-back-sunday"
mk_artist(_TBS, "Taking Back Sunday", "Group", ["Alternative Rock"], "Alternative Rock", 1999,
          [("adam-lazzara",  "Adam Lazzara",   "Vocals"),
           ("john-nolan",    "John Nolan",     "Guitar"),
           ("shaun-cooper",  "Shaun Cooper",   "Bass"),
           ("mark-oconnell", "Mark O'Connell", "Drums"),
           ("eddie-reyes",   "Eddie Reyes",    "Guitar")],
          [("tell-all-your-friends-tbs",   "Tell All Your Friends", 2002),
           ("where-you-want-to-be-tbs",    "Where You Want to Be",  2004),
           ("louder-now-tbs",              "Louder Now",            2006),
           ("new-again-tbs",              "New Again",             2009)])

mk_album("tell-all-your-friends-tbs",  "Tell All Your Friends", _TBS, 2002, "adam-lazzara",
         [("cute-without-the-e-tbs", "Cute Without the E (Cut From the Team)"),
          ("youre-so-last-summer-tbs", "You're So Last Summer")])
mk_album("where-you-want-to-be-tbs",   "Where You Want to Be",  _TBS, 2004, "adam-lazzara", [])
mk_album("louder-now-tbs",             "Louder Now",            _TBS, 2006, "adam-lazzara",
         [("makedamnsure-tbs", "MakeDamnSure")])
mk_album("new-again-tbs",             "New Again",             _TBS, 2009, "adam-lazzara",
         [("new-again-song-tbs", "New Again")])

mk_song("cute-without-the-e-tbs",    "Cute Without the E (Cut From the Team)",
        _TBS, "tell-all-your-friends-tbs", 2002,
        [("adam-lazzara", "Adam Lazzara", "Vocals")])
mk_song("youre-so-last-summer-tbs",  "You're So Last Summer",
        _TBS, "tell-all-your-friends-tbs", 2002,
        [("adam-lazzara", "Adam Lazzara", "Vocals")])
mk_song("makedamnsure-tbs",          "MakeDamnSure",  _TBS, "louder-now-tbs",  2006,
        [("adam-lazzara", "Adam Lazzara", "Vocals")])
mk_song("new-again-song-tbs",        "New Again",     _TBS, "new-again-tbs",   2009,
        [("adam-lazzara", "Adam Lazzara", "Vocals")])


# =============================================================================
# 9. THE GASLIGHT ANTHEM
# =============================================================================
print("\n=== 9. The Gaslight Anthem ===")
_TGA = "the-gaslight-anthem"
mk_artist(_TGA, "The Gaslight Anthem", "Group", ["Rock"], "Rock", 2006,
          [("brian-fallon",    "Brian Fallon",    "Vocals"),
           ("alex-rosamilia",  "Alex Rosamilia",  "Guitar"),
           ("benny-horowitz",  "Benny Horowitz",  "Drums")],
          [("the-59-sound",      "The '59 Sound", 2008),
           ("american-slang-tga","American Slang", 2010),
           ("handwritten-tga",   "Handwritten",   2012),
           ("history-books-tga", "History Books", 2023)])

mk_album("the-59-sound",       "The '59 Sound", _TGA, 2008, "ted-hutt",
         [("the-59-sound-song", "The '59 Sound"), ("heres-looking-at-you-kid-tga", "Here's Looking at You Kid")])
mk_album("american-slang-tga", "American Slang", _TGA, 2010, "ted-hutt",
         [("here-comes-my-man-tga", "Here Comes My Man")])
mk_album("handwritten-tga",    "Handwritten",    _TGA, 2012, "ted-hutt",
         [("get-hurt-tga", "Get Hurt")])
mk_album("history-books-tga",  "History Books",  _TGA, 2023, "brian-fallon", [])

mk_song("the-59-sound-song",          "The '59 Sound",              _TGA, "the-59-sound",       2008,
        [("brian-fallon", "Brian Fallon", "Vocals"), ("ted-hutt", "Ted Hutt", "Producer")])
mk_song("heres-looking-at-you-kid-tga","Here's Looking at You Kid", _TGA, "the-59-sound",       2008,
        [("brian-fallon", "Brian Fallon", "Vocals")])
mk_song("here-comes-my-man-tga",      "Here Comes My Man",          _TGA, "american-slang-tga", 2010,
        [("brian-fallon", "Brian Fallon", "Vocals")])
mk_song("get-hurt-tga",               "Get Hurt",                   _TGA, "handwritten-tga",    2012,
        [("brian-fallon", "Brian Fallon", "Vocals")])

_person("ted-hutt", "Ted Hutt")


# =============================================================================
# 10. DROPKICK MURPHYS
# =============================================================================
print("\n=== 10. Dropkick Murphys ===")
_DKM = "dropkick-murphys"
mk_artist(_DKM, "Dropkick Murphys", "Group", ["Punk Rock"], "Punk Rock", 1996,
          [("ken-casey",     "Ken Casey",  "Vocals"),
           ("al-barr",       "Al Barr",    "Vocals"),
           ("matt-kelly-dkm","Matt Kelly", "Drums")],
          [("warriors-code-dkm",       "The Warrior's Code",         2005),
           ("the-meanest-of-times-dkm","The Meanest of Times",       2007),
           ("going-out-in-style-dkm",  "Going Out in Style",         2011),
           ("signed-and-sealed-dkm",   "Signed and Sealed in Blood", 2013)])

mk_album("warriors-code-dkm",        "The Warrior's Code",         _DKM, 2005, "ted-hutt",
         [("im-shipping-up-to-boston-dkm", "I'm Shipping Up to Boston"), ("tessie-dkm", "Tessie")])
mk_album("the-meanest-of-times-dkm", "The Meanest of Times",       _DKM, 2007, "ted-hutt",
         [("the-state-of-massachusetts-dkm", "The State of Massachusetts")])
mk_album("going-out-in-style-dkm",   "Going Out in Style",         _DKM, 2011, "ted-hutt",
         [("rose-tattoo-dkm", "Rose Tattoo")])
mk_album("signed-and-sealed-dkm",    "Signed and Sealed in Blood", _DKM, 2013, "ted-hutt", [])

mk_song("im-shipping-up-to-boston-dkm",    "I'm Shipping Up to Boston",  _DKM, "warriors-code-dkm",        2005,
        [("ken-casey", "Ken Casey", "Vocals"), ("ted-hutt", "Ted Hutt", "Producer")])
mk_song("tessie-dkm",                      "Tessie",                     _DKM, "warriors-code-dkm",        2005,
        [("ken-casey", "Ken Casey", "Vocals")])
mk_song("the-state-of-massachusetts-dkm",  "The State of Massachusetts", _DKM, "the-meanest-of-times-dkm", 2007,
        [("ken-casey", "Ken Casey", "Vocals")])
mk_song("rose-tattoo-dkm",                 "Rose Tattoo",                _DKM, "going-out-in-style-dkm",   2011,
        [("ken-casey", "Ken Casey", "Vocals")])


# =============================================================================
# 11. RISE AGAINST
# =============================================================================
print("\n=== 11. Rise Against ===")
_RA = "rise-against"
mk_artist(_RA, "Rise Against", "Group", ["Punk Rock"], "Punk Rock", 1999,
          [("tim-mcilrath",   "Tim McIlrath",   "Vocals"),
           ("zach-blair",     "Zach Blair",     "Guitar"),
           ("joe-principe",   "Joe Principe",   "Bass"),
           ("brandon-barnes", "Brandon Barnes", "Drums")],
          [("siren-song-counter-culture-ra",  "Siren Song of the Counter Culture", 2004),
           ("the-sufferer-and-witness-ra",    "The Sufferer & the Witness",        2006),
           ("appeal-to-reason-ra",            "Appeal to Reason",                  2008),
           ("endgame-ra",                     "Endgame",                           2011),
           ("wolves-ra",                      "Wolves",                            2017)])

mk_album("siren-song-counter-culture-ra", "Siren Song of the Counter Culture", _RA, 2004, "bill-stevenson",
         [("give-it-all-ra", "Give It All"), ("swing-life-away-ra", "Swing Life Away")])
mk_album("the-sufferer-and-witness-ra",   "The Sufferer & the Witness",        _RA, 2006, "bill-stevenson",
         [("prayer-of-the-refugee-ra", "Prayer of the Refugee")])
mk_album("appeal-to-reason-ra",           "Appeal to Reason",                  _RA, 2008, "bill-stevenson",
         [("savior-ra", "Savior")])
mk_album("endgame-ra",                    "Endgame",                           _RA, 2011, "bill-stevenson",
         [("satellite-ra", "Satellite")])
mk_album("wolves-ra",                     "Wolves",                            _RA, 2017, "tim-mcilrath", [])

mk_song("give-it-all-ra",         "Give It All",           _RA, "siren-song-counter-culture-ra", 2004,
        [("tim-mcilrath", "Tim McIlrath", "Vocals"), ("bill-stevenson", "Bill Stevenson", "Producer")])
mk_song("swing-life-away-ra",     "Swing Life Away",       _RA, "siren-song-counter-culture-ra", 2004,
        [("tim-mcilrath", "Tim McIlrath", "Vocals")])
mk_song("prayer-of-the-refugee-ra","Prayer of the Refugee",_RA, "the-sufferer-and-witness-ra",   2006,
        [("tim-mcilrath", "Tim McIlrath", "Vocals")])
mk_song("savior-ra",              "Savior",                _RA, "appeal-to-reason-ra",           2008,
        [("tim-mcilrath", "Tim McIlrath", "Vocals")])
mk_song("satellite-ra",           "Satellite",             _RA, "endgame-ra",                    2011,
        [("tim-mcilrath", "Tim McIlrath", "Vocals")])

_person("bill-stevenson", "Bill Stevenson")


# =============================================================================
# 12. NOTHING BUT THIEVES
# =============================================================================
print("\n=== 12. Nothing But Thieves ===")
_NBT = "nothing-but-thieves"
mk_artist(_NBT, "Nothing But Thieves", "Group", ["Alternative Rock"], "Alternative Rock", 2012,
          [("conor-mason",          "Conor Mason",         "Vocals"),
           ("joe-langridge-brown",  "Joe Langridge-Brown", "Guitar"),
           ("dominic-craik",        "Dominic Craik",       "Guitar"),
           ("philip-blake",         "Philip Blake",        "Bass"),
           ("james-price-nbt",      "James Price",         "Drums")],
          [("nothing-but-thieves-2015", "Nothing But Thieves", 2015),
           ("broken-machine-nbt",       "Broken Machine",      2017),
           ("moral-panic-nbt",          "Moral Panic",         2020),
           ("dead-club-city-nbt",       "Dead Club City",      2023)])

mk_album("nothing-but-thieves-2015", "Nothing But Thieves", _NBT, 2015, "conor-mason",
         [("amsterdam-nbt", "Amsterdam"), ("trip-switch-nbt", "Trip Switch")])
mk_album("broken-machine-nbt",       "Broken Machine",      _NBT, 2017, "conor-mason",
         [("sorry-nbt", "Sorry")])
mk_album("moral-panic-nbt",          "Moral Panic",         _NBT, 2020, "conor-mason",
         [("is-everybody-going-crazy-nbt", "Is Everybody Going Crazy?")])
mk_album("dead-club-city-nbt",       "Dead Club City",      _NBT, 2023, "conor-mason",
         [("city-haunts-nbt", "City Haunts")])

mk_song("amsterdam-nbt",               "Amsterdam",                  _NBT, "nothing-but-thieves-2015", 2015,
        [("conor-mason", "Conor Mason", "Vocals")])
mk_song("trip-switch-nbt",             "Trip Switch",                _NBT, "nothing-but-thieves-2015", 2015,
        [("conor-mason", "Conor Mason", "Vocals")])
mk_song("sorry-nbt",                   "Sorry",                      _NBT, "broken-machine-nbt",       2017,
        [("conor-mason", "Conor Mason", "Vocals")])
mk_song("is-everybody-going-crazy-nbt","Is Everybody Going Crazy?",  _NBT, "moral-panic-nbt",          2020,
        [("conor-mason", "Conor Mason", "Vocals")])
mk_song("city-haunts-nbt",             "City Haunts",                _NBT, "dead-club-city-nbt",       2023,
        [("conor-mason", "Conor Mason", "Vocals")])


# =============================================================================
# 13. COHEED AND CAMBRIA
# =============================================================================
print("\n=== 13. Coheed and Cambria ===")
_CAC = "coheed-and-cambria"
mk_artist(_CAC, "Coheed and Cambria", "Group", ["Alternative Rock"], "Alternative Rock", 1995,
          [("claudio-sanchez",  "Claudio Sanchez", "Vocals"),
           ("travis-stever",    "Travis Stever",   "Guitar"),
           ("zach-cooper-cac",  "Zach Cooper",     "Bass"),
           ("josh-eppard",      "Josh Eppard",     "Drums")],
          [("in-keeping-secrets-cac",       "In Keeping Secrets of Silent Earth: 3",      2003),
           ("good-apollo-i-burning-star-iv","Good Apollo I'm Burning Star IV, Volume One", 2005),
           ("the-afterman-ascension-cac",   "The Afterman: Ascension",                    2012),
           ("color-before-the-sun-cac",     "The Color Before the Sun",                   2015)])

mk_album("in-keeping-secrets-cac",       "In Keeping Secrets of Silent Earth: 3",
         _CAC, 2003, "claudio-sanchez",
         [("a-favor-house-atlantic-cac", "A Favor House Atlantic"), ("the-suffering-cac", "The Suffering")])
mk_album("good-apollo-i-burning-star-iv","Good Apollo I'm Burning Star IV, Volume One",
         _CAC, 2005, "claudio-sanchez",
         [("welcome-home-cac", "Welcome Home")])
mk_album("the-afterman-ascension-cac",   "The Afterman: Ascension",
         _CAC, 2012, "claudio-sanchez",
         [("key-entity-extraction-i-cac", "Key Entity Extraction I: Domino the Destitute")])
mk_album("color-before-the-sun-cac",     "The Color Before the Sun",
         _CAC, 2015, "claudio-sanchez", [])

mk_song("a-favor-house-atlantic-cac",    "A Favor House Atlantic",   _CAC, "in-keeping-secrets-cac",       2003,
        [("claudio-sanchez", "Claudio Sanchez", "Vocals")])
mk_song("the-suffering-cac",             "The Suffering",            _CAC, "in-keeping-secrets-cac",       2003,
        [("claudio-sanchez", "Claudio Sanchez", "Vocals")])
mk_song("welcome-home-cac",              "Welcome Home",             _CAC, "good-apollo-i-burning-star-iv", 2005,
        [("claudio-sanchez", "Claudio Sanchez", "Vocals")])
mk_song("key-entity-extraction-i-cac",
        "Key Entity Extraction I: Domino the Destitute",
        _CAC, "the-afterman-ascension-cac", 2012,
        [("claudio-sanchez", "Claudio Sanchez", "Vocals")])


# =============================================================================
# 14. LAMB OF GOD
# =============================================================================
print("\n=== 14. Lamb of God ===")
_LOG = "lamb-of-god"
mk_artist(_LOG, "Lamb of God", "Group", ["Alternative Rock", "Metal"], "Alternative Rock", 1994,
          [("randy-blythe",      "Randy Blythe",  "Vocals"),
           ("mark-morton",       "Mark Morton",   "Guitar"),
           ("willie-adler",      "Willie Adler",  "Guitar"),
           ("john-campbell-log", "John Campbell", "Bass"),
           ("chris-adler",       "Chris Adler",   "Drums")],
          [("ashes-of-the-wake-log", "Ashes of the Wake", 2004),
           ("sacrament-log",         "Sacrament",         2006),
           ("wrath-log",             "Wrath",             2009),
           ("resolution-log",        "Resolution",        2012),
           ("lamb-of-god-2020",      "Lamb of God",       2020)])

mk_album("ashes-of-the-wake-log", "Ashes of the Wake", _LOG, 2004, "machine-producer",
         [("laid-to-rest-log", "Laid to Rest")])
mk_album("sacrament-log",         "Sacrament",         _LOG, 2006, "machine-producer",
         [("redneck-log", "Redneck"), ("walk-with-me-in-hell-log", "Walk with Me in Hell")])
mk_album("wrath-log",             "Wrath",             _LOG, 2009, "machine-producer", [])
mk_album("resolution-log",        "Resolution",        _LOG, 2012, "machine-producer",
         [("ghost-walking-log", "Ghost Walking")])
mk_album("lamb-of-god-2020",      "Lamb of God",       _LOG, 2020, "machine-producer",
         [("checkmate-log", "Checkmate")])

mk_song("laid-to-rest-log",         "Laid to Rest",        _LOG, "ashes-of-the-wake-log", 2004,
        [("randy-blythe", "Randy Blythe", "Vocals"), ("machine-producer", "Machine", "Producer")])
mk_song("redneck-log",              "Redneck",             _LOG, "sacrament-log",         2006,
        [("randy-blythe", "Randy Blythe", "Vocals")])
mk_song("walk-with-me-in-hell-log", "Walk with Me in Hell",_LOG, "sacrament-log",         2006,
        [("randy-blythe", "Randy Blythe", "Vocals")])
mk_song("ghost-walking-log",        "Ghost Walking",       _LOG, "resolution-log",         2012,
        [("randy-blythe", "Randy Blythe", "Vocals")])
mk_song("checkmate-log",            "Checkmate",           _LOG, "lamb-of-god-2020",       2020,
        [("randy-blythe", "Randy Blythe", "Vocals")])

_person("machine-producer", "Machine")


# =============================================================================
# 15. BREAKING BENJAMIN
# =============================================================================
print("\n=== 15. Breaking Benjamin ===")
_BB = "breaking-benjamin"
mk_artist(_BB, "Breaking Benjamin", "Group", ["Rock"], "Rock", 1998,
          [("benjamin-burnley", "Benjamin Burnley", "Vocals"),
           ("aaron-fink",       "Aaron Fink",       "Guitar"),
           ("mark-klepaski",    "Mark Klepaski",    "Bass")],
          [("we-are-not-alone-bb",  "We Are Not Alone", 2004),
           ("phobia-bb",            "Phobia",           2006),
           ("dear-agony-bb",        "Dear Agony",       2009),
           ("dark-before-dawn-bb",  "Dark Before Dawn", 2015),
           ("ember-bb",             "Ember",            2018)])

mk_album("we-are-not-alone-bb",  "We Are Not Alone", _BB, 2004, "david-bendeth", [])
mk_album("phobia-bb",            "Phobia",           _BB, 2006, "david-bendeth",
         [("diary-of-jane-bb", "The Diary of Jane"), ("breath-bb", "Breath")])
mk_album("dear-agony-bb",        "Dear Agony",       _BB, 2009, "david-bendeth",
         [("i-will-not-bow-bb", "I Will Not Bow")])
mk_album("dark-before-dawn-bb",  "Dark Before Dawn", _BB, 2015, "david-bendeth",
         [("angels-fall-bb", "Angels Fall")])
mk_album("ember-bb",             "Ember",            _BB, 2018, "david-bendeth",
         [("red-cold-river-bb", "Red Cold River")])

mk_song("diary-of-jane-bb",  "The Diary of Jane", _BB, "phobia-bb",           2006,
        [("benjamin-burnley","Benjamin Burnley","Vocals"),("david-bendeth","David Bendeth","Producer")])
mk_song("breath-bb",         "Breath",            _BB, "phobia-bb",           2006,
        [("benjamin-burnley","Benjamin Burnley","Vocals")])
mk_song("i-will-not-bow-bb", "I Will Not Bow",    _BB, "dear-agony-bb",       2009,
        [("benjamin-burnley","Benjamin Burnley","Vocals")])
mk_song("angels-fall-bb",    "Angels Fall",       _BB, "dark-before-dawn-bb", 2015,
        [("benjamin-burnley","Benjamin Burnley","Vocals")])
mk_song("red-cold-river-bb", "Red Cold River",    _BB, "ember-bb",            2018,
        [("benjamin-burnley","Benjamin Burnley","Vocals")])

_person("david-bendeth", "David Bendeth")


# =============================================================================
# 16. THREE DAYS GRACE
# =============================================================================
print("\n=== 16. Three Days Grace ===")
_TDG = "three-days-grace"
mk_artist(_TDG, "Three Days Grace", "Group", ["Rock"], "Rock", 1992,
          [("adam-gontier",  "Adam Gontier",  "Vocals"),
           ("neil-sanderson","Neil Sanderson","Drums"),
           ("barry-stock",   "Barry Stock",   "Guitar"),
           ("brad-walst",    "Brad Walst",    "Bass")],
          [("three-days-grace-2003", "Three Days Grace", 2003),
           ("one-x-tdg",             "One-X",            2006),
           ("life-starts-now-tdg",   "Life Starts Now",  2009),
           ("transit-of-venus-tdg",  "Transit of Venus", 2012)])

mk_album("three-days-grace-2003", "Three Days Grace", _TDG, 2003, "gavin-brown-prod",
         [("i-hate-everything-about-you-tdg", "I Hate Everything About You")])
mk_album("one-x-tdg",             "One-X",            _TDG, 2006, "gavin-brown-prod",
         [("pain-tdg", "Pain"), ("animal-i-have-become-tdg", "Animal I Have Become")])
mk_album("life-starts-now-tdg",   "Life Starts Now",  _TDG, 2009, "gavin-brown-prod",
         [("the-good-life-tdg", "The Good Life")])
mk_album("transit-of-venus-tdg",  "Transit of Venus", _TDG, 2012, "gavin-brown-prod",
         [("painkiller-tdg", "Painkiller")])

mk_song("i-hate-everything-about-you-tdg","I Hate Everything About You",_TDG,"three-days-grace-2003",2003,
        [("adam-gontier","Adam Gontier","Vocals"),("gavin-brown-prod","Gavin Brown","Producer")])
mk_song("pain-tdg",               "Pain",                _TDG, "one-x-tdg",           2006,
        [("adam-gontier","Adam Gontier","Vocals")])
mk_song("animal-i-have-become-tdg","Animal I Have Become",_TDG, "one-x-tdg",          2006,
        [("adam-gontier","Adam Gontier","Vocals")])
mk_song("the-good-life-tdg",      "The Good Life",       _TDG, "life-starts-now-tdg", 2009,
        [("adam-gontier","Adam Gontier","Vocals")])
mk_song("painkiller-tdg",         "Painkiller",          _TDG, "transit-of-venus-tdg",2012,
        [("adam-gontier","Adam Gontier","Vocals")])

_person("gavin-brown-prod", "Gavin Brown")


# =============================================================================
# 17. SEETHER
# =============================================================================
print("\n=== 17. Seether ===")
_STH = "seether"
mk_artist(_STH, "Seether", "Group", ["Rock"], "Rock", 1999,
          [("shaun-morgan",         "Shaun Morgan",  "Vocals"),
           ("dale-stewart",         "Dale Stewart",  "Bass"),
           ("john-humphrey-seether","John Humphrey", "Drums"),
           ("troy-mclawhorn",       "Troy McLawhorn","Guitar")],
          [("disclaimer-seether",              "Disclaimer",                         2002),
           ("karma-and-effect-seether",        "Karma and Effect",                   2005),
           ("finding-beauty-negative-spaces",  "Finding Beauty in Negative Spaces",  2007),
           ("isolate-and-medicate-seether",    "Isolate and Medicate",               2014)])

mk_album("disclaimer-seether",             "Disclaimer",                        _STH, 2002, "shaun-morgan",
         [("broken-seether","Broken"),("fine-again-seether","Fine Again")])
mk_album("karma-and-effect-seether",       "Karma and Effect",                  _STH, 2005, "shaun-morgan",
         [("remedy-seether","Remedy")])
mk_album("finding-beauty-negative-spaces", "Finding Beauty in Negative Spaces", _STH, 2007, "shaun-morgan",
         [("fake-it-seether","Fake It")])
mk_album("isolate-and-medicate-seether",   "Isolate and Medicate",              _STH, 2014, "shaun-morgan",
         [("words-as-weapons-seether","Words as Weapons")])

mk_song("broken-seether",          "Broken",           _STH, "disclaimer-seether",             2002,
        [("shaun-morgan","Shaun Morgan","Vocals")])
mk_song("fine-again-seether",      "Fine Again",       _STH, "disclaimer-seether",             2002,
        [("shaun-morgan","Shaun Morgan","Vocals")])
mk_song("remedy-seether",          "Remedy",           _STH, "karma-and-effect-seether",        2005,
        [("shaun-morgan","Shaun Morgan","Vocals")])
mk_song("fake-it-seether",         "Fake It",          _STH, "finding-beauty-negative-spaces",  2007,
        [("shaun-morgan","Shaun Morgan","Vocals")])
mk_song("words-as-weapons-seether","Words as Weapons", _STH, "isolate-and-medicate-seether",    2014,
        [("shaun-morgan","Shaun Morgan","Vocals")])


# =============================================================================
# 18. PERIPHERY
# =============================================================================
print("\n=== 18. Periphery ===")
_PRP = "periphery"
mk_artist(_PRP, "Periphery", "Group", ["Alternative Rock", "Metal"], "Alternative Rock", 2005,
          [("spencer-sotelo", "Spencer Sotelo", "Vocals"),
           ("misha-mansoor",  "Misha Mansoor",  "Guitar"),
           ("jake-bowen",     "Jake Bowen",     "Guitar"),
           ("mark-holcomb",   "Mark Holcomb",   "Guitar"),
           ("matt-halpern",   "Matt Halpern",   "Drums")],
          [("periphery-2010",         "Periphery",                          2010),
           ("periphery-ii",           "Periphery II: This Time It's Personal",2012),
           ("juggernaut-alpha",        "Juggernaut: Alpha",                   2015),
           ("periphery-iv-hail-stan",  "Periphery IV: HAIL STAN",             2019),
           ("periphery-v-djent",       "Periphery V: Djent Is Not a Genre",   2023)])

mk_album("periphery-2010",        "Periphery",                           _PRP, 2010, "misha-mansoor",
         [("icarus-lives-prp","Icarus Lives!")])
mk_album("periphery-ii",          "Periphery II: This Time It's Personal",_PRP, 2012, "misha-mansoor",
         [("ragnarok-prp","Ragnarok")])
mk_album("juggernaut-alpha",       "Juggernaut: Alpha",                   _PRP, 2015, "misha-mansoor",
         [("marigold-prp","Marigold")])
mk_album("periphery-iv-hail-stan", "Periphery IV: HAIL STAN",             _PRP, 2019, "misha-mansoor",
         [("blood-eagle-prp","Blood Eagle")])
mk_album("periphery-v-djent",      "Periphery V: Djent Is Not a Genre",   _PRP, 2023, "misha-mansoor",
         [("wildfire-prp","Wildfire")])

mk_song("icarus-lives-prp", "Icarus Lives!", _PRP, "periphery-2010",        2010,
        [("spencer-sotelo","Spencer Sotelo","Vocals")])
mk_song("ragnarok-prp",     "Ragnarok",      _PRP, "periphery-ii",          2012,
        [("spencer-sotelo","Spencer Sotelo","Vocals")])
mk_song("marigold-prp",     "Marigold",      _PRP, "juggernaut-alpha",       2015,
        [("spencer-sotelo","Spencer Sotelo","Vocals")])
mk_song("blood-eagle-prp",  "Blood Eagle",   _PRP, "periphery-iv-hail-stan", 2019,
        [("spencer-sotelo","Spencer Sotelo","Vocals")])
mk_song("wildfire-prp",     "Wildfire",      _PRP, "periphery-v-djent",      2023,
        [("spencer-sotelo","Spencer Sotelo","Vocals")])


# =============================================================================
# 19. PALAYE ROYALE
# =============================================================================
print("\n=== 19. Palaye Royale ===")
_PR = "palaye-royale"
mk_artist(_PR, "Palaye Royale", "Group", ["Alternative Rock"], "Alternative Rock", 2008,
          [("remington-leith", "Remington Leith", "Vocals"),
           ("sebastian-danzig","Sebastian Danzig","Guitar"),
           ("emerson-barrett", "Emerson Barrett", "Drums")],
          [("boom-boom-room-side-a", "Boom Boom Room (Side A)", 2016),
           ("boom-boom-room-side-b", "Boom Boom Room (Side B)", 2018),
           ("the-bastards-pr",       "The Bastards",            2020),
           ("fever-dream-pr",        "Fever Dream",             2023)])

mk_album("boom-boom-room-side-a", "Boom Boom Room (Side A)", _PR, 2016, "zakk-cervini",
         [("death-dance-pr","Death Dance"),("boom-boom-pr","Boom Boom")])
mk_album("boom-boom-room-side-b", "Boom Boom Room (Side B)", _PR, 2018, "zakk-cervini", [])
mk_album("the-bastards-pr",       "The Bastards",            _PR, 2020, "zakk-cervini",
         [("anxiety-pr","Anxiety")])
mk_album("fever-dream-pr",        "Fever Dream",             _PR, 2023, "zakk-cervini",
         [("tonight-is-the-night-pr","Tonight Is the Night I Die")])

mk_song("death-dance-pr",         "Death Dance",               _PR, "boom-boom-room-side-a", 2016,
        [("remington-leith","Remington Leith","Vocals"),("zakk-cervini","Zakk Cervini","Producer")])
mk_song("boom-boom-pr",           "Boom Boom",                 _PR, "boom-boom-room-side-a", 2016,
        [("remington-leith","Remington Leith","Vocals")])
mk_song("anxiety-pr",             "Anxiety",                   _PR, "the-bastards-pr",       2020,
        [("remington-leith","Remington Leith","Vocals")])
mk_song("tonight-is-the-night-pr","Tonight Is the Night I Die",_PR, "fever-dream-pr",        2023,
        [("remington-leith","Remington Leith","Vocals")])

_person("zakk-cervini", "Zakk Cervini")


# =============================================================================
# 20. CHEVELLE
# =============================================================================
print("\n=== 20. Chevelle ===")
_CHV = "chevelle"
mk_artist(_CHV, "Chevelle", "Group", ["Rock"], "Rock", 1995,
          [("pete-loeffler",  "Pete Loeffler",  "Vocals"),
           ("sam-loeffler",   "Sam Loeffler",   "Drums"),
           ("dean-bernardini","Dean Bernardini","Bass")],
          [("wonder-whats-next-chv",     "Wonder What's Next",                    2002),
           ("this-type-of-thinking-chv", "This Type of Thinking (Could Do Us In)", 2004),
           ("vena-sera-chv",             "Vena Sera",                             2007),
           ("sci-fi-crimes-chv",         "Sci-Fi Crimes",                         2009),
           ("niratias-chv",              "NIRATIAS",                              2021)])

mk_album("wonder-whats-next-chv",     "Wonder What's Next",                     _CHV, 2002, "joe-barresi",
         [("send-the-pain-below-chv","Send the Pain Below"),("the-red-chv","The Red")])
mk_album("this-type-of-thinking-chv", "This Type of Thinking (Could Do Us In)", _CHV, 2004, "joe-barresi", [])
mk_album("vena-sera-chv",             "Vena Sera",                              _CHV, 2007, "joe-barresi", [])
mk_album("sci-fi-crimes-chv",         "Sci-Fi Crimes",                          _CHV, 2009, "joe-barresi",
         [("face-to-the-floor-chv","Face to the Floor"),("well-enough-alone-chv","Well Enough Alone")])
mk_album("niratias-chv",              "NIRATIAS",                               _CHV, 2021, "pete-loeffler", [])

mk_song("send-the-pain-below-chv","Send the Pain Below",_CHV,"wonder-whats-next-chv",2002,
        [("pete-loeffler","Pete Loeffler","Vocals"),("joe-barresi","Joe Barresi","Producer")])
mk_song("the-red-chv",            "The Red",           _CHV,"wonder-whats-next-chv",2002,
        [("pete-loeffler","Pete Loeffler","Vocals")])
mk_song("face-to-the-floor-chv",  "Face to the Floor", _CHV,"sci-fi-crimes-chv",    2009,
        [("pete-loeffler","Pete Loeffler","Vocals")])
mk_song("well-enough-alone-chv",  "Well Enough Alone", _CHV,"sci-fi-crimes-chv",    2009,
        [("pete-loeffler","Pete Loeffler","Vocals")])


# =============================================================================
# 21. EVANESCENCE
# NOTE: troy-mclawhorn already registered under Seether — add second band here
# =============================================================================
print("\n=== 21. Evanescence ===")
_EV = "evanescence"
mk_artist(_EV, "Evanescence", "Group", ["Rock"], "Rock", 1995,
          [("amy-lee",       "Amy Lee",       "Vocals"),
           ("will-hunt-ev",  "Will Hunt",     "Drums"),
           ("troy-mclawhorn","Troy McLawhorn","Guitar"),   # shared with Seether
           ("tim-mccord",    "Tim McCord",    "Bass")],
          [("fallen-ev",          "Fallen",          2003),
           ("the-open-door-ev",   "The Open Door",   2006),
           ("evanescence-2011",   "Evanescence",     2011),
           ("the-bitter-truth-ev","The Bitter Truth", 2021)])

mk_album("fallen-ev",           "Fallen",           _EV, 2003, "dave-fortman",
         [("bring-me-to-life-ev","Bring Me to Life"),
          ("my-immortal-ev","My Immortal"),
          ("going-under-ev","Going Under")])
mk_album("the-open-door-ev",    "The Open Door",    _EV, 2006, "dave-fortman",
         [("call-me-when-youre-sober-ev","Call Me When You're Sober")])
mk_album("evanescence-2011",    "Evanescence",      _EV, 2011, "dave-fortman", [])
mk_album("the-bitter-truth-ev", "The Bitter Truth", _EV, 2021, "dave-fortman",
         [("made-of-stone-ev","Made of Stone")])

mk_song("bring-me-to-life-ev",         "Bring Me to Life",         _EV,"fallen-ev",         2003,
        [("amy-lee","Amy Lee","Vocals"),("dave-fortman","Dave Fortman","Producer")])
mk_song("my-immortal-ev",              "My Immortal",              _EV,"fallen-ev",         2003,
        [("amy-lee","Amy Lee","Vocals")])
mk_song("going-under-ev",              "Going Under",              _EV,"fallen-ev",         2003,
        [("amy-lee","Amy Lee","Vocals")])
mk_song("call-me-when-youre-sober-ev", "Call Me When You're Sober",_EV,"the-open-door-ev",  2006,
        [("amy-lee","Amy Lee","Vocals")])
mk_song("made-of-stone-ev",            "Made of Stone",            _EV,"the-bitter-truth-ev",2021,
        [("amy-lee","Amy Lee","Vocals")])

_person("dave-fortman", "Dave Fortman")


# =============================================================================
# 22. SKILLET
# =============================================================================
print("\n=== 22. Skillet ===")
_SKI = "skillet"
mk_artist(_SKI, "Skillet", "Group", ["Rock"], "Rock", 1996,
          [("john-cooper",  "John Cooper",  "Vocals"),
           ("korey-cooper", "Korey Cooper", "Guitar"),
           ("jen-ledger",   "Jen Ledger",   "Drums"),
           ("seth-morrison","Seth Morrison","Guitar")],
          [("comatose-skillet",  "Comatose",   2006),
           ("awake-skillet",     "Awake",      2009),
           ("rise-skillet",      "Rise",       2013),
           ("unleashed-skillet", "Unleashed",  2016),
           ("victorious-skillet","Victorious", 2019)])

mk_album("comatose-skillet",  "Comatose",  _SKI, 2006, "john-cooper",
         [("comatose-song-skillet","Comatose")])
mk_album("awake-skillet",     "Awake",     _SKI, 2009, "john-cooper",
         [("monster-skillet","Monster"),("hero-skillet","Hero"),("awake-and-alive-skillet","Awake and Alive")])
mk_album("rise-skillet",      "Rise",      _SKI, 2013, "john-cooper", [])
mk_album("unleashed-skillet", "Unleashed", _SKI, 2016, "john-cooper",
         [("feel-invincible-skillet","Feel Invincible")])
mk_album("victorious-skillet","Victorious",_SKI, 2019, "john-cooper", [])

mk_song("comatose-song-skillet",  "Comatose",       _SKI,"comatose-skillet",2006,
        [("john-cooper","John Cooper","Vocals")])
mk_song("monster-skillet",        "Monster",        _SKI,"awake-skillet",   2009,
        [("john-cooper","John Cooper","Vocals")])
mk_song("hero-skillet",           "Hero",           _SKI,"awake-skillet",   2009,
        [("john-cooper","John Cooper","Vocals")])
mk_song("awake-and-alive-skillet","Awake and Alive", _SKI,"awake-skillet",  2009,
        [("john-cooper","John Cooper","Vocals")])
mk_song("feel-invincible-skillet","Feel Invincible", _SKI,"unleashed-skillet",2016,
        [("john-cooper","John Cooper","Vocals")])


# =============================================================================
# 23. FLOGGING MOLLY
# =============================================================================
print("\n=== 23. Flogging Molly ===")
_FM = "flogging-molly"
mk_artist(_FM, "Flogging Molly", "Group", ["Punk Rock", "Folk"], "Punk Rock", 1997,
          [("dave-king-fm",    "Dave King",     "Vocals"),
           ("bridget-regan",   "Bridget Regan", "Violin"),
           ("dennis-casey-fm", "Dennis Casey",  "Guitar"),
           ("nathen-maxwell",  "Nathen Maxwell","Bass")],
          [("swagger-fm",               "Swagger",              2000),
           ("drunken-lullabies-fm",     "Drunken Lullabies",    2002),
           ("within-a-mile-of-home-fm", "Within a Mile of Home",2004),
           ("speed-of-darkness-fm",     "Speed of Darkness",    2011),
           ("anthem-fm",                "Anthem",               2022)])

mk_album("swagger-fm",               "Swagger",               _FM, 2000, "dave-king-fm",
         [("rebels-of-the-sacred-heart-fm","Rebels of the Sacred Heart")])
mk_album("drunken-lullabies-fm",     "Drunken Lullabies",     _FM, 2002, "dave-king-fm",
         [("drunken-lullabies-song-fm","Drunken Lullabies"),
          ("whats-left-of-the-flag-fm","What's Left of the Flag")])
mk_album("within-a-mile-of-home-fm", "Within a Mile of Home", _FM, 2004, "dave-king-fm",
         [("if-i-ever-leave-this-world-alive-fm","If I Ever Leave This World Alive")])
mk_album("speed-of-darkness-fm",     "Speed of Darkness",     _FM, 2011, "dave-king-fm", [])
mk_album("anthem-fm",                "Anthem",                _FM, 2022, "dave-king-fm", [])

mk_song("rebels-of-the-sacred-heart-fm",      "Rebels of the Sacred Heart",    _FM,"swagger-fm",              2000,
        [("dave-king-fm","Dave King","Vocals")])
mk_song("drunken-lullabies-song-fm",           "Drunken Lullabies",             _FM,"drunken-lullabies-fm",    2002,
        [("dave-king-fm","Dave King","Vocals")])
mk_song("whats-left-of-the-flag-fm",           "What's Left of the Flag",       _FM,"drunken-lullabies-fm",   2002,
        [("dave-king-fm","Dave King","Vocals")])
mk_song("if-i-ever-leave-this-world-alive-fm", "If I Ever Leave This World Alive",
        _FM,"within-a-mile-of-home-fm",2004,
        [("dave-king-fm","Dave King","Vocals")])


# =============================================================================
# 24. JASON ISBELL
# =============================================================================
print("\n=== 24. Jason Isbell ===")
_JI = "jason-isbell"
mk_artist(_JI, "Jason Isbell", "Solo", ["Country", "Folk"], "Country", 2007,
          [("jason-isbell-person","Jason Isbell",  "Vocals"),
           ("amanda-shires",      "Amanda Shires", "Fiddle")],
          [("southeastern-ji",           "Southeastern",          2013),
           ("something-more-than-free-ji","Something More Than Free",2015),
           ("the-nashville-sound-ji",    "The Nashville Sound",    2017),
           ("reunions-ji",               "Reunions",               2020),
           ("weathervanes-ji",           "Weathervanes",           2023)])

mk_album("southeastern-ji",            "Southeastern",           _JI, 2013, "dave-cobb",
         [("cover-me-up-ji","Cover Me Up"),("elephant-ji","Elephant")])
mk_album("something-more-than-free-ji","Something More Than Free",_JI, 2015, "dave-cobb", [])
mk_album("the-nashville-sound-ji",     "The Nashville Sound",     _JI, 2017, "dave-cobb",
         [("if-we-were-vampires-ji","If We Were Vampires"),("white-mans-world-ji","White Man's World")])
mk_album("reunions-ji",                "Reunions",                _JI, 2020, "dave-cobb",
         [("death-wish-ji","Death Wish")])
mk_album("weathervanes-ji",            "Weathervanes",            _JI, 2023, "dave-cobb", [])

mk_song("cover-me-up-ji",        "Cover Me Up",          _JI,"southeastern-ji",        2013,
        [("jason-isbell-person","Jason Isbell","Vocals"),("dave-cobb","Dave Cobb","Producer")])
mk_song("elephant-ji",           "Elephant",             _JI,"southeastern-ji",        2013,
        [("jason-isbell-person","Jason Isbell","Vocals")])
mk_song("if-we-were-vampires-ji","If We Were Vampires",  _JI,"the-nashville-sound-ji", 2017,
        [("jason-isbell-person","Jason Isbell","Vocals")])
mk_song("white-mans-world-ji",   "White Man's World",    _JI,"the-nashville-sound-ji", 2017,
        [("jason-isbell-person","Jason Isbell","Vocals")])
mk_song("death-wish-ji",         "Death Wish",           _JI,"reunions-ji",            2020,
        [("jason-isbell-person","Jason Isbell","Vocals")])

_person("dave-cobb", "Dave Cobb")


# =============================================================================
# 25. THE MENZINGERS
# =============================================================================
print("\n=== 25. The Menzingers ===")
_MENZ = "the-menzingers"
mk_artist(_MENZ, "The Menzingers", "Group", ["Punk Rock"], "Punk Rock", 2006,
          [("greg-barnett",   "Greg Barnett",  "Vocals"),
           ("tom-may",        "Tom May",       "Vocals"),
           ("eric-keen-menz", "Eric Keen",     "Bass"),
           ("joe-godino",     "Joe Godino",    "Drums")],
          [("on-the-impossible-past-menz","On the Impossible Past", 2012),
           ("after-the-party-menz",       "After the Party",        2017),
           ("hello-exile-menz",           "Hello Exile",            2019),
           ("from-exile-menz",            "From Exile",             2021)])

mk_album("on-the-impossible-past-menz","On the Impossible Past",_MENZ,2012,"will-yip",
         [("good-things-menz","Good Things"),("bad-catholics-menz","Bad Catholics")])
mk_album("after-the-party-menz",       "After the Party",       _MENZ,2017,"will-yip",
         [("after-the-party-song-menz","After the Party"),("anna-menz","Anna")])
mk_album("hello-exile-menz",           "Hello Exile",           _MENZ,2019,"will-yip",
         [("hello-exile-song-menz","Hello Exile")])
mk_album("from-exile-menz",            "From Exile",            _MENZ,2021,"will-yip", [])

mk_song("good-things-menz",           "Good Things",   _MENZ,"on-the-impossible-past-menz",2012,
        [("greg-barnett","Greg Barnett","Vocals"),("will-yip","Will Yip","Producer")])
mk_song("bad-catholics-menz",         "Bad Catholics", _MENZ,"on-the-impossible-past-menz",2012,
        [("greg-barnett","Greg Barnett","Vocals")])
mk_song("after-the-party-song-menz",  "After the Party",_MENZ,"after-the-party-menz",      2017,
        [("greg-barnett","Greg Barnett","Vocals")])
mk_song("anna-menz",                  "Anna",          _MENZ,"after-the-party-menz",        2017,
        [("tom-may","Tom May","Vocals")])
mk_song("hello-exile-song-menz",      "Hello Exile",   _MENZ,"hello-exile-menz",            2019,
        [("greg-barnett","Greg Barnett","Vocals")])

_person("will-yip", "Will Yip")


# =============================================================================
# WRITE ALL PERSON FILES
# =============================================================================
print("\n=== Writing people files ===")
for slug, p in _people.items():
    data = {"title": p["title"], "slug": slug}
    if p["bands"]:
        data["bands"] = p["bands"]
    if p["song_credits"]:
        data["song_credits"] = p["song_credits"]
    _write(PEOPLE_DIR / f"{slug}.md", data)


# =============================================================================
# SUMMARY
# =============================================================================
print(f"\n{'='*50}")
print(f"  Files created : {_stats['created']}")
print(f"  Files skipped : {_stats['skipped']}")
print(f"{'='*50}")
