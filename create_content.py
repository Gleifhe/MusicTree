from pathlib import Path

BASE = Path("c:/repo/MusicTree/content")
for d in ["artists", "albums", "songs", "people"]:
    (BASE / d).mkdir(parents=True, exist_ok=True)

nc = {"A": 0, "AL": 0, "S": 0, "P": 0}
sk = 0


def qs(s):
    return str(s).replace("\\", "\\\\").replace('"', '\\"')


def glist(items):
    return "[" + ", ".join(f'"{x}"' for x in items) + "]"


def artist(slug, title, scene, country, formed, btype, genres, members, albums, bio=""):
    global sk
    p = BASE / "artists" / f"{slug}.md"
    if p.exists():
        sk += 1
        return
    mlines = "\n".join(
        f'  - slug: "{m[0]}"\n    name: "{qs(m[1])}"\n    role: "{m[2]}"' for m in members
    )
    alines = "\n".join(
        f'  - slug: "{a[0]}"\n    title: "{qs(a[1])}"\n    year: {a[2]}' for a in albums
    )
    bio_line = f'\nbio: "{qs(bio)}"' if bio else ""
    content = f"""---
scene: "{scene}"
title: "{qs(title)}"
country: "{country}"
formed: {formed}
band_type: "{btype}"
genres: {glist(genres)}
members:
{mlines}
albums:
{alines}{bio_line}
draft: false
---
"""
    p.write_text(content, encoding="utf-8")
    nc["A"] += 1


def alb(slug, title, aname, aslug, year, genres, songs, bio=""):
    global sk
    p = BASE / "albums" / f"{slug}.md"
    if p.exists():
        sk += 1
        return
    slines = "\n".join(
        f'  - slug: "{s[0]}"\n    title: "{qs(s[1])}"' for s in songs
    )
    bio_line = f'\nbio: "{qs(bio)}"' if bio else ""
    content = f"""---
title: "{qs(title)}"
artist: "{qs(aname)}"
artist_slug: "{aslug}"
year: {year}
genres: {glist(genres)}
songs:
{slines}{bio_line}
draft: false
---
"""
    p.write_text(content, encoding="utf-8")
    nc["AL"] += 1


def sng(slug, title, aname, aslug, altitle, alslug, year, credits, bio=""):
    global sk
    p = BASE / "songs" / f"{slug}.md"
    if p.exists():
        sk += 1
        return
    clines = "\n".join(
        f'  - person_slug: "{c[0]}"\n    person: "{qs(c[1])}"\n    role: "{c[2]}"'
        for c in credits
    )
    bio_line = f'\nbio: "{qs(bio)}"' if bio else ""
    content = f"""---
title: "{qs(title)}"
artist: "{qs(aname)}"
artist_slug: "{aslug}"
album: "{qs(altitle)}"
album_slug: "{alslug}"
year: {year}
credits:
{clines}{bio_line}
draft: false
---
"""
    p.write_text(content, encoding="utf-8")
    nc["S"] += 1


def per(slug, title, born, nat, roles, bands=None, credits=None, bio="", died=None):
    global sk
    p = BASE / "people" / f"{slug}.md"
    if p.exists():
        sk += 1
        return
    died_line = f"\ndied: {died}" if died else ""
    blines = ""
    if bands:
        blines = "\nbands:\n" + "\n".join(
            f'  - slug: "{b[0]}"\n    name: "{qs(b[1])}"\n    role: "{b[2]}"' for b in bands
        )
    clines_str = ""
    if credits:
        clines_str = "\ncredits:\n" + "\n".join(
            f'  - slug: "{c[0]}"\n    title: "{qs(c[1])}"\n    role: "{c[2]}"' for c in credits
        )
    bio_line = f'\nbio: "{qs(bio)}"' if bio else ""
    content = f"""---
title: "{qs(title)}"
born: {born}{died_line}
nationality: "{nat}"
roles: {glist(roles)}{blines}{clines_str}{bio_line}
draft: false
---
"""
    p.write_text(content, encoding="utf-8")
    nc["P"] += 1


def mk(alslug, altitle, aname, aslug, year, genres, songs_list, members,
       prod_slug=None, prod_name=None):
    songs_ref = [(s[0], s[1]) for s in songs_list]
    alb(alslug, altitle, aname, aslug, year, genres, songs_ref)
    for s in songs_list:
        credits = [(m[0], m[1], "Performer") for m in members]
        if prod_slug:
            credits.append((prod_slug, prod_name, "Producer"))
        sng(s[0], s[1], aname, aslug, altitle, alslug, year, credits)


# ===========================================================================
# BATCH 1: Robert Randolph and the Family Band
# ===========================================================================

rrfb = "robert-randolph-and-the-family-band"
rrfb_n = "Robert Randolph and the Family Band"
rrfb_m = [
    ("robert-randolph", "Robert Randolph", "Pedal Steel Guitar/Vocals"),
    ("danyel-morgan", "Danyel Morgan", "Bass"),
    ("marcus-randolph", "Marcus Randolph", "Drums"),
    ("lenesha-randolph", "Lenesha Randolph", "Vocals"),
]

artist(rrfb, rrfb_n, "Gospel/Funk", "US", 1999, "Group",
       ["Gospel", "Funk", "Blues", "Soul"], rrfb_m,
       [("unclassified", "Unclassified", 2003),
        ("colorblind", "Colorblind", 2006),
        ("we-walk-this-road", "We Walk This Road", 2010),
        ("lickety-split", "Lickety Split", 2013)])

mk("unclassified", "Unclassified", rrfb_n, rrfb, 2003, ["Gospel", "Funk", "Blues"],
   [("deliver-me", "Deliver Me"),
    ("i-need-more-love", "I Need More Love"),
    ("thrill-of-it", "Thrill of It"),
    ("the-march", "The March")], rrfb_m)

mk("colorblind", "Colorblind", rrfb_n, rrfb, 2006, ["Gospel", "Funk", "Soul"],
   [("colorblind-rrfb", "Colorblind"),
    ("aint-nothing-wrong-with-that", "Ain't Nothing Wrong with That"),
    ("mind-right", "Mind Right"),
    ("going-in-the-light", "Going in the Light")], rrfb_m)

mk("we-walk-this-road", "We Walk This Road", rrfb_n, rrfb, 2010, ["Gospel", "Blues", "Soul"],
   [("i-shall-not-walk-alone", "I Shall Not Walk Alone"),
    ("traveling-shoes", "Traveling Shoes"),
    ("dont-let-it-be-too-late", "Don't Let It Be Too Late"),
    ("pray-on", "Pray On")], rrfb_m)

mk("lickety-split", "Lickety Split", rrfb_n, rrfb, 2013, ["Gospel", "Funk", "Blues"],
   [("lickety-split-rrfb", "Lickety Split"),
    ("brand-new-wayo", "Brand New Wayo"),
    ("one-more-chance-rrfb", "One More Chance"),
    ("im-gonna-love-you-more", "I'm Gonna Love You More")], rrfb_m)

# ===========================================================================
# BATCH 2: Canadian Bands
# ===========================================================================

# --- Billy Talent ---
bt = "billy-talent"
bt_n = "Billy Talent"
bt_m = [
    ("benjamin-kowalewicz", "Benjamin Kowalewicz", "Vocals"),
    ("ian-d-sa", "Ian D'Sa", "Guitar/Vocals"),
    ("jonathan-gallant", "Jonathan Gallant", "Bass"),
    ("aaron-solowoniuk", "Aaron Solowoniuk", "Drums"),
]

artist(bt, bt_n, "Alternative Rock", "CA", 1999, "Group",
       ["Alternative Rock", "Punk Rock", "Post-Hardcore"], bt_m,
       [("billy-talent-st", "Billy Talent", 2003),
        ("billy-talent-ii", "Billy Talent II", 2006),
        ("billy-talent-iii", "Billy Talent III", 2009)])

mk("billy-talent-st", "Billy Talent", bt_n, bt, 2003, ["Punk Rock", "Alternative Rock"],
   [("try-honesty", "Try Honesty"),
    ("river-below", "River Below"),
    ("nothing-to-lose-bt", "Nothing to Lose"),
    ("the-ex-bt", "The Ex")], bt_m)

mk("billy-talent-ii", "Billy Talent II", bt_n, bt, 2006, ["Punk Rock", "Alternative Rock"],
   [("fallen-leaves", "Fallen Leaves"),
    ("devil-in-a-midnight-mass", "Devil in a Midnight Mass"),
    ("worker-bees", "Worker Bees"),
    ("red-flag-bt", "Red Flag")], bt_m)

mk("billy-talent-iii", "Billy Talent III", bt_n, bt, 2009, ["Punk Rock", "Alternative Rock"],
   [("rusted-from-the-rain", "Rusted from the Rain"),
    ("saint-veronika", "Saint Veronika"),
    ("diamond-on-a-landmine", "Diamond on a Landmine"),
    ("surrender-bt", "Surrender")], bt_m)

# --- Nickelback ---
nb = "nickelback"
nb_n = "Nickelback"
nb_m = [
    ("chad-kroeger", "Chad Kroeger", "Vocals/Guitar"),
    ("ryan-peake", "Ryan Peake", "Guitar/Vocals"),
    ("mike-kroeger", "Mike Kroeger", "Bass"),
    ("daniel-adair", "Daniel Adair", "Drums"),
]

artist(nb, nb_n, "Rock", "CA", 1995, "Group",
       ["Hard Rock", "Post-Grunge", "Alternative Rock"], nb_m,
       [("silver-side-up", "Silver Side Up", 2001),
        ("the-long-road", "The Long Road", 2003),
        ("all-the-right-reasons", "All the Right Reasons", 2005)])

mk("silver-side-up", "Silver Side Up", nb_n, nb, 2001, ["Post-Grunge", "Hard Rock"],
   [("how-you-remind-me", "How You Remind Me"),
    ("too-bad-nb", "Too Bad"),
    ("never-again-nb", "Never Again"),
    ("woke-up-this-morning-nb", "Woke Up This Morning")], nb_m)

mk("the-long-road", "The Long Road", nb_n, nb, 2003, ["Post-Grunge", "Hard Rock"],
   [("someday-nb", "Someday"),
    ("figured-you-out", "Figured You Out"),
    ("feelin-way-too-damn-good", "Feelin' Way Too Damn Good"),
    ("animals-nb", "Animals")], nb_m)

mk("all-the-right-reasons", "All the Right Reasons", nb_n, nb, 2005,
   ["Hard Rock", "Post-Grunge"],
   [("photograph-nb", "Photograph"),
    ("far-away-nb", "Far Away"),
    ("rockstar-nb", "Rockstar"),
    ("savin-me", "Savin' Me")], nb_m)

# --- The Tragically Hip ---
th = "tragically-hip"
th_n = "The Tragically Hip"
th_m = [
    ("gordon-downie", "Gordon Downie", "Vocals"),
    ("rob-baker", "Rob Baker", "Guitar"),
    ("paul-langlois", "Paul Langlois", "Guitar"),
    ("gord-sinclair", "Gord Sinclair", "Bass"),
    ("johnny-fay", "Johnny Fay", "Drums"),
]

artist(th, th_n, "Rock", "CA", 1983, "Group",
       ["Alternative Rock", "Roots Rock", "Indie Rock"], th_m,
       [("up-to-here", "Up to Here", 1989),
        ("fully-completely", "Fully Completely", 1992),
        ("phantom-power", "Phantom Power", 1998)])

mk("up-to-here", "Up to Here", th_n, th, 1989, ["Alternative Rock", "Roots Rock"],
   [("blow-at-high-dough", "Blow at High Dough"),
    ("new-orleans-is-sinking", "New Orleans Is Sinking"),
    ("38-years-old", "38 Years Old"),
    ("boots-or-hearts", "Boots or Hearts")], th_m)

mk("fully-completely", "Fully Completely", th_n, th, 1992, ["Alternative Rock", "Roots Rock"],
   [("courage-th", "Courage"),
    ("fifty-mission-cap", "Fifty-Mission Cap"),
    ("wheat-kings", "Wheat Kings"),
    ("at-the-hundredth-meridian", "At the Hundredth Meridian")], th_m)

mk("phantom-power", "Phantom Power", th_n, th, 1998, ["Alternative Rock", "Roots Rock"],
   [("poets-th", "Poets"),
    ("bobcaygeon", "Bobcaygeon"),
    ("fireworks-th", "Fireworks"),
    ("something-on", "Something On")], th_m)

# --- Rush ---
rsh = "rush"
rsh_n = "Rush"
rsh_mem_rutsey = [
    ("geddy-lee", "Geddy Lee", "Vocals/Bass/Keyboards"),
    ("alex-lifeson", "Alex Lifeson", "Guitar"),
    ("john-rutsey", "John Rutsey", "Drums"),
]
rsh_mem_peart = [
    ("geddy-lee", "Geddy Lee", "Vocals/Bass/Keyboards"),
    ("alex-lifeson", "Alex Lifeson", "Guitar"),
    ("neil-peart", "Neil Peart", "Drums/Percussion"),
]

artist(rsh, rsh_n, "Rock", "CA", 1968, "Group",
       ["Progressive Rock", "Hard Rock", "Heavy Metal"], rsh_mem_peart,
       [("rush-st", "Rush", 1974),
        ("2112", "2112", 1976),
        ("moving-pictures", "Moving Pictures", 1981)])

mk("rush-st", "Rush", rsh_n, rsh, 1974, ["Hard Rock", "Blues Rock"],
   [("finding-my-way-rsh", "Finding My Way"),
    ("need-some-love-rsh", "Need Some Love"),
    ("before-and-after-rsh", "Before and After"),
    ("working-man-rsh", "Working Man")], rsh_mem_rutsey)

mk("2112", "2112", rsh_n, rsh, 1976, ["Progressive Rock", "Hard Rock"],
   [("2112-overture", "2112 Overture"),
    ("the-temples-of-syrinx", "The Temples of Syrinx"),
    ("passage-to-bangkok", "A Passage to Bangkok"),
    ("something-for-nothing-rsh", "Something for Nothing")], rsh_mem_peart)

mk("moving-pictures", "Moving Pictures", rsh_n, rsh, 1981, ["Progressive Rock", "Hard Rock"],
   [("tom-sawyer", "Tom Sawyer"),
    ("red-barchetta", "Red Barchetta"),
    ("yyz", "YYZ"),
    ("limelight-rsh", "Limelight")], rsh_mem_peart)

# --- Arcade Fire ---
af = "arcade-fire"
af_n = "Arcade Fire"
af_m = [
    ("win-butler", "Win Butler", "Vocals/Guitar"),
    ("regine-chassagne", "Régine Chassagne", "Vocals/Keyboards"),
    ("richard-reed-parry", "Richard Reed Parry", "Multi-Instrumentalist"),
    ("tim-kingsbury", "Tim Kingsbury", "Bass/Guitar"),
    ("jeremy-gara", "Jeremy Gara", "Drums"),
    ("william-butler", "William Butler", "Multi-Instrumentalist"),
]

artist(af, af_n, "Indie Rock", "CA", 2001, "Group",
       ["Indie Rock", "Art Rock", "Chamber Pop"], af_m,
       [("funeral", "Funeral", 2004),
        ("the-suburbs", "The Suburbs", 2010),
        ("reflektor", "Reflektor", 2013)])

mk("funeral", "Funeral", af_n, af, 2004, ["Indie Rock", "Chamber Pop"],
   [("neighborhood-1-tunnels", "Neighbourhood #1 (Tunnels)"),
    ("laika-af", "Laika"),
    ("wake-up-af", "Wake Up"),
    ("rebellion-lies", "Rebellion (Lies)")], af_m)

mk("the-suburbs", "The Suburbs", af_n, af, 2010, ["Indie Rock", "Art Rock"],
   [("the-suburbs-af", "The Suburbs"),
    ("ready-to-start", "Ready to Start"),
    ("sprawl-ii", "Sprawl II (Mountains Beyond Mountains)"),
    ("we-used-to-wait", "We Used to Wait")], af_m)

mk("reflektor", "Reflektor", af_n, af, 2013, ["Art Rock", "Dance Rock"],
   [("reflektor-af", "Reflektor"),
    ("here-comes-the-night-time", "Here Comes the Night Time"),
    ("afterlife-af", "Afterlife"),
    ("supersymmetry", "Supersymmetry")], af_m)

# --- The Weeknd ---
tw = "the-weeknd"
tw_n = "The Weeknd"
tw_m = [("abel-tesfaye", "Abel Tesfaye", "Vocals")]

artist(tw, tw_n, "R&B/Pop", "CA", 2009, "Solo",
       ["R&B", "Pop", "Alternative R&B", "Dark Pop"], tw_m,
       [("kiss-land", "Kiss Land", 2013),
        ("beauty-behind-the-madness", "Beauty Behind the Madness", 2015),
        ("after-hours", "After Hours", 2020)])

mk("kiss-land", "Kiss Land", tw_n, tw, 2013, ["R&B", "Alternative R&B"],
   [("love-i-never-had", "Love I Never Had"),
    ("belong-to-the-world", "Belong to the World"),
    ("adaptation-tw", "Adaptation"),
    ("kiss-land-tw", "Kiss Land")], tw_m)

mk("beauty-behind-the-madness", "Beauty Behind the Madness", tw_n, tw, 2015, ["R&B", "Pop"],
   [("cant-feel-my-face", "Can't Feel My Face"),
    ("earned-it", "Earned It"),
    ("the-hills-tw", "The Hills"),
    ("in-the-night-tw", "In the Night")], tw_m)

mk("after-hours", "After Hours", tw_n, tw, 2020, ["R&B", "Dark Pop"],
   [("blinding-lights", "Blinding Lights"),
    ("heartless-tw", "Heartless"),
    ("save-your-tears", "Save Your Tears"),
    ("after-hours-tw", "After Hours")], tw_m)

# --- Neil Young ---
ny = "neil-young"
ny_n = "Neil Young"
ny_m = [("neil-young-person", "Neil Young", "Vocals/Guitar")]

artist(ny, ny_n, "Rock", "CA", 1966, "Solo",
       ["Rock", "Folk Rock", "Country Rock", "Soft Rock"], ny_m,
       [("after-the-gold-rush", "After the Gold Rush", 1970),
        ("harvest-ny", "Harvest", 1972),
        ("rust-never-sleeps", "Rust Never Sleeps", 1979)])

mk("after-the-gold-rush", "After the Gold Rush", ny_n, ny, 1970,
   ["Folk Rock", "Country Rock"],
   [("tell-me-why-ny", "Tell Me Why"),
    ("after-the-gold-rush-ny", "After the Gold Rush"),
    ("only-love-can-break-your-heart", "Only Love Can Break Your Heart"),
    ("southern-man-ny", "Southern Man")], ny_m)

mk("harvest-ny", "Harvest", ny_n, ny, 1972, ["Country Rock", "Soft Rock"],
   [("out-on-the-weekend", "Out on the Weekend"),
    ("harvest-song", "Harvest"),
    ("old-man-ny", "Old Man"),
    ("heart-of-gold-ny", "Heart of Gold")], ny_m)

mk("rust-never-sleeps", "Rust Never Sleeps", ny_n, ny, 1979, ["Rock", "Folk Rock"],
   [("my-my-hey-hey", "My My, Hey Hey (Out of the Blue)"),
    ("thrasher-ny", "Thrasher"),
    ("pocahontas-ny", "Pocahontas"),
    ("hey-hey-my-my", "Hey Hey, My My (Into the Black)")], ny_m)

# --- Joni Mitchell ---
jm = "joni-mitchell"
jm_n = "Joni Mitchell"
jm_m = [("joni-mitchell-person", "Joni Mitchell", "Vocals/Guitar/Piano")]

artist(jm, jm_n, "Folk/Pop", "CA", 1964, "Solo",
       ["Folk", "Pop", "Jazz", "Art Rock"], jm_m,
       [("blue-jm", "Blue", 1971),
        ("court-and-spark", "Court and Spark", 1974),
        ("hejira", "Hejira", 1976)])

mk("blue-jm", "Blue", jm_n, jm, 1971, ["Folk", "Pop"],
   [("all-i-want-jm", "All I Want"),
    ("my-old-man-jm", "My Old Man"),
    ("little-green-jm", "Little Green"),
    ("carey-jm", "Carey")], jm_m)

mk("court-and-spark", "Court and Spark", jm_n, jm, 1974, ["Pop", "Jazz"],
   [("court-and-spark-jm", "Court and Spark"),
    ("help-me-jm", "Help Me"),
    ("free-man-in-paris-jm", "Free Man in Paris"),
    ("raised-on-robbery-jm", "Raised on Robbery")], jm_m)

mk("hejira", "Hejira", jm_n, jm, 1976, ["Folk", "Jazz"],
   [("coyote-jm", "Coyote"),
    ("amelia-jm", "Amelia"),
    ("song-for-sharon-jm", "Song for Sharon"),
    ("hejira-jm", "Hejira")], jm_m)

# --- Broken Social Scene ---
bss = "broken-social-scene"
bss_n = "Broken Social Scene"
bss_m = [
    ("kevin-drew", "Kevin Drew", "Vocals/Guitar"),
    ("brendan-canning", "Brendan Canning", "Vocals/Bass"),
    ("emily-haines", "Emily Haines", "Vocals/Keyboards"),
    ("leslie-feist", "Leslie Feist", "Vocals/Guitar"),
    ("jason-collett", "Jason Collett", "Vocals/Guitar"),
    ("andrew-whiteman", "Andrew Whiteman", "Guitar"),
    ("charles-spearin", "Charles Spearin", "Bass/Trumpet"),
]

artist(bss, bss_n, "Indie Rock", "CA", 1999, "Group",
       ["Indie Rock", "Art Rock", "Post-Rock"], bss_m,
       [("you-forgot-it-in-people", "You Forgot It in People", 2002),
        ("broken-social-scene-st", "Broken Social Scene", 2005),
        ("forgiveness-rock-record", "Forgiveness Rock Record", 2010)])

mk("you-forgot-it-in-people", "You Forgot It in People", bss_n, bss, 2002,
   ["Indie Rock", "Post-Rock"],
   [("anthems-for-a-seventeen-year-old-girl", "Anthems for a Seventeen Year-Old Girl"),
    ("cause-equals-time", "Cause = Time"),
    ("almost-crimes", "Almost Crimes"),
    ("lovers-spit", "Lover's Spit")], bss_m)

mk("broken-social-scene-st", "Broken Social Scene", bss_n, bss, 2005,
   ["Indie Rock", "Art Rock"],
   [("ibi-dreams-of-pavement", "Ibi Dreams of Pavement (A Better Day)"),
    ("7-4-shoreline", "7/4 (Shoreline)"),
    ("marbled-sea", "Marbled Sea"),
    ("its-all-gonna-break", "It's All Gonna Break")], bss_m)

mk("forgiveness-rock-record", "Forgiveness Rock Record", bss_n, bss, 2010,
   ["Indie Rock", "Art Rock"],
   [("forced-to-love", "Forced to Love"),
    ("all-to-all", "All to All"),
    ("world-sick", "World Sick"),
    ("romance-to-the-grave", "Romance to the Grave")], bss_m)

# --- Metric ---
met = "metric"
met_n = "Metric"
met_m = [
    ("emily-haines", "Emily Haines", "Vocals/Keyboards"),
    ("james-shaw", "James Shaw", "Guitar"),
    ("joshua-winstead", "Joshua Winstead", "Bass"),
    ("joules-scott-key", "Joules Scott-Key", "Drums"),
]

artist(met, met_n, "Indie Rock", "CA", 1998, "Group",
       ["Indie Rock", "New Wave", "Synth-Pop", "Alternative Rock"], met_m,
       [("old-world-underground", "Old World Underground, Where Are You Now?", 2003),
        ("live-it-out", "Live It Out", 2005),
        ("fantasies", "Fantasies", 2009)])

mk("old-world-underground", "Old World Underground, Where Are You Now?", met_n, met, 2003,
   ["Indie Rock", "New Wave"],
   [("dead-disco-met", "Dead Disco"),
    ("combat-baby-met", "Combat Baby"),
    ("gold-guns-girls-met", "Gold Guns Girls"),
    ("succexy-met", "Succexy")], met_m)

mk("live-it-out", "Live It Out", met_n, met, 2005, ["Indie Rock", "New Wave"],
   [("monster-hospital", "Monster Hospital"),
    ("the-list-met", "The List"),
    ("poster-of-a-girl", "Poster of a Girl"),
    ("handshakes-met", "Handshakes")], met_m)

mk("fantasies", "Fantasies", met_n, met, 2009, ["Indie Rock", "Synth-Pop"],
   [("help-im-alive", "Help I'm Alive"),
    ("sick-muse", "Sick Muse"),
    ("gimme-sympathy", "Gimme Sympathy"),
    ("stadium-love", "Stadium Love")], met_m)

# --- Barenaked Ladies ---
bnl = "barenaked-ladies"
bnl_n = "Barenaked Ladies"
bnl_m = [
    ("steven-page", "Steven Page", "Vocals/Guitar"),
    ("ed-robertson", "Ed Robertson", "Vocals/Guitar"),
    ("jim-creeggan", "Jim Creeggan", "Bass"),
    ("kevin-hearn", "Kevin Hearn", "Keyboards"),
    ("tyler-stewart", "Tyler Stewart", "Drums"),
]

artist(bnl, bnl_n, "Pop Rock", "CA", 1988, "Group",
       ["Pop Rock", "Alternative Rock", "Comedy Rock"], bnl_m,
       [("gordon-bnl", "Gordon", 1992),
        ("stunt-bnl", "Stunt", 1998),
        ("maroon-bnl", "Maroon", 2000)])

mk("gordon-bnl", "Gordon", bnl_n, bnl, 1992, ["Pop Rock", "Alternative Rock"],
   [("brian-wilson-bnl", "Brian Wilson"),
    ("if-i-had-1000000", "If I Had $1000000"),
    ("grade-9-bnl", "Grade 9"),
    ("what-a-good-boy", "What a Good Boy")], bnl_m)

mk("stunt-bnl", "Stunt", bnl_n, bnl, 1998, ["Pop Rock", "Alternative Rock"],
   [("one-week-bnl", "One Week"),
    ("its-all-been-done", "It's All Been Done"),
    ("leave-bnl", "Leave"),
    ("call-and-answer", "Call and Answer")], bnl_m)

mk("maroon-bnl", "Maroon", bnl_n, bnl, 2000, ["Pop Rock", "Alternative Rock"],
   [("pinch-me-bnl", "Pinch Me"),
    ("too-little-too-late-bnl", "Too Little Too Late"),
    ("the-old-apartment", "The Old Apartment"),
    ("never-is-enough", "Never Is Enough")], bnl_m)

# --- Alanis Morissette ---
ala = "alanis-morissette"
ala_n = "Alanis Morissette"
ala_m = [("alanis-morissette-person", "Alanis Morissette", "Vocals/Guitar/Harmonica")]

artist(ala, ala_n, "Alternative Rock", "CA", 1991, "Solo",
       ["Alternative Rock", "Post-Grunge", "Pop Rock"], ala_m,
       [("jagged-little-pill", "Jagged Little Pill", 1995),
        ("supposed-former-infatuation-junkie", "Supposed Former Infatuation Junkie", 1998),
        ("under-rug-swept", "Under Rug Swept", 2002)])

mk("jagged-little-pill", "Jagged Little Pill", ala_n, ala, 1995,
   ["Alternative Rock", "Post-Grunge"],
   [("you-oughta-know", "You Oughta Know"),
    ("hand-in-my-pocket", "Hand in My Pocket"),
    ("ironic-am", "Ironic"),
    ("you-learn", "You Learn")], ala_m)

mk("supposed-former-infatuation-junkie", "Supposed Former Infatuation Junkie",
   ala_n, ala, 1998, ["Alternative Rock", "Pop Rock"],
   [("thank-u-am", "Thank U"),
    ("so-pure-am", "So Pure"),
    ("joining-you-am", "Joining You"),
    ("unsent-am", "Unsent")], ala_m)

mk("under-rug-swept", "Under Rug Swept", ala_n, ala, 2002,
   ["Alternative Rock", "Pop Rock"],
   [("hands-clean-am", "Hands Clean"),
    ("precious-illusions-am", "Precious Illusions"),
    ("so-unsexy-am", "So Unsexy"),
    ("narcissus-am", "Narcissus")], ala_m)

# --- Avril Lavigne ---
avr = "avril-lavigne"
avr_n = "Avril Lavigne"
avr_m = [("avril-lavigne-person", "Avril Lavigne", "Vocals/Guitar")]

artist(avr, avr_n, "Pop Rock", "CA", 1999, "Solo",
       ["Pop Rock", "Punk Pop", "Alternative Rock"], avr_m,
       [("let-go-avr", "Let Go", 2002),
        ("under-my-skin", "Under My Skin", 2004),
        ("the-best-damn-thing", "The Best Damn Thing", 2007)])

mk("let-go-avr", "Let Go", avr_n, avr, 2002, ["Pop Rock", "Punk Pop"],
   [("complicated-avr", "Complicated"),
    ("sk8er-boi", "Sk8er Boi"),
    ("im-with-you-avr", "I'm with You"),
    ("losing-grip-avr", "Losing Grip")], avr_m)

mk("under-my-skin", "Under My Skin", avr_n, avr, 2004, ["Pop Rock", "Punk Pop"],
   [("dont-tell-me-avr", "Don't Tell Me"),
    ("my-happy-ending-avr", "My Happy Ending"),
    ("he-wasnt-avr", "He Wasn't"),
    ("nobodys-home-avr", "Nobody's Home")], avr_m)

mk("the-best-damn-thing", "The Best Damn Thing", avr_n, avr, 2007, ["Pop Rock", "Punk Pop"],
   [("girlfriend-avr", "Girlfriend"),
    ("when-youre-gone-avr", "When You're Gone"),
    ("i-can-do-better-avr", "I Can Do Better"),
    ("hot-avr", "Hot")], avr_m)

# --- Sum 41 ---
s41 = "sum-41"
s41_n = "Sum 41"
s41_m = [
    ("deryck-whibley", "Deryck Whibley", "Vocals/Guitar"),
    ("dave-baksh", "Dave Baksh", "Guitar/Vocals"),
    ("jason-mccaslin", "Jason McCaslin", "Bass"),
    ("tom-thacker", "Tom Thacker", "Guitar"),
    ("frank-zummo", "Frank Zummo", "Drums"),
]

artist(s41, s41_n, "Punk Rock", "CA", 1996, "Group",
       ["Punk Rock", "Pop Punk", "Heavy Metal"], s41_m,
       [("all-killer-no-filler", "All Killer No Filler", 2001),
        ("chuck-s41", "Chuck", 2004),
        ("screaming-bloody-murder", "Screaming Bloody Murder", 2011)])

mk("all-killer-no-filler", "All Killer No Filler", s41_n, s41, 2001,
   ["Pop Punk", "Punk Rock"],
   [("fat-lip", "Fat Lip"),
    ("in-too-deep-s41", "In Too Deep"),
    ("motivation-s41", "Motivation"),
    ("pain-for-pleasure-s41", "Pain for Pleasure")], s41_m)

mk("chuck-s41", "Chuck", s41_n, s41, 2004, ["Punk Rock", "Heavy Metal"],
   [("were-all-to-blame", "We're All to Blame"),
    ("slipping-away-s41", "Slipping Away"),
    ("some-say-s41", "Some Say"),
    ("angels-with-dirty-faces-s41", "Angels with Dirty Faces")], s41_m)

mk("screaming-bloody-murder", "Screaming Bloody Murder", s41_n, s41, 2011,
   ["Heavy Metal", "Punk Rock"],
   [("blood-in-my-eyes-s41", "Blood in My Eyes"),
    ("sick-of-everyone-s41", "Sick of Everyone"),
    ("starving-for-change-s41", "Starving for Change"),
    ("the-jester-s41", "The Jester")], s41_m)

# --- Our Lady Peace ---
olp = "our-lady-peace"
olp_n = "Our Lady Peace"
olp_m = [
    ("raine-maida", "Raine Maida", "Vocals"),
    ("mike-turner", "Mike Turner", "Guitar"),
    ("jeremy-taggart", "Jeremy Taggart", "Drums"),
    ("duncan-coutts", "Duncan Coutts", "Bass"),
]

artist(olp, olp_n, "Alternative Rock", "CA", 1992, "Group",
       ["Alternative Rock", "Post-Grunge", "Art Rock"], olp_m,
       [("naveed", "Naveed", 1994),
        ("clumsy-olp", "Clumsy", 1997),
        ("happiness-is-not-a-fish", "Happiness Is Not a Fish That You Can Catch", 1999)])

mk("naveed", "Naveed", olp_n, olp, 1994, ["Alternative Rock", "Post-Grunge"],
   [("starseed-olp", "Starseed"),
    ("naveed-olp", "Naveed"),
    ("hope-olp", "Hope"),
    ("is-it-safe-olp", "Is It Safe?")], olp_m)

mk("clumsy-olp", "Clumsy", olp_n, olp, 1997, ["Alternative Rock", "Post-Grunge"],
   [("supermans-dead-olp", "Superman's Dead"),
    ("clumsy-song-olp", "Clumsy"),
    ("4am-olp", "4 AM"),
    ("automatic-flowers-olp", "Automatic Flowers")], olp_m)

mk("happiness-is-not-a-fish", "Happiness Is Not a Fish That You Can Catch",
   olp_n, olp, 1999, ["Alternative Rock", "Art Rock"],
   [("is-anybody-home-olp", "Is Anybody Home?"),
    ("thief-olp", "Thief"),
    ("are-you-sad-olp", "Are You Sad?"),
    ("life-olp", "Life")], olp_m)

# --- Tegan and Sara ---
tns = "tegan-and-sara"
tns_n = "Tegan and Sara"
tns_m = [
    ("tegan-quin", "Tegan Quin", "Vocals/Guitar"),
    ("sara-quin", "Sara Quin", "Vocals/Guitar"),
]

artist(tns, tns_n, "Indie Pop", "CA", 1995, "Group",
       ["Indie Pop", "Alternative Rock", "New Wave"], tns_m,
       [("so-jealous", "So Jealous", 2004),
        ("the-con-tns", "The Con", 2007),
        ("heartthrob-tns", "Heartthrob", 2013)])

mk("so-jealous", "So Jealous", tns_n, tns, 2004, ["Indie Pop", "Alternative Rock"],
   [("walking-with-a-ghost", "Walking with a Ghost"),
    ("you-wouldnt-like-me-tns", "You Wouldn't Like Me"),
    ("so-jealous-tns", "So Jealous"),
    ("city-girl-tns", "City Girl")], tns_m)

mk("the-con-tns", "The Con", tns_n, tns, 2007, ["Indie Pop", "Alternative Rock"],
   [("back-in-your-head", "Back in Your Head"),
    ("the-con-tns-song", "The Con"),
    ("burn-your-life-down-tns", "Burn Your Life Down"),
    ("call-it-off-tns", "Call It Off")], tns_m)

mk("heartthrob-tns", "Heartthrob", tns_n, tns, 2013, ["Indie Pop", "New Wave", "Synth-Pop"],
   [("closer-tns", "Closer"),
    ("i-was-a-fool-tns", "I Was a Fool"),
    ("im-not-your-hero-tns", "I'm Not Your Hero"),
    ("now-im-all-messed-up-tns", "Now I'm All Messed Up")], tns_m)

# --- Feist ---
fst = "feist"
fst_n = "Feist"
fst_m = [("leslie-feist", "Leslie Feist", "Vocals/Guitar")]

artist(fst, fst_n, "Indie Pop", "CA", 1999, "Solo",
       ["Indie Pop", "Folk Pop", "Baroque Pop"], fst_m,
       [("let-it-die-fst", "Let It Die", 2004),
        ("the-reminder", "The Reminder", 2007),
        ("metals-fst", "Metals", 2011)])

mk("let-it-die-fst", "Let It Die", fst_n, fst, 2004, ["Indie Pop", "Folk Pop"],
   [("inside-and-out-fst", "Inside and Out"),
    ("mushaboom-fst", "Mushaboom"),
    ("let-it-die-fst-song", "Let It Die"),
    ("leisure-suite-fst", "Leisure Suite")], fst_m)

mk("the-reminder", "The Reminder", fst_n, fst, 2007, ["Indie Pop", "Folk Pop"],
   [("1234-fst", "1234"),
    ("my-moon-my-man-fst", "My Moon My Man"),
    ("i-feel-it-all-fst", "I Feel It All"),
    ("past-in-present-fst", "Past in Present")], fst_m)

mk("metals-fst", "Metals", fst_n, fst, 2011, ["Indie Folk", "Art Rock"],
   [("how-come-you-never-go-there-fst", "How Come You Never Go There"),
    ("anti-pioneer-fst", "Anti-Pioneer"),
    ("graveyard-fst", "Graveyard"),
    ("the-bad-in-each-other-fst", "The Bad in Each Other")], fst_m)

# --- Sarah McLachlan ---
smc = "sarah-mclachlan"
smc_n = "Sarah McLachlan"
smc_m = [("sarah-mclachlan-person", "Sarah McLachlan", "Vocals/Piano/Guitar")]

artist(smc, smc_n, "Pop", "CA", 1987, "Solo",
       ["Pop", "Soft Rock", "Adult Contemporary"], smc_m,
       [("fumbling-towards-ecstasy", "Fumbling Towards Ecstasy", 1993),
        ("surfacing-smc", "Surfacing", 1997),
        ("afterglow-smc", "Afterglow", 2003)])

mk("fumbling-towards-ecstasy", "Fumbling Towards Ecstasy", smc_n, smc, 1993,
   ["Pop", "Soft Rock"],
   [("possession-smc", "Possession"),
    ("hold-on-smc", "Hold On"),
    ("good-enough-smc", "Good Enough"),
    ("the-path-of-thorns-smc", "The Path of Thorns (Terms)")], smc_m)

mk("surfacing-smc", "Surfacing", smc_n, smc, 1997, ["Pop", "Soft Rock"],
   [("building-a-mystery-smc", "Building a Mystery"),
    ("angel-smc", "Angel"),
    ("adia-smc", "Adia"),
    ("sweet-surrender-smc", "Sweet Surrender")], smc_m)

mk("afterglow-smc", "Afterglow", smc_n, smc, 2003, ["Pop", "Adult Contemporary"],
   [("world-on-fire-smc", "World on Fire"),
    ("fallen-smc", "Fallen"),
    ("stupid-smc", "Stupid"),
    ("dear-god-smc", "Dear God")], smc_m)

# --- Leonard Cohen ---
lco = "leonard-cohen"
lco_n = "Leonard Cohen"
lco_m = [("leonard-cohen-person", "Leonard Cohen", "Vocals/Guitar")]

artist(lco, lco_n, "Folk", "CA", 1967, "Solo",
       ["Folk", "Pop", "Rock", "Classical"], lco_m,
       [("songs-of-leonard-cohen", "Songs of Leonard Cohen", 1967),
        ("songs-of-love-and-hate", "Songs of Love and Hate", 1971),
        ("im-your-man", "I'm Your Man", 1988)])

mk("songs-of-leonard-cohen", "Songs of Leonard Cohen", lco_n, lco, 1967, ["Folk", "Pop"],
   [("suzanne-lco", "Suzanne"),
    ("master-song-lco", "Master Song"),
    ("sisters-of-mercy-lco", "Sisters of Mercy"),
    ("hey-thats-no-way-to-say-goodbye-lco", "Hey, That's No Way to Say Goodbye")], lco_m)

mk("songs-of-love-and-hate", "Songs of Love and Hate", lco_n, lco, 1971, ["Folk", "Pop"],
   [("avalanche-lco", "Avalanche"),
    ("last-years-man-lco", "Last Year's Man"),
    ("famous-blue-raincoat-lco", "Famous Blue Raincoat"),
    ("joan-of-arc-lco", "Joan of Arc")], lco_m)

mk("im-your-man", "I'm Your Man", lco_n, lco, 1988, ["Pop", "Rock"],
   [("first-we-take-manhattan-lco", "First We Take Manhattan"),
    ("aint-no-cure-for-love-lco", "Ain't No Cure for Love"),
    ("everywhere-lco", "Everywhere"),
    ("im-your-man-lco", "I'm Your Man")], lco_m)

# --- Death from Above 1979 ---
dfa = "death-from-above-1979"
dfa_n = "Death from Above 1979"
dfa_m = [
    ("sebastien-grainger", "Sebastien Grainger", "Vocals/Drums"),
    ("jesse-f-keeler", "Jesse F. Keeler", "Bass/Keyboards"),
]

artist(dfa, dfa_n, "Alternative Rock", "CA", 2001, "Group",
       ["Dance-Punk", "Noise Rock", "Electronic Rock"], dfa_m,
       [("youre-a-woman-im-a-machine", "You're a Woman, I'm a Machine", 2004),
        ("the-physical-world", "The Physical World", 2014)])

mk("youre-a-woman-im-a-machine", "You're a Woman, I'm a Machine", dfa_n, dfa, 2004,
   ["Dance-Punk", "Noise Rock"],
   [("romantic-rights-dfa", "Romantic Rights"),
    ("going-steady-dfa", "Going Steady"),
    ("black-history-month-dfa", "Black History Month"),
    ("pull-out-dfa", "Pull Out")], dfa_m)

mk("the-physical-world", "The Physical World", dfa_n, dfa, 2014,
   ["Dance-Punk", "Electronic Rock"],
   [("cheap-talk-dfa", "Cheap Talk"),
    ("white-is-red-dfa", "White Is Red"),
    ("statues-dfa", "Statues"),
    ("got-a-woman-dfa", "Got a Woman")], dfa_m)

# --- The New Pornographers ---
tnp = "the-new-pornographers"
tnp_n = "The New Pornographers"
tnp_m = [
    ("a-c-newman", "A.C. Newman", "Vocals/Guitar"),
    ("neko-case", "Neko Case", "Vocals"),
    ("kathryn-calder", "Kathryn Calder", "Vocals/Keyboards"),
    ("todd-fancey", "Todd Fancey", "Guitar"),
    ("john-collins", "John Collins", "Bass"),
    ("kurt-dahle", "Kurt Dahle", "Drums"),
]

artist(tnp, tnp_n, "Indie Pop", "CA", 1997, "Group",
       ["Indie Pop", "Power Pop", "Alternative Rock"], tnp_m,
       [("mass-romantic", "Mass Romantic", 2000),
        ("electric-version", "Electric Version", 2003),
        ("twin-cinema", "Twin Cinema", 2005)])

mk("mass-romantic", "Mass Romantic", tnp_n, tnp, 2000, ["Indie Pop", "Power Pop"],
   [("mass-romantic-tnp", "Mass Romantic"),
    ("the-slow-descent-tnp", "The Slow Descent into Alcoholism"),
    ("letter-from-an-occupant-tnp", "Letter from an Occupant"),
    ("the-end-of-medicine-tnp", "The End of Medicine")], tnp_m)

mk("electric-version", "Electric Version", tnp_n, tnp, 2003, ["Indie Pop", "Power Pop"],
   [("the-electric-version-tnp", "The Electric Version"),
    ("all-for-swinging-you-around-tnp", "All for Swinging You Around"),
    ("from-blown-speakers-tnp", "From Blown Speakers"),
    ("testament-youth-in-verse-tnp", "Testament to Youth in Verse")], tnp_m)

mk("twin-cinema", "Twin Cinema", tnp_n, tnp, 2005, ["Indie Pop", "Power Pop"],
   [("twin-cinema-tnp", "Twin Cinema"),
    ("use-it-tnp", "Use It"),
    ("the-bleeding-heart-show-tnp", "The Bleeding Heart Show"),
    ("broken-beads-tnp", "Broken Beads")], tnp_m)

# --- Wolf Parade ---
wp = "wolf-parade"
wp_n = "Wolf Parade"
wp_m = [
    ("dan-boeckner", "Dan Boeckner", "Vocals/Guitar"),
    ("spencer-krug", "Spencer Krug", "Vocals/Keyboards"),
    ("arlen-thompson", "Arlen Thompson", "Drums"),
    ("hadji-bakara", "Hadji Bakara", "Keyboards"),
]

artist(wp, wp_n, "Indie Rock", "CA", 2003, "Group",
       ["Indie Rock", "Art Rock", "Post-Punk"], wp_m,
       [("apologies-to-the-queen-mary", "Apologies to the Queen Mary", 2005),
        ("at-mount-zoomer", "At Mount Zoomer", 2008),
        ("cry-cry-cry-wp", "Cry Cry Cry", 2017)])

mk("apologies-to-the-queen-mary", "Apologies to the Queen Mary", wp_n, wp, 2005,
   ["Indie Rock", "Art Rock"],
   [("you-are-a-runner-wp", "You Are a Runner and I Am My Father's Son"),
    ("grounds-for-divorce-wp", "Grounds for Divorce"),
    ("ill-believe-in-anything-wp", "I'll Believe in Anything"),
    ("modern-world-wp", "Modern World")], wp_m)

mk("at-mount-zoomer", "At Mount Zoomer", wp_n, wp, 2008, ["Art Rock", "Post-Punk"],
   [("soldiers-grin-wp", "Soldier's Grin"),
    ("call-it-a-ritual-wp", "Call It a Ritual"),
    ("california-dreamer-wp", "California Dreamer"),
    ("bang-your-drum-wp", "Bang Your Drum")], wp_m)

mk("cry-cry-cry-wp", "Cry Cry Cry", wp_n, wp, 2017, ["Indie Rock", "Post-Punk"],
   [("valley-boy-wp", "Valley Boy"),
    ("lazarus-online-wp", "Lazarus Online"),
    ("a-place-where-theres-no-more-pain-wp", "A Place Where There's No More Pain"),
    ("baby-blue-wp", "Baby Blue")], wp_m)

# --- Drake ---
drk = "drake"
drk_n = "Drake"
drk_m = [("drake-person", "Drake", "Vocals/Rapper")]

artist(drk, drk_n, "Hip-Hop", "CA", 2006, "Solo",
       ["Hip-Hop", "R&B", "Pop Rap", "Trap"], drk_m,
       [("thank-me-later", "Thank Me Later", 2010),
        ("take-care-drk", "Take Care", 2011),
        ("nothing-was-the-same", "Nothing Was the Same", 2013)])

mk("thank-me-later", "Thank Me Later", drk_n, drk, 2010, ["Hip-Hop", "R&B"],
   [("fireworks-drk", "Fireworks"),
    ("find-your-love-drk", "Find Your Love"),
    ("miss-me-drk", "Miss Me"),
    ("thank-me-now-drk", "Thank Me Now")], drk_m,
   prod_slug="noah-shebib", prod_name="Noah Shebib")

mk("take-care-drk", "Take Care", drk_n, drk, 2011, ["Hip-Hop", "R&B"],
   [("headlines-drk", "Headlines"),
    ("marvins-room-drk", "Marvins Room"),
    ("take-care-drk-song", "Take Care"),
    ("the-motto-drk", "The Motto")], drk_m,
   prod_slug="noah-shebib", prod_name="Noah Shebib")

mk("nothing-was-the-same", "Nothing Was the Same", drk_n, drk, 2013, ["Hip-Hop", "R&B"],
   [("started-from-the-bottom-drk", "Started from the Bottom"),
    ("hold-on-were-going-home-drk", "Hold On, We're Going Home"),
    ("wu-tang-forever-drk", "Wu-Tang Forever"),
    ("from-time-drk", "From Time")], drk_m,
   prod_slug="noah-shebib", prod_name="Noah Shebib")

# ===========================================================================
# BATCH 3: Top Artists
# ===========================================================================

# --- Taylor Swift ---
tsw = "taylor-swift"
tsw_n = "Taylor Swift"
tsw_m = [("taylor-swift-person", "Taylor Swift", "Vocals/Guitar")]

artist(tsw, tsw_n, "Pop", "US", 2004, "Solo",
       ["Pop", "Country Pop", "Indie Folk", "Synth-Pop"], tsw_m,
       [("fearless-tsw", "Fearless", 2008),
        ("1989-tsw", "1989", 2014),
        ("folklore-tsw", "Folklore", 2020)])

mk("fearless-tsw", "Fearless", tsw_n, tsw, 2008, ["Country Pop", "Pop"],
   [("love-story-tsw", "Love Story"),
    ("you-belong-with-me-tsw", "You Belong with Me"),
    ("fearless-tsw-song", "Fearless"),
    ("white-horse-tsw", "White Horse")], tsw_m,
   prod_slug="nathan-chapman", prod_name="Nathan Chapman")

mk("1989-tsw", "1989", tsw_n, tsw, 2014, ["Pop", "Synth-Pop"],
   [("shake-it-off-tsw", "Shake It Off"),
    ("blank-space-tsw", "Blank Space"),
    ("style-tsw", "Style"),
    ("bad-blood-tsw", "Bad Blood")], tsw_m,
   prod_slug="max-martin", prod_name="Max Martin")

mk("folklore-tsw", "Folklore", tsw_n, tsw, 2020, ["Indie Folk", "Alternative"],
   [("cardigan-tsw", "Cardigan"),
    ("exile-tsw", "Exile"),
    ("august-tsw", "August"),
    ("the-1-tsw", "The 1")], tsw_m,
   prod_slug="jack-antonoff", prod_name="Jack Antonoff")

# --- Beyonce ---
bey = "beyonce"
bey_n = "Beyonce"
bey_m = [("beyonce-person", "Beyonce", "Vocals")]

artist(bey, bey_n, "R&B/Pop", "US", 1997, "Solo",
       ["R&B", "Pop", "Dance-Pop", "Hip-Hop"], bey_m,
       [("dangerously-in-love", "Dangerously in Love", 2003),
        ("lemonade-bey", "Lemonade", 2016),
        ("renaissance-bey", "Renaissance", 2022)])

mk("dangerously-in-love", "Dangerously in Love", bey_n, bey, 2003, ["R&B", "Pop"],
   [("crazy-in-love-bey", "Crazy in Love"),
    ("naughty-girl-bey", "Naughty Girl"),
    ("baby-boy-bey", "Baby Boy"),
    ("me-myself-and-i-bey", "Me, Myself and I")], bey_m,
   prod_slug="pharrell-williams", prod_name="Pharrell Williams")

mk("lemonade-bey", "Lemonade", bey_n, bey, 2016, ["R&B", "Pop", "Hip-Hop"],
   [("hold-up-bey", "Hold Up"),
    ("sorry-bey", "Sorry"),
    ("formation-bey", "Formation"),
    ("love-drought-bey", "Love Drought")], bey_m,
   prod_slug="jack-antonoff", prod_name="Jack Antonoff")

mk("renaissance-bey", "Renaissance", bey_n, bey, 2022, ["Dance-Pop", "R&B"],
   [("break-my-soul-bey", "BREAK MY SOUL"),
    ("cuff-it-bey", "CUFF IT"),
    ("alien-superstar-bey", "ALIEN SUPERSTAR"),
    ("church-girl-bey", "CHURCH GIRL")], bey_m)

# --- Kendrick Lamar ---
kl = "kendrick-lamar"
kl_n = "Kendrick Lamar"
kl_m = [("kendrick-lamar-person", "Kendrick Lamar", "Rapper/Vocals")]

artist(kl, kl_n, "Hip-Hop", "US", 2003, "Solo",
       ["Hip-Hop", "Conscious Hip-Hop", "Jazz Rap", "West Coast Hip-Hop"], kl_m,
       [("good-kid-maad-city", "good kid, m.A.A.d city", 2012),
        ("to-pimp-a-butterfly", "To Pimp a Butterfly", 2015),
        ("damn-kl", "DAMN.", 2017)])

mk("good-kid-maad-city", "good kid, m.A.A.d city", kl_n, kl, 2012,
   ["Hip-Hop", "West Coast Hip-Hop"],
   [("backseat-freestyle-kl", "Backseat Freestyle"),
    ("money-trees-kl", "Money Trees"),
    ("swimming-pools-kl", "Swimming Pools (Drank)"),
    ("poetic-justice-kl", "Poetic Justice")], kl_m)

mk("to-pimp-a-butterfly", "To Pimp a Butterfly", kl_n, kl, 2015,
   ["Jazz Rap", "Conscious Hip-Hop"],
   [("king-kunta-kl", "King Kunta"),
    ("alright-kl", "Alright"),
    ("the-blacker-the-berry-kl", "The Blacker the Berry"),
    ("mortal-man-kl", "Mortal Man")], kl_m)

mk("damn-kl", "DAMN.", kl_n, kl, 2017, ["Hip-Hop", "Conscious Hip-Hop"],
   [("humble-kl", "HUMBLE."),
    ("dna-kl", "DNA."),
    ("love-kl", "LOVE."),
    ("fear-kl", "FEAR.")], kl_m)

# --- Sabrina Carpenter ---
sc = "sabrina-carpenter"
sc_n = "Sabrina Carpenter"
sc_m = [("sabrina-carpenter-person", "Sabrina Carpenter", "Vocals")]

artist(sc, sc_n, "Pop", "US", 2014, "Solo",
       ["Pop", "Pop Rock", "Bubblegum Pop"], sc_m,
       [("emails-i-cant-send", "emails i can't send", 2022),
        ("short-n-sweet", "Short n' Sweet", 2024)])

mk("emails-i-cant-send", "emails i can't send", sc_n, sc, 2022, ["Pop", "Pop Rock"],
   [("because-i-liked-a-boy-sc", "because i liked a boy"),
    ("read-your-mind-sc", "read your mind"),
    ("bet-u-wanna-sc", "bet u wanna"),
    ("because-of-you-sc", "because of you")], sc_m,
   prod_slug="amy-allen", prod_name="Amy Allen")

mk("short-n-sweet", "Short n' Sweet", sc_n, sc, 2024, ["Pop"],
   [("espresso-sc", "Espresso"),
    ("please-please-please-sc", "Please Please Please"),
    ("taste-sc", "Taste"),
    ("good-graces-sc", "Good Graces")], sc_m,
   prod_slug="jack-antonoff", prod_name="Jack Antonoff")

# --- Olivia Rodrigo ---
ori = "olivia-rodrigo"
ori_n = "Olivia Rodrigo"
ori_m = [("olivia-rodrigo-person", "Olivia Rodrigo", "Vocals/Guitar/Piano")]

artist(ori, ori_n, "Pop", "US", 2020, "Solo",
       ["Pop", "Pop Rock", "Alternative Pop", "Bedroom Pop"], ori_m,
       [("sour-ori", "SOUR", 2021),
        ("guts-ori", "GUTS", 2023)])

mk("sour-ori", "SOUR", ori_n, ori, 2021, ["Pop", "Pop Rock"],
   [("drivers-license-ori", "drivers license"),
    ("deja-vu-ori", "deja vu"),
    ("good-4-u-ori", "good 4 u"),
    ("enough-for-you-ori", "enough for you")], ori_m,
   prod_slug="dan-nigro", prod_name="Dan Nigro")

mk("guts-ori", "GUTS", ori_n, ori, 2023, ["Pop", "Alternative Pop"],
   [("vampire-ori", "vampire"),
    ("bad-idea-right-ori", "bad idea right?"),
    ("get-him-back-ori", "get him back!"),
    ("lacy-ori", "lacy")], ori_m,
   prod_slug="dan-nigro", prod_name="Dan Nigro")

# --- Billie Eilish ---
bei = "billie-eilish"
bei_n = "Billie Eilish"
bei_m = [("billie-eilish-person", "Billie Eilish", "Vocals")]

artist(bei, bei_n, "Pop", "US", 2015, "Solo",
       ["Pop", "Dark Pop", "Electropop", "Indie Pop"], bei_m,
       [("when-we-all-fall-asleep", "When We All Fall Asleep, Where Do We Go?", 2019),
        ("happier-than-ever", "Happier Than Ever", 2021)])

mk("when-we-all-fall-asleep", "When We All Fall Asleep, Where Do We Go?",
   bei_n, bei, 2019, ["Pop", "Dark Pop", "Electropop"],
   [("bad-guy-bei", "bad guy"),
    ("xanny-bei", "xanny"),
    ("when-the-partys-over-bei", "when the party's over"),
    ("all-the-good-girls-go-to-hell-bei", "all the good girls go to hell")], bei_m,
   prod_slug="finneas-obrien", prod_name="FINNEAS")

mk("happier-than-ever", "Happier Than Ever", bei_n, bei, 2021, ["Pop", "Indie Pop"],
   [("happier-than-ever-bei", "Happier Than Ever"),
    ("oxytocin-bei", "Oxytocin"),
    ("lost-cause-bei", "Lost Cause"),
    ("my-future-bei", "my future")], bei_m,
   prod_slug="finneas-obrien", prod_name="FINNEAS")

# --- Chappell Roan ---
cr = "chappell-roan"
cr_n = "Chappell Roan"
cr_m = [("chappell-roan-person", "Chappell Roan", "Vocals")]

artist(cr, cr_n, "Pop", "US", 2017, "Solo",
       ["Pop", "Synth-Pop", "Glam Pop"], cr_m,
       [("the-rise-and-fall-of-a-midwest-princess",
         "The Rise and Fall of a Midwest Princess", 2023)])

mk("the-rise-and-fall-of-a-midwest-princess",
   "The Rise and Fall of a Midwest Princess", cr_n, cr, 2023, ["Pop", "Synth-Pop"],
   [("pink-pony-club-cr", "Pink Pony Club"),
    ("good-luck-babe-cr", "Good Luck, Babe!"),
    ("red-wine-supernova-cr", "Red Wine Supernova"),
    ("casual-cr", "Casual")], cr_m,
   prod_slug="dan-nigro", prod_name="Dan Nigro")

# --- SZA ---
sza_slug = "sza"
sza_n = "SZA"
sza_m = [("sza-person", "SZA", "Vocals")]

artist(sza_slug, sza_n, "R&B", "US", 2012, "Solo",
       ["R&B", "Alternative R&B", "Neo Soul", "Hip-Hop"], sza_m,
       [("ctrl-sza", "Ctrl", 2017),
        ("sos-sza", "SOS", 2022)])

mk("ctrl-sza", "Ctrl", sza_n, sza_slug, 2017, ["R&B", "Alternative R&B"],
   [("garden-say-it-like-dat-sza", "Garden (Say It Like Dat)"),
    ("the-weekend-sza", "The Weekend"),
    ("drew-barrymore-sza", "Drew Barrymore"),
    ("love-galore-sza", "Love Galore")], sza_m)

mk("sos-sza", "SOS", sza_n, sza_slug, 2022, ["R&B", "Alternative R&B"],
   [("shirt-sza", "Shirt"),
    ("nobody-gets-me-sza", "Nobody Gets Me"),
    ("kill-bill-sza", "Kill Bill"),
    ("seek-and-destroy-sza", "Seek & Destroy")], sza_m)

# --- Tyler the Creator ---
ttc = "tyler-the-creator"
ttc_n = "Tyler, the Creator"
ttc_m = [("tyler-the-creator-person", "Tyler, the Creator", "Rapper/Producer")]

artist(ttc, ttc_n, "Hip-Hop", "US", 2007, "Solo",
       ["Hip-Hop", "Neo Soul", "Jazz Rap", "Alternative Hip-Hop"], ttc_m,
       [("flower-boy-ttc", "Flower Boy", 2017),
        ("igor-ttc", "IGOR", 2019),
        ("call-me-if-you-get-lost-ttc", "Call Me If You Get Lost", 2021)])

mk("flower-boy-ttc", "Flower Boy", ttc_n, ttc, 2017, ["Hip-Hop", "Neo Soul"],
   [("foreword-ttc", "Foreword"),
    ("see-you-again-ttc", "See You Again"),
    ("november-ttc", "November"),
    ("911-mr-lonely-ttc", "911 / Mr. Lonely")], ttc_m,
   prod_slug="tyler-the-creator-person", prod_name="Tyler, the Creator")

mk("igor-ttc", "IGOR", ttc_n, ttc, 2019, ["Neo Soul", "Alternative Hip-Hop"],
   [("igor-s-theme-ttc", "IGOR'S THEME"),
    ("earfquake-ttc", "EARFQUAKE"),
    ("a-boy-is-a-gun-ttc", "A BOY IS A GUN*"),
    ("gone-gone-ttc", "GONE, GONE / THANK YOU")], ttc_m,
   prod_slug="tyler-the-creator-person", prod_name="Tyler, the Creator")

mk("call-me-if-you-get-lost-ttc", "Call Me If You Get Lost", ttc_n, ttc, 2021,
   ["Hip-Hop", "Alternative Hip-Hop"],
   [("corso-ttc", "CORSO"),
    ("lumberjack-ttc", "LUMBERJACK"),
    ("wusyaname-ttc", "WUSYANAME"),
    ("sweet-outside-ttc", "SWEET / I THOUGHT YOU WANTED TO DANCE")], ttc_m,
   prod_slug="tyler-the-creator-person", prod_name="Tyler, the Creator")

# --- Bad Bunny ---
bb = "bad-bunny"
bb_n = "Bad Bunny"
bb_m = [("bad-bunny-person", "Bad Bunny", "Rapper/Singer")]

artist(bb, bb_n, "Latin/Reggaeton", "US", 2013, "Solo",
       ["Reggaeton", "Latin Trap", "Pop"], bb_m,
       [("yhlqmdlg", "YHLQMDLG", 2020),
        ("el-ultimo-tour-del-mundo", "El Ultimo Tour del Mundo", 2020),
        ("un-verano-sin-ti", "Un Verano Sin Ti", 2022)])

mk("yhlqmdlg", "YHLQMDLG", bb_n, bb, 2020, ["Reggaeton", "Latin Trap"],
   [("safaera-bb", "Safaera"),
    ("yo-perreo-sola-bb", "Yo Perreo Sola"),
    ("dakiti-bb", "Dakiti"),
    ("cabeza-bb", "Cabeza")], bb_m)

mk("el-ultimo-tour-del-mundo", "El Ultimo Tour del Mundo", bb_n, bb, 2020,
   ["Latin Trap", "Pop"],
   [("te-deseo-lo-mejor-bb", "Te Deseo Lo Mejor"),
    ("antes-que-se-acabe-bb", "Antes Que Se Acabe"),
    ("la-noche-de-anoche-bb", "La Noche de Anoche"),
    ("vete-bb", "Vete")], bb_m)

mk("un-verano-sin-ti", "Un Verano Sin Ti", bb_n, bb, 2022, ["Reggaeton", "Pop", "Dembow"],
   [("moscow-mule-bb", "Moscow Mule"),
    ("titi-me-pregunto-bb", "Titi Me Pregunto"),
    ("after-party-bb", "After Party"),
    ("el-apagon-bb", "El Apagon")], bb_m)

# --- Morgan Wallen ---
mw = "morgan-wallen"
mw_n = "Morgan Wallen"
mw_m = [("morgan-wallen-person", "Morgan Wallen", "Vocals/Guitar")]

artist(mw, mw_n, "Country", "US", 2016, "Solo",
       ["Country", "Country Pop", "Bro-Country"], mw_m,
       [("if-i-know-me", "If I Know Me", 2018),
        ("dangerous-mw", "Dangerous: The Double Album", 2021),
        ("one-thing-at-a-time", "One Thing at a Time", 2023)])

mk("if-i-know-me", "If I Know Me", mw_n, mw, 2018, ["Country", "Country Pop"],
   [("up-down-mw", "Up Down"),
    ("the-way-i-talk-mw", "The Way I Talk"),
    ("whiskey-glasses-mw", "Whiskey Glasses"),
    ("if-i-know-me-mw", "If I Know Me")], mw_m)

mk("dangerous-mw", "Dangerous: The Double Album", mw_n, mw, 2021,
   ["Country", "Country Pop"],
   [("wasted-on-you-mw", "Wasted on You"),
    ("7-summers-mw", "7 Summers"),
    ("somebodys-problem-mw", "Somebody's Problem"),
    ("sand-in-my-boots-mw", "Sand in My Boots")], mw_m)

mk("one-thing-at-a-time", "One Thing at a Time", mw_n, mw, 2023, ["Country"],
   [("last-night-mw", "Last Night"),
    ("i-wrote-the-book-mw", "I Wrote the Book"),
    ("thinkin-bout-me-mw", "Thinkin' Bout Me"),
    ("i-had-some-help-mw", "I Had Some Help")], mw_m)

# --- Noah Kahan ---
nk = "noah-kahan"
nk_n = "Noah Kahan"
nk_m = [("noah-kahan-person", "Noah Kahan", "Vocals/Guitar")]

artist(nk, nk_n, "Folk Pop", "US", 2017, "Solo",
       ["Folk Pop", "Indie Folk", "Singer-Songwriter"], nk_m,
       [("busyhead-nk", "Busyhead", 2019),
        ("stick-season-nk", "Stick Season", 2022)])

mk("busyhead-nk", "Busyhead", nk_n, nk, 2019, ["Folk Pop", "Indie Folk"],
   [("young-blood-nk", "Young Blood"),
    ("mess-nk", "Mess"),
    ("come-over-nk", "Come Over"),
    ("cynic-nk", "Cynic")], nk_m)

mk("stick-season-nk", "Stick Season", nk_n, nk, 2022, ["Folk Pop", "Indie Folk"],
   [("stick-season-nk-song", "Stick Season"),
    ("all-my-love-nk", "All My Love"),
    ("dial-drunk-nk", "Dial Drunk"),
    ("northern-attitude-nk", "Northern Attitude")], nk_m)

# --- Zach Bryan ---
zb = "zach-bryan"
zb_n = "Zach Bryan"
zb_m = [("zach-bryan-person", "Zach Bryan", "Vocals/Guitar")]

artist(zb, zb_n, "Country", "US", 2019, "Solo",
       ["Country", "Americana", "Folk"], zb_m,
       [("american-heartbreak", "American Heartbreak", 2022),
        ("zach-bryan-st", "Zach Bryan", 2023)])

mk("american-heartbreak", "American Heartbreak", zb_n, zb, 2022,
   ["Country", "Americana"],
   [("crooked-teeth-zb", "Crooked Teeth"),
    ("from-austin-zb", "From Austin"),
    ("something-in-the-orange-zb", "Something in the Orange"),
    ("late-july-zb", "Late July")], zb_m,
   prod_slug="zach-bryan-person", prod_name="Zach Bryan")

mk("zach-bryan-st", "Zach Bryan", zb_n, zb, 2023, ["Country", "Folk"],
   [("i-remember-everything-zb", "I Remember Everything"),
    ("oklahoma-smokeshow-zb", "Oklahoma Smokeshow"),
    ("overtime-zb", "Overtime"),
    ("fearless-zb", "Fearless")], zb_m,
   prod_slug="zach-bryan-person", prod_name="Zach Bryan")

# --- Gracie Abrams ---
ga = "gracie-abrams"
ga_n = "Gracie Abrams"
ga_m = [("gracie-abrams-person", "Gracie Abrams", "Vocals/Guitar")]

artist(ga, ga_n, "Indie Pop", "US", 2019, "Solo",
       ["Indie Pop", "Bedroom Pop", "Folk Pop"], ga_m,
       [("good-riddance-ga", "Good Riddance", 2023),
        ("the-secret-of-us-ga", "The Secret of Us", 2024)])

mk("good-riddance-ga", "Good Riddance", ga_n, ga, 2023, ["Indie Pop", "Bedroom Pop"],
   [("21-ga", "21"),
    ("amelie-ga", "Amelie"),
    ("difficult-ga", "Difficult"),
    ("will-u-still-ga", "Will you still?")], ga_m,
   prod_slug="aaron-dessner", prod_name="Aaron Dessner")

mk("the-secret-of-us-ga", "The Secret of Us", ga_n, ga, 2024, ["Indie Pop", "Folk Pop"],
   [("close-to-you-ga", "Close to You"),
    ("lets-be-honest-ga", "Let's Be Honest"),
    ("risk-ga", "Risk"),
    ("the-secret-of-us-ga-song", "The Secret of Us")], ga_m,
   prod_slug="jack-antonoff", prod_name="Jack Antonoff")

# --- Benson Boone ---
bbo = "benson-boone"
bbo_n = "Benson Boone"
bbo_m = [("benson-boone-person", "Benson Boone", "Vocals/Piano")]

artist(bbo, bbo_n, "Pop", "US", 2021, "Solo",
       ["Pop", "Pop Rock", "Indie Pop"], bbo_m,
       [("fireworks-and-rollerblades", "Fireworks & Rollerblades", 2024)])

mk("fireworks-and-rollerblades", "Fireworks & Rollerblades", bbo_n, bbo, 2024,
   ["Pop", "Pop Rock"],
   [("beautiful-things-bbo", "Beautiful Things"),
    ("in-the-stars-bbo", "In the Stars"),
    ("ghost-town-bbo", "Ghost Town"),
    ("before-you-go-bbo", "Before You Go")], bbo_m)

# --- Post Malone ---
pm = "post-malone"
pm_n = "Post Malone"
pm_m = [("post-malone-person", "Post Malone", "Vocals/Rapper")]

artist(pm, pm_n, "Hip-Hop", "US", 2013, "Solo",
       ["Hip-Hop", "Pop Rap", "Trap", "R&B"], pm_m,
       [("beerbongs-and-bentleys", "beerbongs & bentleys", 2018),
        ("hollywoods-bleeding", "Hollywood's Bleeding", 2019),
        ("twelve-carat-toothache", "Twelve Carat Toothache", 2022)])

mk("beerbongs-and-bentleys", "beerbongs & bentleys", pm_n, pm, 2018,
   ["Hip-Hop", "Pop Rap"],
   [("rockstar-pm", "Rockstar"),
    ("psycho-pm", "Psycho"),
    ("better-now-pm", "Better Now"),
    ("paranoid-pm", "Paranoid")], pm_m)

mk("hollywoods-bleeding", "Hollywood's Bleeding", pm_n, pm, 2019, ["Hip-Hop", "Pop Rap"],
   [("circles-pm", "Circles"),
    ("sunflower-pm", "Sunflower"),
    ("wow-pm", "Wow."),
    ("take-what-you-want-pm", "Take What You Want")], pm_m)

mk("twelve-carat-toothache", "Twelve Carat Toothache", pm_n, pm, 2022, ["Pop Rap", "R&B"],
   [("motley-crew-pm", "Motley Crew"),
    ("one-right-now-pm", "One Right Now"),
    ("i-cannot-be-pm", "I Cannot Be (a Broken Heart)"),
    ("wrapped-around-your-finger-pm", "Wrapped Around Your Finger")], pm_m)

# --- Ariana Grande ---
agr = "ariana-grande"
agr_n = "Ariana Grande"
agr_m = [("ariana-grande-person", "Ariana Grande", "Vocals")]

artist(agr, agr_n, "Pop", "US", 2011, "Solo",
       ["Pop", "R&B", "Dance-Pop", "Trap Pop"], agr_m,
       [("thank-u-next", "thank u, next", 2019),
        ("positions-agr", "Positions", 2020),
        ("eternal-sunshine-agr", "eternal sunshine", 2024)])

mk("thank-u-next", "thank u, next", agr_n, agr, 2019, ["Pop", "Trap Pop"],
   [("7-rings-agr", "7 rings"),
    ("thank-u-next-agr", "thank u, next"),
    ("break-up-with-your-girlfriend-agr", "break up with your girlfriend, i'm bored"),
    ("imagine-agr", "imagine")], agr_m,
   prod_slug="max-martin", prod_name="Max Martin")

mk("positions-agr", "Positions", agr_n, agr, 2020, ["Pop", "R&B"],
   [("positions-agr-song", "positions"),
    ("34-35-agr", "34+35"),
    ("motive-agr", "motive"),
    ("just-like-magic-agr", "just like magic")], agr_m,
   prod_slug="max-martin", prod_name="Max Martin")

mk("eternal-sunshine-agr", "eternal sunshine", agr_n, agr, 2024, ["Pop", "Dance-Pop"],
   [("yes-and-agr", "yes, and?"),
    ("we-cant-be-friends-agr", "we can't be friends (wait for your love)"),
    ("the-boy-is-mine-agr", "the boy is mine"),
    ("imperfect-for-you-agr", "imperfect for you")], agr_m,
   prod_slug="max-martin", prod_name="Max Martin")

# --- Harry Styles ---
hs = "harry-styles"
hs_n = "Harry Styles"
hs_m = [("harry-styles-person", "Harry Styles", "Vocals/Guitar")]

artist(hs, hs_n, "Pop", "UK", 2010, "Solo",
       ["Pop", "Pop Rock", "Soft Rock", "Folk Pop"], hs_m,
       [("harry-styles-st", "Harry Styles", 2017),
        ("fine-line-hs", "Fine Line", 2019),
        ("harrys-house", "Harry's House", 2022)])

mk("harry-styles-st", "Harry Styles", hs_n, hs, 2017, ["Pop", "Soft Rock"],
   [("sign-of-the-times-hs", "Sign of the Times"),
    ("sweet-creature-hs", "Sweet Creature"),
    ("two-ghosts-hs", "Two Ghosts"),
    ("from-the-dining-table-hs", "From the Dining Table")], hs_m)

mk("fine-line-hs", "Fine Line", hs_n, hs, 2019, ["Pop", "Pop Rock"],
   [("lights-up-hs", "Lights Up"),
    ("watermelon-sugar-hs", "Watermelon Sugar"),
    ("adore-you-hs", "Adore You"),
    ("cherry-hs", "Cherry")], hs_m)

mk("harrys-house", "Harry's House", hs_n, hs, 2022, ["Pop", "Indie Pop"],
   [("as-it-was-hs", "As It Was"),
    ("late-night-talking-hs", "Late Night Talking"),
    ("music-for-a-sushi-restaurant-hs", "Music for a Sushi Restaurant"),
    ("satellite-hs", "Satellite")], hs_m)

# --- Lady Gaga ---
lgag = "lady-gaga"
lgag_n = "Lady Gaga"
lgag_m = [("lady-gaga-person", "Lady Gaga", "Vocals/Piano")]

artist(lgag, lgag_n, "Pop", "US", 2006, "Solo",
       ["Pop", "Dance-Pop", "Electropop", "Art Pop"], lgag_m,
       [("the-fame-lgag", "The Fame", 2008),
        ("born-this-way-lgag", "Born This Way", 2011),
        ("chromatica-lgag", "Chromatica", 2020)])

mk("the-fame-lgag", "The Fame", lgag_n, lgag, 2008, ["Pop", "Dance-Pop", "Electropop"],
   [("just-dance-lgag", "Just Dance"),
    ("poker-face-lgag", "Poker Face"),
    ("paparazzi-lgag", "Paparazzi"),
    ("lovegame-lgag", "LoveGame")], lgag_m,
   prod_slug="max-martin", prod_name="Max Martin")

mk("born-this-way-lgag", "Born This Way", lgag_n, lgag, 2011, ["Pop", "Dance-Pop"],
   [("born-this-way-lgag-song", "Born This Way"),
    ("the-edge-of-glory-lgag", "The Edge of Glory"),
    ("you-and-i-lgag", "You & I"),
    ("bad-kids-lgag", "Bad Kids")], lgag_m)

mk("chromatica-lgag", "Chromatica", lgag_n, lgag, 2020, ["Dance-Pop", "Electropop"],
   [("stupid-love-lgag", "Stupid Love"),
    ("rain-on-me-lgag", "Rain on Me"),
    ("free-woman-lgag", "Free Woman"),
    ("sour-candy-lgag", "Sour Candy")], lgag_m)

# --- Doja Cat ---
doj = "doja-cat"
doj_n = "Doja Cat"
doj_m = [("doja-cat-person", "Doja Cat", "Vocals/Rapper")]

artist(doj, doj_n, "Pop/R&B", "US", 2012, "Solo",
       ["Pop", "R&B", "Hip-Hop", "Dance-Pop"], doj_m,
       [("hot-pink-doj", "Hot Pink", 2019),
        ("planet-her-doj", "Planet Her", 2021),
        ("scarlet-doj", "Scarlet", 2023)])

mk("hot-pink-doj", "Hot Pink", doj_n, doj, 2019, ["Pop", "R&B", "Hip-Hop"],
   [("say-so-doj", "Say So"),
    ("juicy-doj", "Juicy"),
    ("streets-doj", "Streets"),
    ("bottom-bitch-doj", "Bottom Bitch")], doj_m)

mk("planet-her-doj", "Planet Her", doj_n, doj, 2021, ["Pop", "R&B", "Dance-Pop"],
   [("kiss-me-more-doj", "Kiss Me More"),
    ("need-to-know-doj", "Need to Know"),
    ("woman-doj", "Woman"),
    ("you-right-doj", "You Right")], doj_m)

mk("scarlet-doj", "Scarlet", doj_n, doj, 2023, ["Hip-Hop", "Rap"],
   [("paint-the-town-red-doj", "Paint the Town Red"),
    ("scarlet-doj-song", "Scarlet"),
    ("demons-doj", "Demons"),
    ("agora-hills-doj", "Agora Hills")], doj_m)

# --- Lana Del Rey ---
ldr = "lana-del-rey"
ldr_n = "Lana Del Rey"
ldr_m = [("lana-del-rey-person", "Lana Del Rey", "Vocals")]

artist(ldr, ldr_n, "Indie Pop", "US", 2005, "Solo",
       ["Indie Pop", "Baroque Pop", "Sadcore", "Dream Pop"], ldr_m,
       [("born-to-die-ldr", "Born to Die", 2012),
        ("ultraviolence-ldr", "Ultraviolence", 2014),
        ("norman-fucking-rockwell", "Norman Fucking Rockwell!", 2019)])

mk("born-to-die-ldr", "Born to Die", ldr_n, ldr, 2012, ["Indie Pop", "Dream Pop"],
   [("born-to-die-ldr-song", "Born to Die"),
    ("video-games-ldr", "Video Games"),
    ("summertime-sadness-ldr", "Summertime Sadness"),
    ("national-anthem-ldr", "National Anthem")], ldr_m)

mk("ultraviolence-ldr", "Ultraviolence", ldr_n, ldr, 2014, ["Indie Rock", "Dream Pop"],
   [("cruel-world-ldr", "Cruel World"),
    ("ultraviolence-ldr-song", "Ultraviolence"),
    ("shades-of-cool-ldr", "Shades of Cool"),
    ("west-coast-ldr", "West Coast")], ldr_m)

mk("norman-fucking-rockwell", "Norman Fucking Rockwell!", ldr_n, ldr, 2019,
   ["Indie Pop", "Art Pop"],
   [("mariners-apartment-complex-ldr", "Mariners Apartment Complex"),
    ("venice-bitch-ldr", "Venice Bitch"),
    ("hope-is-a-dangerous-thing-ldr",
     "Hope Is a Dangerous Thing for a Woman Like Me to Have"),
    ("the-greatest-ldr", "The Greatest")], ldr_m,
   prod_slug="jack-antonoff", prod_name="Jack Antonoff")

# --- Bruno Mars ---
bm = "bruno-mars"
bm_n = "Bruno Mars"
bm_m = [("bruno-mars-person", "Bruno Mars", "Vocals")]

artist(bm, bm_n, "Pop/R&B", "US", 2004, "Solo",
       ["Pop", "R&B", "Funk", "Soul"], bm_m,
       [("doo-wops-and-hooligans", "Doo-Wops & Hooligans", 2010),
        ("unorthodox-jukebox", "Unorthodox Jukebox", 2012),
        ("24k-magic", "24K Magic", 2016)])

mk("doo-wops-and-hooligans", "Doo-Wops & Hooligans", bm_n, bm, 2010, ["Pop", "R&B"],
   [("just-the-way-you-are-bm", "Just the Way You Are"),
    ("grenade-bm", "Grenade"),
    ("the-lazy-song-bm", "The Lazy Song"),
    ("marry-you-bm", "Marry You")], bm_m)

mk("unorthodox-jukebox", "Unorthodox Jukebox", bm_n, bm, 2012, ["Pop", "R&B", "Funk"],
   [("locked-out-of-heaven-bm", "Locked Out of Heaven"),
    ("when-i-was-your-man-bm", "When I Was Your Man"),
    ("gorilla-bm", "Gorilla"),
    ("treasure-bm", "Treasure")], bm_m)

mk("24k-magic", "24K Magic", bm_n, bm, 2016, ["Funk", "R&B", "Pop"],
   [("24k-magic-song", "24K Magic"),
    ("thats-what-i-like-bm", "That's What I Like"),
    ("versace-on-the-floor-bm", "Versace on the Floor"),
    ("finesse-bm", "Finesse")], bm_m)

# --- Mitski ---
mts = "mitski"
mts_n = "Mitski"
mts_m = [("mitski-person", "Mitski", "Vocals/Guitar")]

artist(mts, mts_n, "Indie Rock", "US", 2011, "Solo",
       ["Indie Rock", "Art Rock", "Indie Pop", "Bedroom Pop"], mts_m,
       [("puberty-2", "Puberty 2", 2016),
        ("be-the-cowboy", "Be the Cowboy", 2018),
        ("laurel-hell", "Laurel Hell", 2022)])

mk("puberty-2", "Puberty 2", mts_n, mts, 2016, ["Indie Rock", "Art Rock"],
   [("your-best-american-girl-mts", "Your Best American Girl"),
    ("once-more-to-see-you-mts", "Once More to See You"),
    ("a-burning-hill-mts", "A Burning Hill"),
    ("fireworks-mts", "Fireworks")], mts_m)

mk("be-the-cowboy", "Be the Cowboy", mts_n, mts, 2018, ["Indie Pop", "Art Rock"],
   [("nobody-mts", "Nobody"),
    ("geyser-mts", "Geyser"),
    ("me-and-my-husband-mts", "Me and My Husband"),
    ("come-into-the-water-mts", "Come Into the Water")], mts_m)

mk("laurel-hell", "Laurel Hell", mts_n, mts, 2022, ["Synth-Pop", "Indie Pop"],
   [("working-for-the-knife-mts", "Working for the Knife"),
    ("the-only-heartbreaker-mts", "The Only Heartbreaker"),
    ("i-guess-mts", "I Guess"),
    ("heat-lightning-mts", "Heat Lightning")], mts_m)

# ===========================================================================
# PEOPLE
# ===========================================================================

# --- RRFB members ---
per("robert-randolph", "Robert Randolph", 1978, "American",
    ["Musician", "Pedal Steel Guitarist", "Vocalist"],
    bands=[(rrfb, rrfb_n, "Pedal Steel Guitar/Vocals")])

per("danyel-morgan", "Danyel Morgan", 1980, "American",
    ["Musician", "Bassist"],
    bands=[(rrfb, rrfb_n, "Bass")])

per("marcus-randolph", "Marcus Randolph", 1982, "American",
    ["Musician", "Drummer"],
    bands=[(rrfb, rrfb_n, "Drums")])

per("lenesha-randolph", "Lenesha Randolph", 1984, "American",
    ["Musician", "Vocalist"],
    bands=[(rrfb, rrfb_n, "Vocals")])

# --- Billy Talent ---
per("benjamin-kowalewicz", "Benjamin Kowalewicz", 1977, "Canadian",
    ["Vocalist"],
    bands=[(bt, bt_n, "Vocals")])

per("ian-d-sa", "Ian D'Sa", 1977, "Canadian",
    ["Guitarist", "Vocalist"],
    bands=[(bt, bt_n, "Guitar/Vocals")])

per("jonathan-gallant", "Jonathan Gallant", 1977, "Canadian",
    ["Bassist"],
    bands=[(bt, bt_n, "Bass")])

per("aaron-solowoniuk", "Aaron Solowoniuk", 1977, "Canadian",
    ["Drummer"],
    bands=[(bt, bt_n, "Drums")])

# --- Nickelback ---
per("chad-kroeger", "Chad Kroeger", 1974, "Canadian",
    ["Vocalist", "Guitarist"],
    bands=[(nb, nb_n, "Vocals/Guitar")])

per("ryan-peake", "Ryan Peake", 1973, "Canadian",
    ["Guitarist"],
    bands=[(nb, nb_n, "Guitar/Vocals")])

per("mike-kroeger", "Mike Kroeger", 1972, "Canadian",
    ["Bassist"],
    bands=[(nb, nb_n, "Bass")])

per("daniel-adair", "Daniel Adair", 1975, "Canadian",
    ["Drummer"],
    bands=[(nb, nb_n, "Drums")])

# --- The Tragically Hip ---
per("gordon-downie", "Gordon Downie", 1964, "Canadian",
    ["Vocalist", "Lyricist"],
    bands=[(th, th_n, "Vocals")],
    died=2017)

per("rob-baker", "Rob Baker", 1964, "Canadian",
    ["Guitarist"],
    bands=[(th, th_n, "Guitar")])

per("paul-langlois", "Paul Langlois", 1964, "Canadian",
    ["Guitarist"],
    bands=[(th, th_n, "Guitar")])

per("gord-sinclair", "Gord Sinclair", 1963, "Canadian",
    ["Bassist"],
    bands=[(th, th_n, "Bass")])

per("johnny-fay", "Johnny Fay", 1966, "Canadian",
    ["Drummer"],
    bands=[(th, th_n, "Drums")])

# --- Rush ---
per("geddy-lee", "Geddy Lee", 1953, "Canadian",
    ["Vocalist", "Bassist", "Keyboardist"],
    bands=[(rsh, rsh_n, "Vocals/Bass/Keyboards")])

per("alex-lifeson", "Alex Lifeson", 1953, "Canadian",
    ["Guitarist"],
    bands=[(rsh, rsh_n, "Guitar")])

per("neil-peart", "Neil Peart", 1952, "Canadian",
    ["Drummer", "Lyricist"],
    bands=[(rsh, rsh_n, "Drums/Percussion")],
    died=2020)

per("john-rutsey", "John Rutsey", 1952, "Canadian",
    ["Drummer"],
    bands=[(rsh, rsh_n, "Drums")],
    died=2008)

# --- Arcade Fire ---
per("win-butler", "Win Butler", 1980, "Canadian",
    ["Vocalist", "Guitarist", "Multi-Instrumentalist"],
    bands=[(af, af_n, "Vocals/Guitar")])

per("regine-chassagne", "Regine Chassagne", 1979, "Canadian",
    ["Vocalist", "Multi-Instrumentalist"],
    bands=[(af, af_n, "Vocals/Keyboards")])

per("richard-reed-parry", "Richard Reed Parry", 1978, "Canadian",
    ["Multi-Instrumentalist"],
    bands=[(af, af_n, "Multi-Instrumentalist")])

per("tim-kingsbury", "Tim Kingsbury", 1978, "Canadian",
    ["Bassist", "Guitarist"],
    bands=[(af, af_n, "Bass/Guitar")])

per("jeremy-gara", "Jeremy Gara", 1978, "Canadian",
    ["Drummer"],
    bands=[(af, af_n, "Drums")])

per("william-butler", "William Butler", 1983, "Canadian",
    ["Multi-Instrumentalist"],
    bands=[(af, af_n, "Multi-Instrumentalist")])

# --- The Weeknd ---
per("abel-tesfaye", "Abel Tesfaye", 1990, "Canadian",
    ["Singer", "Songwriter", "Producer"],
    bands=[(tw, tw_n, "Vocals")])

# --- Neil Young ---
per("neil-young-person", "Neil Young", 1945, "Canadian",
    ["Singer", "Songwriter", "Guitarist"],
    bands=[(ny, ny_n, "Vocals/Guitar")])

# --- Joni Mitchell ---
per("joni-mitchell-person", "Joni Mitchell", 1943, "Canadian",
    ["Singer", "Songwriter", "Guitarist", "Painter"],
    bands=[(jm, jm_n, "Vocals/Guitar/Piano")])

# --- Broken Social Scene / Metric ---
per("emily-haines", "Emily Haines", 1974, "Canadian",
    ["Vocalist", "Keyboardist", "Songwriter"],
    bands=[(bss, bss_n, "Vocals/Keyboards"),
           (met, met_n, "Vocals/Keyboards")])

per("leslie-feist", "Leslie Feist", 1976, "Canadian",
    ["Singer", "Songwriter", "Guitarist"],
    bands=[(bss, bss_n, "Vocals/Guitar"),
           (fst, fst_n, "Vocals/Guitar")])

per("kevin-drew", "Kevin Drew", 1974, "Canadian",
    ["Musician", "Producer"],
    bands=[(bss, bss_n, "Vocals/Guitar")])

per("brendan-canning", "Brendan Canning", 1973, "Canadian",
    ["Musician"],
    bands=[(bss, bss_n, "Vocals/Bass")])

per("jason-collett", "Jason Collett", 1970, "Canadian",
    ["Singer", "Songwriter"],
    bands=[(bss, bss_n, "Vocals/Guitar")])

per("andrew-whiteman", "Andrew Whiteman", 1975, "Canadian",
    ["Guitarist"],
    bands=[(bss, bss_n, "Guitar")])

per("charles-spearin", "Charles Spearin", 1970, "Canadian",
    ["Bassist", "Trumpeter"],
    bands=[(bss, bss_n, "Bass/Trumpet")])

# --- Metric ---
per("james-shaw", "James Shaw", 1976, "Canadian",
    ["Guitarist"],
    bands=[(met, met_n, "Guitar")])

per("joshua-winstead", "Joshua Winstead", 1976, "Canadian",
    ["Bassist"],
    bands=[(met, met_n, "Bass")])

per("joules-scott-key", "Joules Scott-Key", 1974, "Canadian",
    ["Drummer"],
    bands=[(met, met_n, "Drums")])

# --- Barenaked Ladies ---
per("steven-page", "Steven Page", 1970, "Canadian",
    ["Vocalist", "Guitarist", "Songwriter"],
    bands=[(bnl, bnl_n, "Vocals/Guitar")])

per("ed-robertson", "Ed Robertson", 1970, "Canadian",
    ["Vocalist", "Guitarist"],
    bands=[(bnl, bnl_n, "Vocals/Guitar")])

per("jim-creeggan", "Jim Creeggan", 1971, "Canadian",
    ["Bassist"],
    bands=[(bnl, bnl_n, "Bass")])

per("kevin-hearn", "Kevin Hearn", 1969, "Canadian",
    ["Keyboardist"],
    bands=[(bnl, bnl_n, "Keyboards")])

per("tyler-stewart", "Tyler Stewart", 1967, "Canadian",
    ["Drummer"],
    bands=[(bnl, bnl_n, "Drums")])

# --- Alanis Morissette ---
per("alanis-morissette-person", "Alanis Morissette", 1974, "Canadian",
    ["Singer", "Songwriter", "Musician"],
    bands=[(ala, ala_n, "Vocals/Guitar/Harmonica")])

# --- Avril Lavigne ---
per("avril-lavigne-person", "Avril Lavigne", 1984, "Canadian",
    ["Singer", "Songwriter", "Musician"],
    bands=[(avr, avr_n, "Vocals/Guitar")])

# --- Sum 41 ---
per("deryck-whibley", "Deryck Whibley", 1980, "Canadian",
    ["Vocalist", "Guitarist", "Producer"],
    bands=[(s41, s41_n, "Vocals/Guitar")])

per("dave-baksh", "Dave Baksh", 1980, "Canadian",
    ["Guitarist"],
    bands=[(s41, s41_n, "Guitar/Vocals")])

per("jason-mccaslin", "Jason McCaslin", 1981, "Canadian",
    ["Bassist"],
    bands=[(s41, s41_n, "Bass")])

per("tom-thacker", "Tom Thacker", 1982, "Canadian",
    ["Guitarist"],
    bands=[(s41, s41_n, "Guitar")])

per("frank-zummo", "Frank Zummo", 1984, "American",
    ["Drummer"],
    bands=[(s41, s41_n, "Drums")])

# --- Our Lady Peace ---
per("raine-maida", "Raine Maida", 1970, "Canadian",
    ["Vocalist", "Songwriter"],
    bands=[(olp, olp_n, "Vocals")])

per("mike-turner", "Mike Turner", 1970, "Canadian",
    ["Guitarist"],
    bands=[(olp, olp_n, "Guitar")])

per("jeremy-taggart", "Jeremy Taggart", 1976, "Canadian",
    ["Drummer"],
    bands=[(olp, olp_n, "Drums")])

per("duncan-coutts", "Duncan Coutts", 1970, "Canadian",
    ["Bassist"],
    bands=[(olp, olp_n, "Bass")])

# --- Tegan and Sara ---
per("tegan-quin", "Tegan Quin", 1980, "Canadian",
    ["Vocalist", "Guitarist", "Songwriter"],
    bands=[(tns, tns_n, "Vocals/Guitar")])

per("sara-quin", "Sara Quin", 1980, "Canadian",
    ["Vocalist", "Guitarist", "Songwriter"],
    bands=[(tns, tns_n, "Vocals/Guitar")])

# --- Sarah McLachlan ---
per("sarah-mclachlan-person", "Sarah McLachlan", 1968, "Canadian",
    ["Singer", "Songwriter", "Pianist"],
    bands=[(smc, smc_n, "Vocals/Piano/Guitar")])

# --- Leonard Cohen ---
per("leonard-cohen-person", "Leonard Cohen", 1934, "Canadian",
    ["Singer", "Songwriter", "Poet", "Novelist"],
    bands=[(lco, lco_n, "Vocals/Guitar")],
    died=2016)

# --- Death from Above 1979 ---
per("sebastien-grainger", "Sebastien Grainger", 1979, "Canadian",
    ["Vocalist", "Drummer"],
    bands=[(dfa, dfa_n, "Vocals/Drums")])

per("jesse-f-keeler", "Jesse F. Keeler", 1977, "Canadian",
    ["Bassist", "Keyboardist"],
    bands=[(dfa, dfa_n, "Bass/Keyboards")])

# --- The New Pornographers ---
per("a-c-newman", "A.C. Newman", 1969, "Canadian",
    ["Vocalist", "Guitarist", "Songwriter"],
    bands=[(tnp, tnp_n, "Vocals/Guitar")])

per("neko-case", "Neko Case", 1970, "American",
    ["Vocalist", "Guitarist", "Songwriter"],
    bands=[(tnp, tnp_n, "Vocals")])

per("kathryn-calder", "Kathryn Calder", 1982, "Canadian",
    ["Vocalist", "Keyboardist"],
    bands=[(tnp, tnp_n, "Vocals/Keyboards")])

per("todd-fancey", "Todd Fancey", 1968, "Canadian",
    ["Guitarist"],
    bands=[(tnp, tnp_n, "Guitar")])

per("john-collins", "John Collins", 1976, "Canadian",
    ["Bassist", "Producer"],
    bands=[(tnp, tnp_n, "Bass")])

per("kurt-dahle", "Kurt Dahle", 1974, "Canadian",
    ["Drummer"],
    bands=[(tnp, tnp_n, "Drums")])

# --- Wolf Parade ---
per("dan-boeckner", "Dan Boeckner", 1979, "Canadian",
    ["Vocalist", "Guitarist"],
    bands=[(wp, wp_n, "Vocals/Guitar")])

per("spencer-krug", "Spencer Krug", 1979, "Canadian",
    ["Vocalist", "Keyboardist"],
    bands=[(wp, wp_n, "Vocals/Keyboards")])

per("arlen-thompson", "Arlen Thompson", 1980, "Canadian",
    ["Drummer"],
    bands=[(wp, wp_n, "Drums")])

per("hadji-bakara", "Hadji Bakara", 1980, "Canadian",
    ["Keyboardist"],
    bands=[(wp, wp_n, "Keyboards")])

# --- Drake ---
per("drake-person", "Drake", 1986, "Canadian",
    ["Rapper", "Singer", "Songwriter", "Actor"],
    bands=[(drk, drk_n, "Vocals/Rapper")])

# --- Producers ---
per("noah-shebib", "Noah Shebib", 1987, "Canadian",
    ["Record Producer", "Musician"])

per("rick-rubin", "Rick Rubin", 1963, "American",
    ["Record Producer"])

per("max-martin", "Max Martin", 1971, "Swedish",
    ["Record Producer", "Songwriter"])

per("jack-antonoff", "Jack Antonoff", 1984, "American",
    ["Record Producer", "Musician"])

per("finneas-obrien", "FINNEAS", 1997, "American",
    ["Record Producer", "Musician", "Songwriter"])

per("pharrell-williams", "Pharrell Williams", 1973, "American",
    ["Record Producer", "Musician", "Vocalist"])

per("dan-nigro", "Dan Nigro", 1987, "American",
    ["Record Producer", "Musician"])

per("nathan-chapman", "Nathan Chapman", 1983, "American",
    ["Record Producer", "Musician"])

per("aaron-dessner", "Aaron Dessner", 1979, "American",
    ["Record Producer", "Musician", "Guitarist"])

per("amy-allen", "Amy Allen", 1991, "American",
    ["Songwriter", "Singer"])

# --- Top Artist persons ---
per("taylor-swift-person", "Taylor Swift", 1989, "American",
    ["Singer", "Songwriter"],
    bands=[(tsw, tsw_n, "Vocals/Guitar")])

per("beyonce-person", "Beyonce", 1981, "American",
    ["Singer", "Songwriter", "Actress"],
    bands=[(bey, bey_n, "Vocals")])

per("kendrick-lamar-person", "Kendrick Lamar", 1987, "American",
    ["Rapper", "Songwriter"],
    bands=[(kl, kl_n, "Rapper/Vocals")])

per("sabrina-carpenter-person", "Sabrina Carpenter", 2000, "American",
    ["Singer", "Songwriter", "Actress"],
    bands=[(sc, sc_n, "Vocals")])

per("olivia-rodrigo-person", "Olivia Rodrigo", 2003, "American",
    ["Singer", "Songwriter", "Actress"],
    bands=[(ori, ori_n, "Vocals/Guitar/Piano")])

per("billie-eilish-person", "Billie Eilish", 2001, "American",
    ["Singer", "Songwriter"],
    bands=[(bei, bei_n, "Vocals")])

per("chappell-roan-person", "Chappell Roan", 1998, "American",
    ["Singer", "Songwriter"],
    bands=[(cr, cr_n, "Vocals")])

per("sza-person", "SZA", 1989, "American",
    ["Singer", "Songwriter"],
    bands=[(sza_slug, sza_n, "Vocals")])

per("tyler-the-creator-person", "Tyler, the Creator", 1991, "American",
    ["Rapper", "Record Producer", "Singer", "Director"],
    bands=[(ttc, ttc_n, "Rapper/Producer")])

per("bad-bunny-person", "Bad Bunny", 1994, "American",
    ["Rapper", "Singer", "Actor"],
    bands=[(bb, bb_n, "Rapper/Singer")])

per("morgan-wallen-person", "Morgan Wallen", 1993, "American",
    ["Singer", "Songwriter"],
    bands=[(mw, mw_n, "Vocals/Guitar")])

per("noah-kahan-person", "Noah Kahan", 1997, "American",
    ["Singer", "Songwriter"],
    bands=[(nk, nk_n, "Vocals/Guitar")])

per("zach-bryan-person", "Zach Bryan", 1996, "American",
    ["Singer", "Songwriter", "Producer"],
    bands=[(zb, zb_n, "Vocals/Guitar")])

per("gracie-abrams-person", "Gracie Abrams", 1999, "American",
    ["Singer", "Songwriter"],
    bands=[(ga, ga_n, "Vocals/Guitar")])

per("benson-boone-person", "Benson Boone", 2002, "American",
    ["Singer", "Songwriter"],
    bands=[(bbo, bbo_n, "Vocals/Piano")])

per("post-malone-person", "Post Malone", 1995, "American",
    ["Rapper", "Singer", "Songwriter"],
    bands=[(pm, pm_n, "Vocals/Rapper")])

per("ariana-grande-person", "Ariana Grande", 1993, "American",
    ["Singer", "Songwriter", "Actress"],
    bands=[(agr, agr_n, "Vocals")])

per("harry-styles-person", "Harry Styles", 1994, "British",
    ["Singer", "Songwriter", "Actor"],
    bands=[(hs, hs_n, "Vocals/Guitar")])

per("lady-gaga-person", "Lady Gaga", 1986, "American",
    ["Singer", "Songwriter", "Actress", "Pianist"],
    bands=[(lgag, lgag_n, "Vocals/Piano")])

per("doja-cat-person", "Doja Cat", 1995, "American",
    ["Singer", "Rapper", "Songwriter"],
    bands=[(doj, doj_n, "Vocals/Rapper")])

per("lana-del-rey-person", "Lana Del Rey", 1985, "American",
    ["Singer", "Songwriter"],
    bands=[(ldr, ldr_n, "Vocals")])

per("bruno-mars-person", "Bruno Mars", 1985, "American",
    ["Singer", "Songwriter", "Dancer", "Producer"],
    bands=[(bm, bm_n, "Vocals")])

per("mitski-person", "Mitski", 1990, "American",
    ["Singer", "Songwriter"],
    bands=[(mts, mts_n, "Vocals/Guitar")])

print(f"Created: A={nc['A']} AL={nc['AL']} S={nc['S']} P={nc['P']} | Skipped={sk}")
