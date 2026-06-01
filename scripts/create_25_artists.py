#!/usr/bin/env python3
"""Create 26 rock artists with albums, songs, and people for MusicTree."""
from pathlib import Path
import os

BASE = Path(__file__).parent.parent
ARTISTS_DIR = BASE / "content" / "artists"
ALBUMS_DIR = BASE / "content" / "albums"
SONGS_DIR = BASE / "content" / "songs"
PEOPLE_DIR = BASE / "content" / "people"

for d in [ARTISTS_DIR, ALBUMS_DIR, SONGS_DIR, PEOPLE_DIR]:
    d.mkdir(parents=True, exist_ok=True)

EXISTING = {'dave-jerden', 'rick-rubin', 'flood-producer', 'alan-moulder'}
persons = {}  # slug -> {title, roles, bands:[], song_credits:[]}

def reg(slug, title, roles):
    if slug in EXISTING:
        return
    if slug not in persons:
        persons[slug] = {"title": title, "roles": roles, "bands": [], "song_credits": []}

def band(ps, as_, an, role):
    if ps in EXISTING:
        return
    if ps in persons:
        persons[ps]["bands"].append({"slug": as_, "name": an, "role": role})

def add_sc(ps, ss, st, cr):
    if ps in EXISTING:
        return
    if ps in persons:
        persons[ps]["song_credits"].append({"slug": ss, "title": st, "credit": cr})

def ys(s):
    s = str(s).replace('"', '\\"')
    return f'"{s}"'

def yml_list_str(items):
    return "[" + ", ".join(ys(i) for i in items) + "]"

def mk_artist(aslug, title, scene, btype, genres, formed, members_def, producers_def, albums_data):
    """
    members_def: list of (slug, name, role, person_roles)
    producers_def: list of (slug, name, person_roles)  -- producers to register
    albums_data: list of (album_slug, album_title, year, songs_list, prod_slug)
      songs_list: list of (song_slug, song_title)
    """
    # Register members
    for (pslug, pname, prole, prolelist) in members_def:
        reg(pslug, pname, prolelist)
        band(pslug, aslug, title, prole)

    # Register producers
    for (pslug, pname, prolelist) in producers_def:
        reg(pslug, pname, prolelist)

    # Build albums list for artist file
    albums_yaml = ""
    for (abl_slug, abl_title, abl_year, songs_list, prod_slug) in albums_data:
        albums_yaml += f"  - slug: {ys(abl_slug)}\n    title: {ys(abl_title)}\n    year: {abl_year}\n"

    # Build members list for artist file
    members_yaml = ""
    for (pslug, pname, prole, _) in members_def:
        members_yaml += f"  - slug: {ys(pslug)}\n    name: {ys(pname)}\n    role: {ys(prole)}\n"

    genres_str = yml_list_str(genres)

    artist_content = f"""---
title: {ys(title)}
slug: {ys(aslug)}
scene: {ys(scene)}
band_type: {ys(btype)}
genres: {genres_str}
formed: {formed}
members:
{members_yaml}albums:
{albums_yaml}draft: false
---
"""
    (ARTISTS_DIR / f"{aslug}.md").write_text(artist_content, encoding="utf-8")
    print(f"  artist: {aslug}")

    # Write albums and songs
    for (abl_slug, abl_title, abl_year, songs_list, prod_slug) in albums_data:
        songs_yaml = ""
        for (ss, st) in songs_list:
            songs_yaml += f"  - slug: {ys(ss)}\n    title: {ys(st)}\n"

        album_content = f"""---
title: {ys(abl_title)}
slug: {ys(abl_slug)}
artist: {ys(title)}
artist_slug: {ys(aslug)}
year: {abl_year}
genres: {genres_str}
producer: {ys(prod_slug)}
songs:
{songs_yaml}draft: false
---
"""
        (ALBUMS_DIR / f"{abl_slug}.md").write_text(album_content, encoding="utf-8")
        print(f"    album: {abl_slug}")

        # Write songs
        for (ss, st) in songs_list:
            credits_yaml = ""
            for (pslug, pname, prole, _) in members_def:
                credits_yaml += f"  - person_slug: {ys(pslug)}\n    role: {ys(prole)}\n"
            credits_yaml += f"  - person_slug: {ys(prod_slug)}\n    role: {ys('Producer')}\n"

            song_content = f"""---
title: {ys(st)}
slug: {ys(ss)}
artist: {ys(aslug)}
album: {ys(abl_slug)}
year: {abl_year}
credits:
{credits_yaml}draft: false
---
"""
            (SONGS_DIR / f"{ss}.md").write_text(song_content, encoding="utf-8")

            # Add song_credits to members
            for (pslug, pname, prole, _) in members_def:
                add_sc(pslug, ss, st, prole)
            # Add song_credit to producer
            add_sc(prod_slug, ss, st, "Producer")

        print(f"      songs: {len(songs_list)}")


print("=== Creating 26 Rock Artists ===")

# 1. Twenty One Pilots
mk_artist(
    "twenty-one-pilots", "Twenty One Pilots", "Alternative Rock", "Group",
    ["alternative rock", "indie pop"],
    2009,
    [
        ("tyler-joseph", "Tyler Joseph", "Vocals, Keys", ["Vocalist", "Songwriter", "Multi-instrumentalist"]),
        ("josh-dun", "Josh Dun", "Drums", ["Drummer"]),
    ],
    [("greg-wells", "Greg Wells", ["Producer"])],
    [
        ("vessel-tol", "Vessel", 2013, [
            ("stressed-out-tol", "Stressed Out"),
            ("holding-on-to-you-tol", "Holding On to You"),
            ("car-radio-tol", "Car Radio"),
            ("semi-automatic-tol", "Semi-Automatic"),
            ("screen-tol", "Screen"),
            ("the-run-and-go-tol", "The Run and Go"),
            ("migraine-tol", "Migraine"),
            ("trees-tol", "Trees"),
        ], "greg-wells"),
        ("blurryface", "Blurryface", 2015, [
            ("heavydirtysoul-tol", "HeavyDirtySoul"),
            ("ride-tol", "Ride"),
            ("tear-in-my-heart-tol", "Tear in My Heart"),
            ("lane-boy-tol", "Lane Boy"),
            ("the-judge-tol", "The Judge"),
            ("doubt-tol", "Doubt"),
            ("polarize-tol", "Polarize"),
            ("we-dont-believe-whats-on-tv-tol", "We Don't Believe What's on TV"),
            ("not-today-tol", "Not Today"),
        ], "greg-wells"),
        ("trench", "Trench", 2018, [
            ("jumpsuit-tol", "Jumpsuit"),
            ("levitate-tol", "Levitate"),
            ("morph-tol", "Morph"),
            ("my-blood-tol", "My Blood"),
            ("neon-gravestones-tol", "Neon Gravestones"),
            ("cut-my-lip-tol", "Cut My Lip"),
            ("smithereens-tol", "Smithereens"),
            ("nico-and-the-niners-tol", "Nico and the Niners"),
        ], "greg-wells"),
        ("scaled-and-icy", "Scaled and Icy", 2021, [
            ("good-day-tol", "Good Day"),
            ("choker-tol", "Choker"),
            ("shy-away-tol", "Shy Away"),
            ("the-outside-tol", "The Outside"),
            ("never-take-it-tol", "Never Take It"),
            ("mulberry-street-tol", "Mulberry Street"),
            ("formidable-tol", "Formidable"),
            ("bounce-man-tol", "Bounce Man"),
        ], "greg-wells"),
    ]
)

# 2. Imagine Dragons
mk_artist(
    "imagine-dragons", "Imagine Dragons", "Alternative Rock", "Group",
    ["alternative rock", "pop rock"],
    2008,
    [
        ("dan-reynolds", "Dan Reynolds", "Vocals", ["Vocalist", "Songwriter"]),
        ("wayne-sermon", "Wayne Sermon", "Guitar", ["Guitarist"]),
        ("ben-mckee", "Ben McKee", "Bass", ["Bassist"]),
        ("daniel-platzman", "Daniel Platzman", "Drums", ["Drummer"]),
    ],
    [("alex-da-kid", "Alex da Kid", ["Producer"])],
    [
        ("night-visions", "Night Visions", 2012, [
            ("radioactive-id", "Radioactive"),
            ("demons-id", "Demons"),
            ("its-time-id", "It's Time"),
            ("on-top-of-the-world-id", "On Top of the World"),
            ("amsterdam-id", "Amsterdam"),
            ("hear-me-id", "Hear Me"),
            ("every-night-id", "Every Night"),
            ("nothing-left-to-say-id", "Nothing Left to Say"),
        ], "alex-da-kid"),
        ("smoke-mirrors", "Smoke + Mirrors", 2015, [
            ("shots-id", "Shots"),
            ("gold-id", "Gold"),
            ("smoke-and-mirrors-id", "Smoke and Mirrors"),
            ("i-bet-my-life-id", "I Bet My Life"),
            ("friction-id", "Friction"),
            ("it-comes-back-to-you-id", "It Comes Back to You"),
            ("dream-id", "Dream"),
            ("thieves-id", "Thieves"),
            ("polaroid-id", "Polaroid"),
        ], "alex-da-kid"),
        ("evolve-id", "Evolve", 2017, [
            ("believer-id", "Believer"),
            ("thunder-id", "Thunder"),
            ("whatever-it-takes-id", "Whatever It Takes"),
            ("walking-the-wire-id", "Walking the Wire"),
            ("rise-up-id", "Rise Up"),
            ("i-dont-know-why-id", "I Don't Know Why"),
            ("start-over-id", "Start Over"),
            ("mouth-of-the-river-id", "Mouth of the River"),
        ], "alex-da-kid"),
        ("mercury-id", "Mercury - Act 1", 2021, [
            ("cutthroat-id", "Cutthroat"),
            ("wrecked-id", "Wrecked"),
            ("dull-knives-id", "Dull Knives"),
            ("follow-you-id", "Follow You"),
            ("my-life-id", "My Life"),
            ("enemy-id", "Enemy"),
            ("breath-id", "Breath"),
            ("giants-id", "Giants"),
        ], "alex-da-kid"),
    ]
)

# 3. Paramore
mk_artist(
    "paramore", "Paramore", "Alternative Rock", "Group",
    ["alternative rock", "pop punk"],
    2004,
    [
        ("hayley-williams", "Hayley Williams", "Vocals", ["Vocalist", "Songwriter"]),
        ("taylor-york", "Taylor York", "Guitar", ["Guitarist", "Songwriter"]),
        ("zac-farro", "Zac Farro", "Drums", ["Drummer"]),
    ],
    [("justin-meldal-johnsen", "Justin Meldal-Johnsen", ["Producer"])],
    [
        ("all-we-know-is-falling", "All We Know Is Falling", 2005, [
            ("pressure-par", "Pressure"),
            ("emergency-par", "Emergency"),
            ("never-let-this-go-par", "Never Let This Go"),
            ("brighter-par", "Brighter"),
            ("here-we-go-again-par", "Here We Go Again"),
            ("my-heart-par", "My Heart"),
            ("whoa-par", "Whoa"),
            ("franklin-par", "Franklin"),
        ], "justin-meldal-johnsen"),
        ("riot-par", "Riot!", 2007, [
            ("misery-business-par", "Misery Business"),
            ("hallelujah-par", "Hallelujah"),
            ("for-a-pessimist-im-pretty-optimistic-par", "For a Pessimist, I'm Pretty Optimistic"),
            ("thats-what-you-get-par", "That's What You Get"),
            ("fences-par", "Fences"),
            ("born-for-this-par", "Born for This"),
            ("we-are-broken-par", "We Are Broken"),
            ("crushcrushcrush-par", "crushcrushcrush"),
            ("when-it-rains-par", "When It Rains"),
        ], "justin-meldal-johnsen"),
        ("brand-new-eyes", "Brand New Eyes", 2009, [
            ("careful-par", "Careful"),
            ("ignorance-par", "Ignorance"),
            ("playing-god-par", "Playing God"),
            ("brick-by-boring-brick-par", "Brick by Boring Brick"),
            ("turn-it-off-par", "Turn It Off"),
            ("the-only-exception-par", "The Only Exception"),
            ("feeling-sorry-par", "Feeling Sorry"),
            ("looking-up-par", "Looking Up"),
        ], "justin-meldal-johnsen"),
        ("paramore-self", "Paramore", 2013, [
            ("fast-in-my-car-par", "Fast in My Car"),
            ("now-par", "Now"),
            ("still-into-you-par", "Still Into You"),
            ("anklebiters-par", "Anklebiters"),
            ("grow-up-par", "Grow Up"),
            ("be-alone-par", "Be Alone"),
            ("hate-to-see-your-heart-break-par", "Hate to See Your Heart Break"),
            ("(one-of-those)-crazy-girls-par", "(One of Those) Crazy Girls"),
            ("interlude-holiday-par", "Interlude: Holiday"),
        ], "justin-meldal-johnsen"),
        ("after-laughter", "After Laughter", 2017, [
            ("hard-times-par", "Hard Times"),
            ("rose-colored-boy-par", "Rose-Colored Boy"),
            ("told-you-so-par", "Told You So"),
            ("forgiveness-par", "Forgiveness"),
            ("fake-happy-par", "Fake Happy"),
            ("26-par", "26"),
            ("pool-par", "Pool"),
            ("idle-worship-par", "Idle Worship"),
            ("no-friend-par", "No Friend"),
        ], "justin-meldal-johnsen"),
    ]
)

# 4. My Chemical Romance
mk_artist(
    "my-chemical-romance", "My Chemical Romance", "Alternative Rock", "Group",
    ["alternative rock", "emo", "post-hardcore"],
    2001,
    [
        ("gerard-way", "Gerard Way", "Vocals", ["Vocalist", "Songwriter"]),
        ("frank-iero", "Frank Iero", "Guitar", ["Guitarist"]),
        ("ray-toro", "Ray Toro", "Guitar", ["Guitarist"]),
        ("mikey-way", "Mikey Way", "Bass", ["Bassist"]),
    ],
    [("rob-cavallo", "Rob Cavallo", ["Producer"])],
    [
        ("i-brought-you-my-bullets", "I Brought You My Bullets, You Brought Me Your Love", 2002, [
            ("im-not-okay-mcr", "I'm Not Okay (I Promise)"),
            ("honey-this-mirror-mcr", "Honey, This Mirror Isn't Big Enough for the Two of Us"),
            ("vampires-will-never-hurt-you-mcr", "Vampires Will Never Hurt You"),
            ("headfirst-for-halos-mcr", "Headfirst for Halos"),
            ("skylines-and-turnstiles-mcr", "Skylines and Turnstiles"),
            ("early-sunsets-over-monroeville-mcr", "Early Sunsets Over Monroeville"),
            ("our-lady-of-sorrows-mcr", "Our Lady of Sorrows"),
            ("drowning-lessons-mcr", "Drowning Lessons"),
        ], "rob-cavallo"),
        ("three-cheers-mcr", "Three Cheers for Sweet Revenge", 2004, [
            ("helena-mcr", "Helena"),
            ("the-ghost-of-you-mcr", "The Ghost of You"),
            ("i-never-told-you-what-i-do-for-a-living-mcr", "I Never Told You What I Do for a Living"),
            ("to-the-end-mcr", "To the End"),
            ("you-know-what-they-do-mcr", "You Know What They Do to Guys Like Us in Prison"),
            ("im-not-okay-mcr2", "I'm Not Okay (I Promise) [Alt]"),
            ("thank-you-for-the-venom-mcr", "Thank You for the Venom"),
            ("hang-em-high-mcr", "Hang 'Em High"),
        ], "rob-cavallo"),
        ("black-parade", "The Black Parade", 2006, [
            ("welcome-to-the-black-parade-mcr", "Welcome to the Black Parade"),
            ("famous-last-words-mcr", "Famous Last Words"),
            ("cancer-mcr", "Cancer"),
            ("i-dont-love-you-mcr", "I Don't Love You"),
            ("house-of-wolves-mcr", "House of Wolves"),
            ("dead-mcr", "Dead!"),
            ("sleep-mcr", "Sleep"),
            ("teenagers-mcr", "Teenagers"),
            ("disenchanted-mcr", "Disenchanted"),
        ], "rob-cavallo"),
        ("danger-days", "Danger Days: The True Lives of the Fabulous Killjoys", 2010, [
            ("na-na-na-mcr", "Na Na Na (Na Na Na Na Na Na Na Na Na)"),
            ("sing-mcr", "SING"),
            ("planetary-go-mcr", "Planetary (GO!)"),
            ("destroya-mcr", "Destroya"),
            ("the-kids-from-yesterday-mcr", "The Kids from Yesterday"),
            ("goodnite-dr-death-mcr", "Goodnite, Dr. Death"),
            ("bulletproof-heart-mcr", "Bulletproof Heart"),
            ("summerboy-mcr", "S/C/A/R/E/C/R/O/W"),
        ], "rob-cavallo"),
    ]
)

# 5. Green Day
mk_artist(
    "green-day", "Green Day", "Alternative Rock", "Group",
    ["alternative rock", "punk rock"],
    1987,
    [
        ("billie-joe-armstrong", "Billie Joe Armstrong", "Vocals, Guitar", ["Vocalist", "Guitarist", "Songwriter"]),
        ("mike-dirnt", "Mike Dirnt", "Bass", ["Bassist"]),
        ("tre-cool", "Tré Cool", "Drums", ["Drummer"]),
    ],
    [("rob-cavallo", "Rob Cavallo", ["Producer"])],
    [
        ("dookie", "Dookie", 1994, [
            ("basket-case-gd", "Basket Case"),
            ("when-i-come-around-gd", "When I Come Around"),
            ("longview-gd", "Longview"),
            ("welcome-to-paradise-gd", "Welcome to Paradise"),
            ("she-gd", "She"),
            ("coming-clean-gd", "Coming Clean"),
            ("sassafras-roots-gd", "Sassafras Roots"),
            ("in-the-end-gd", "In the End"),
            ("emenius-sleepus-gd", "Emenius Sleepus"),
        ], "rob-cavallo"),
        ("insomniac-gd", "Insomniac", 1995, [
            ("geek-stink-breath-gd", "Geek Stink Breath"),
            ("brain-stew-gd", "Brain Stew"),
            ("jaded-gd", "Jaded"),
            ("walking-contradiction-gd", "Walking Contradiction"),
            ("brat-gd", "Brat"),
            ("stuck-with-me-gd", "Stuck with Me"),
            ("86-gd", "86"),
            ("panic-song-gd", "Panic Song"),
        ], "rob-cavallo"),
        ("nimrod-gd", "Nimrod", 1997, [
            ("good-riddance-gd", "Good Riddance (Time of Your Life)"),
            ("hitchin-a-ride-gd", "Hitchin' a Ride"),
            ("the-grouch-gd", "The Grouch"),
            ("redundant-gd", "Redundant"),
            ("scattered-gd", "Scattered"),
            ("all-the-time-gd", "All the Time"),
            ("worry-rock-gd", "Worry Rock"),
            ("uptight-gd", "Uptight"),
        ], "rob-cavallo"),
        ("american-idiot", "American Idiot", 2004, [
            ("american-idiot-gd", "American Idiot"),
            ("jesus-of-suburbia-gd", "Jesus of Suburbia"),
            ("boulevard-of-broken-dreams-gd", "Boulevard of Broken Dreams"),
            ("holiday-gd", "Holiday"),
            ("are-we-the-waiting-gd", "Are We the Waiting"),
            ("st-jimmy-gd", "St. Jimmy"),
            ("give-me-novacaine-gd", "Give Me Novacaine"),
            ("she-s-a-rebel-gd", "She's a Rebel"),
            ("wake-me-up-when-september-ends-gd", "Wake Me Up When September Ends"),
        ], "rob-cavallo"),
        ("21st-century-gd", "21st Century Breakdown", 2009, [
            ("know-your-enemy-gd", "Know Your Enemy"),
            ("21-guns-gd", "21 Guns"),
            ("before-the-lobotomy-gd", "Before the Lobotomy"),
            ("christian-inferno-gd", "Christian's Inferno"),
            ("last-night-on-earth-gd", "Last Night on Earth"),
            ("east-jesus-nowhere-gd", "East Jesus Nowhere"),
            ("peacemaker-gd", "Peacemaker"),
            ("murder-city-gd", "Murder City"),
        ], "rob-cavallo"),
    ]
)

# 6. The Killers
mk_artist(
    "the-killers", "The Killers", "Alternative Rock", "Group",
    ["alternative rock", "indie rock"],
    2001,
    [
        ("brandon-flowers", "Brandon Flowers", "Vocals, Keys", ["Vocalist", "Songwriter"]),
        ("dave-keuning", "Dave Keuning", "Guitar", ["Guitarist"]),
        ("mark-stoermer", "Mark Stoermer", "Bass", ["Bassist"]),
        ("ronnie-vannucci", "Ronnie Vannucci Jr.", "Drums", ["Drummer"]),
    ],
    [("flood-producer", "Flood", ["Producer"]), ("alan-moulder", "Alan Moulder", ["Producer"])],
    [
        ("hot-fuss", "Hot Fuss", 2004, [
            ("mr-brightside-kl", "Mr. Brightside"),
            ("somebody-told-me-kl", "Somebody Told Me"),
            ("all-these-things-that-ive-done-kl", "All These Things That I've Done"),
            ("indie-rock-and-roll-kl", "Indie Rock & Roll"),
            ("on-top-kl", "On Top"),
            ("change-your-mind-kl", "Change Your Mind"),
            ("believe-me-natalie-kl", "Believe Me Natalie"),
            ("midnight-show-kl", "Midnight Show"),
            ("jenny-was-a-friend-of-mine-kl", "Jenny Was a Friend of Mine"),
        ], "flood-producer"),
        ("sams-town", "Sam's Town", 2006, [
            ("when-you-were-young-kl", "When You Were Young"),
            ("enterlude-kl", "Enterlude"),
            ("for-reasons-unknown-kl", "For Reasons Unknown"),
            ("read-my-mind-kl", "Read My Mind"),
            ("uncle-jonny-kl", "Uncle Jonny"),
            ("bones-kl", "Bones"),
            ("my-list-kl", "My List"),
            ("this-river-is-wild-kl", "This River Is Wild"),
            ("why-do-i-keep-counting-kl", "Why Do I Keep Counting"),
        ], "flood-producer"),
        ("day-age", "Day & Age", 2008, [
            ("human-kl", "Human"),
            ("spaceman-kl", "Spaceman"),
            ("joy-ride-kl", "Joy Ride"),
            ("a-dustland-fairytale-kl", "A Dustland Fairytale"),
            ("this-is-your-life-kl", "This Is Your Life"),
            ("i-cant-stay-kl", "I Can't Stay"),
            ("neon-tiger-kl", "Neon Tiger"),
            ("the-world-we-live-in-kl", "The World We Live In"),
        ], "flood-producer"),
        ("battle-born", "Battle Born", 2012, [
            ("runaways-kl", "Runaways"),
            ("the-way-it-was-kl", "The Way It Was"),
            ("here-with-me-kl", "Here with Me"),
            ("a-matter-of-time-kl", "A Matter of Time"),
            ("deadlines-and-commitments-kl", "Deadlines and Commitments"),
            ("miss-atomic-bomb-kl", "Miss Atomic Bomb"),
            ("the-rising-tide-kl", "The Rising Tide"),
            ("heart-of-a-girl-kl", "Heart of a Girl"),
            ("from-here-on-out-kl", "From Here on Out"),
        ], "flood-producer"),
    ]
)

# 7. Arctic Monkeys
mk_artist(
    "arctic-monkeys", "Arctic Monkeys", "Indie Rock", "Group",
    ["indie rock", "alternative rock"],
    2002,
    [
        ("alex-turner", "Alex Turner", "Vocals, Guitar", ["Vocalist", "Guitarist", "Songwriter"]),
        ("jamie-cook", "Jamie Cook", "Guitar", ["Guitarist"]),
        ("nick-o-malley", "Nick O'Malley", "Bass", ["Bassist"]),
        ("matt-helders", "Matt Helders", "Drums", ["Drummer"]),
    ],
    [("james-ford-am", "James Ford", ["Producer"])],
    [
        ("whatever-people-say", "Whatever People Say I Am, That's What I'm Not", 2006, [
            ("i-bet-you-look-good-on-the-dancefloor-am", "I Bet You Look Good on the Dancefloor"),
            ("fake-tales-of-san-francisco-am", "Fake Tales of San Francisco"),
            ("dancing-shoes-am", "Dancing Shoes"),
            ("you-probably-couldnt-see-am", "You Probably Couldn't See for the Lights but You Were Staring Straight at Me"),
            ("the-stars-are-blind-am", "The Stars Are Blind"),
            ("from-the-ritz-to-the-rubble-am", "From the Ritz to the Rubble"),
            ("a-certain-romance-am", "A Certain Romance"),
            ("still-take-you-home-am", "Still Take You Home"),
        ], "james-ford-am"),
        ("favourite-worst-nightmare", "Favourite Worst Nightmare", 2007, [
            ("brianstorm-am", "Brianstorm"),
            ("teddy-picker-am", "Teddy Picker"),
            ("d-is-for-dangerous-am", "D Is for Dangerous"),
            ("balaclava-am", "Balaclava"),
            ("fluorescent-adolescent-am", "Fluorescent Adolescent"),
            ("only-ones-who-know-am", "Only Ones Who Know"),
            ("do-me-a-favour-am", "Do Me a Favour"),
            ("this-house-is-a-circus-am", "This House Is a Circus"),
        ], "james-ford-am"),
        ("humbug-am", "Humbug", 2009, [
            ("my-propeller-am", "My Propeller"),
            ("crying-lightning-am", "Crying Lightning"),
            ("dangerous-animals-am", "Dangerous Animals"),
            ("secret-door-am", "Secret Door"),
            ("potion-approaching-am", "Potion Approaching"),
            ("fire-and-the-thud-am", "Fire and the Thud"),
            ("cornerstone-am", "Cornerstone"),
            ("the-jeweller-s-hands-am", "The Jeweller's Hands"),
        ], "james-ford-am"),
        ("am-arcticmonkeys", "AM", 2013, [
            ("do-i-wanna-know-am", "Do I Wanna Know?"),
            ("r-u-mine-am", "R U Mine?"),
            ("one-for-the-road-am", "One for the Road"),
            ("arabella-am", "Arabella"),
            ("i-want-it-all-am", "I Want It All"),
            ("no-1-party-anthem-am", "No. 1 Party Anthem"),
            ("mad-sounds-am", "Mad Sounds"),
            ("fireside-am", "Fireside"),
            ("why-d-you-only-call-me-when-youre-high-am", "Why'd You Only Call Me When You're High?"),
        ], "james-ford-am"),
    ]
)

# 8. Muse
mk_artist(
    "muse", "Muse", "Alternative Rock", "Group",
    ["alternative rock", "progressive rock"],
    1994,
    [
        ("matt-bellamy", "Matt Bellamy", "Vocals, Guitar, Keys", ["Vocalist", "Guitarist", "Songwriter"]),
        ("chris-wolstenholme", "Chris Wolstenholme", "Bass", ["Bassist"]),
        ("dominic-howard", "Dominic Howard", "Drums", ["Drummer"]),
    ],
    [("john-leckie", "John Leckie", ["Producer"])],
    [
        ("showbiz-ms", "Showbiz", 1999, [
            ("sunburn-ms", "Sunburn"),
            ("muscle-museum-ms", "Muscle Museum"),
            ("fillip-ms", "Fillip"),
            ("falling-down-ms", "Falling Down"),
            ("cave-ms", "Cave"),
            ("showbiz-ms-song", "Showbiz"),
            ("unintended-ms", "Unintended"),
            ("uno-ms", "Uno"),
        ], "john-leckie"),
        ("origin-of-symmetry", "Origin of Symmetry", 2001, [
            ("new-born-ms", "New Born"),
            ("bliss-ms", "Bliss"),
            ("space-dementia-ms", "Space Dementia"),
            ("hyper-music-ms", "Hyper Music"),
            ("plug-in-baby-ms", "Plug In Baby"),
            ("citizen-erased-ms", "Citizen Erased"),
            ("micro-cuts-ms", "Micro Cuts"),
            ("dark-shines-ms", "Dark Shines"),
            ("feeling-good-ms", "Feeling Good"),
        ], "john-leckie"),
        ("absolution-ms", "Absolution", 2003, [
            ("intro-ms", "Intro"),
            ("apocalypse-please-ms", "Apocalypse Please"),
            ("time-is-running-out-ms", "Time Is Running Out"),
            ("sing-for-absolution-ms", "Sing for Absolution"),
            ("stockholm-syndrome-ms", "Stockholm Syndrome"),
            ("hysteria-ms", "Hysteria"),
            ("blackout-ms", "Blackout"),
            ("butterflies-and-hurricanes-ms", "Butterflies and Hurricanes"),
            ("the-small-print-ms", "The Small Print"),
        ], "john-leckie"),
        ("black-holes-ms", "Black Holes and Revelations", 2006, [
            ("take-a-bow-ms", "Take a Bow"),
            ("starlight-ms", "Starlight"),
            ("supermassive-black-hole-ms", "Supermassive Black Hole"),
            ("map-of-the-problematique-ms", "Map of the Problematique"),
            ("soldier-s-poem-ms", "Soldier's Poem"),
            ("invincible-ms", "Invincible"),
            ("assassin-ms", "Assassin"),
            ("exo-politics-ms", "Exo-Politics"),
            ("city-of-delusion-ms", "City of Delusion"),
        ], "john-leckie"),
        ("resistance-ms", "The Resistance", 2009, [
            ("uprising-ms", "Uprising"),
            ("resistance-ms-song", "Resistance"),
            ("undisclosed-desires-ms", "Undisclosed Desires"),
            ("united-states-of-eurasia-ms", "United States of Eurasia"),
            ("guiding-light-ms", "Guiding Light"),
            ("unnatural-selection-ms", "Unnatural Selection"),
            ("mk-ultra-ms", "MK Ultra"),
            ("i-belong-to-you-ms", "I Belong to You"),
            ("exogenesis-symphony-ms", "Exogenesis: Symphony Part 1"),
        ], "matt-bellamy"),
    ]
)

# 9. Weezer
mk_artist(
    "weezer", "Weezer", "Alternative Rock", "Group",
    ["alternative rock", "power pop"],
    1992,
    [
        ("rivers-cuomo", "Rivers Cuomo", "Vocals, Guitar", ["Vocalist", "Guitarist", "Songwriter"]),
        ("pat-wilson-wz", "Patrick Wilson", "Drums", ["Drummer"]),
        ("brian-bell", "Brian Bell", "Guitar", ["Guitarist"]),
        ("scott-shriner", "Scott Shriner", "Bass", ["Bassist"]),
    ],
    [("rick-rubin", "Rick Rubin", ["Producer"])],
    [
        ("weezer-blue", "Weezer (Blue Album)", 1994, [
            ("undone-the-sweater-song-wz", "Undone - The Sweater Song"),
            ("buddy-holly-wz", "Buddy Holly"),
            ("in-the-garage-wz", "In the Garage"),
            ("holiday-wz", "Holiday"),
            ("the-world-has-turned-wz", "The World Has Turned and Left Me Here"),
            ("no-one-else-wz", "No One Else"),
            ("my-name-is-jonas-wz", "My Name Is Jonas"),
            ("say-it-aint-so-wz", "Say It Ain't So"),
        ], "rick-rubin"),
        ("pinkerton-wz", "Pinkerton", 1996, [
            ("tired-of-sex-wz", "Tired of Sex"),
            ("getchoo-wz", "Getchoo"),
            ("no-other-one-wz", "No Other One"),
            ("why-bother-wz", "Why Bother?"),
            ("across-the-sea-wz", "Across the Sea"),
            ("the-good-life-wz", "The Good Life"),
            ("el-scorcho-wz", "El Scorcho"),
            ("pink-triangle-wz", "Pink Triangle"),
            ("falling-for-you-wz", "Falling for You"),
        ], "rick-rubin"),
        ("weezer-green", "Weezer (Green Album)", 2001, [
            ("hash-pipe-wz", "Hash Pipe"),
            ("island-in-the-sun-wz", "Island in the Sun"),
            ("crab-wz", "Crab"),
            ("knockdown-dragout-wz", "Knockdown Dragout"),
            ("smile-wz", "Smile"),
            ("draft-wz", "Draft"),
            ("glorious-day-wz", "Glorious Day"),
            ("o-girlfriend-wz", "O Girlfriend"),
        ], "rick-rubin"),
        ("maladroit-wz", "Maladroit", 2002, [
            ("dope-nose-wz", "Dope Nose"),
            ("keep-fishin-wz", "Keep Fishin'"),
            ("take-control-wz", "Take Control"),
            ("death-and-destruction-wz", "Death and Destruction"),
            ("peace-wz", "Peace"),
            ("slob-wz", "Slob"),
            ("burndt-jamb-wz", "Burndt Jamb"),
            ("space-rock-wz", "Space Rock"),
        ], "rick-rubin"),
    ]
)

# 10. Blink-182
mk_artist(
    "blink-182", "Blink-182", "Alternative Rock", "Group",
    ["alternative rock", "pop punk"],
    1992,
    [
        ("tom-delonge", "Tom DeLonge", "Vocals, Guitar", ["Vocalist", "Guitarist"]),
        ("mark-hoppus", "Mark Hoppus", "Vocals, Bass", ["Vocalist", "Bassist"]),
        ("travis-barker", "Travis Barker", "Drums", ["Drummer"]),
    ],
    [("jerry-finn", "Jerry Finn", ["Producer"])],
    [
        ("enema-bl", "Enema of the State", 1999, [
            ("all-the-small-things-bl", "All the Small Things"),
            ("whats-my-age-again-bl", "What's My Age Again?"),
            ("adams-song-bl", "Adam's Song"),
            ("dumpweed-bl", "Dumpweed"),
            ("dont-leave-me-bl", "Don't Leave Me"),
            ("alienated-bl", "Alienated"),
            ("mutt-bl", "Mutt"),
            ("going-away-to-college-bl", "Going Away to College"),
        ], "jerry-finn"),
        ("take-off-bl", "Take Off Your Pants and Jacket", 2001, [
            ("the-rock-show-bl", "The Rock Show"),
            ("stay-together-bl", "Stay Together for the Kids"),
            ("first-date-bl", "First Date"),
            ("happy-holidays-bl", "Happy Holidays, You Bastard"),
            ("more-than-meets-the-eye-bl", "More Than Meets the Eye"),
            ("please-take-me-home-bl", "Please Take Me Home"),
            ("story-of-a-lonely-guy-bl", "Story of a Lonely Guy"),
            ("the-fallen-interlude-bl", "The Fallen Interlude"),
        ], "jerry-finn"),
        ("blink182-self", "Blink-182 (Self-Titled)", 2003, [
            ("feeling-this-bl", "Feeling This"),
            ("i-miss-you-bl", "I Miss You"),
            ("violence-bl", "Violence"),
            ("down-bl", "Down"),
            ("go-bl", "Go"),
            ("always-bl", "Always"),
            ("im-lost-without-you-bl", "I'm Lost Without You"),
            ("asthenia-bl", "Asthenia"),
        ], "jerry-finn"),
        ("neighborhoods-bl", "Neighborhoods", 2011, [
            ("up-all-night-bl", "Up All Night"),
            ("after-midnight-bl", "After Midnight"),
            ("hearts-all-gone-bl", "Hearts All Gone"),
            ("ghost-on-the-dance-floor-bl", "Ghost on the Dance Floor"),
            ("kaleidoscope-bl", "Kaleidoscope"),
            ("wishing-well-bl", "Wishing Well"),
            ("moon-over-california-bl", "Moon Over California"),
            ("natives-bl", "Natives"),
        ], "jerry-finn"),
    ]
)

# 11. The Offspring
mk_artist(
    "the-offspring", "The Offspring", "Alternative Rock", "Group",
    ["alternative rock", "punk rock"],
    1984,
    [
        ("dexter-holland", "Dexter Holland", "Vocals", ["Vocalist", "Songwriter"]),
        ("noodles-offspring", "Noodles", "Guitar", ["Guitarist"]),
        ("greg-k", "Greg K.", "Bass", ["Bassist"]),
        ("ron-welty", "Ron Welty", "Drums", ["Drummer"]),
    ],
    [("dave-jerden", "Dave Jerden", ["Producer"])],
    [
        ("smash-of", "Smash", 1994, [
            ("self-esteem-of", "Self Esteem"),
            ("come-out-and-play-of", "Come Out and Play"),
            ("gotta-get-away-of", "Gotta Get Away"),
            ("bad-habit-of", "Bad Habit"),
            ("genocide-of", "Genocide"),
            ("something-to-believe-in-of", "Something to Believe In"),
            ("not-the-one-of", "Not the One"),
            ("smash-of-song", "Smash"),
        ], "dave-jerden"),
        ("ixnay-of", "Ixnay on the Hombre", 1997, [
            ("all-i-want-of", "All I Want"),
            ("gone-away-of", "Gone Away"),
            ("i-choose-of", "I Choose"),
            ("intermission-of", "Intermission"),
            ("cool-to-hate-of", "Cool to Hate"),
            ("leave-it-behind-of", "Leave It Behind"),
            ("the-sprawl-of", "The Sprawl"),
            ("don-t-pick-it-up-of", "Don't Pick It Up"),
        ], "dave-jerden"),
        ("americana-of", "Americana", 1998, [
            ("pretty-fly-of", "Pretty Fly (for a White Guy)"),
            ("why-don-t-you-get-a-job-of", "Why Don't You Get a Job?"),
            ("the-kids-arent-alright-of", "The Kids Aren't Alright"),
            ("she-s-got-issues-of", "She's Got Issues"),
            ("walla-walla-of", "Walla Walla"),
            ("the-end-of-the-line-of", "The End of the Line"),
            ("no-brakes-of", "No Brakes"),
            ("staring-at-the-sun-of", "Staring at the Sun"),
        ], "dave-jerden"),
        ("conspiracy-of", "Conspiracy of One", 2000, [
            ("original-prankster-of", "Original Prankster"),
            ("want-you-bad-of", "Want You Bad"),
            ("million-miles-away-of", "Million Miles Away"),
            ("dammit-i-changed-again-of", "Dammit, I Changed Again"),
            ("living-in-chaos-of", "Living in Chaos"),
            ("special-delivery-of", "Special Delivery"),
            ("one-fine-day-of", "One Fine Day"),
            ("all-along-of", "All Along"),
        ], "dave-jerden"),
    ]
)

# 12. Fall Out Boy
mk_artist(
    "fall-out-boy", "Fall Out Boy", "Alternative Rock", "Group",
    ["alternative rock", "pop punk", "emo"],
    2001,
    [
        ("pete-wentz", "Pete Wentz", "Bass, Lyrics", ["Bassist", "Songwriter"]),
        ("patrick-stump", "Patrick Stump", "Vocals, Guitar", ["Vocalist", "Guitarist"]),
        ("joe-trohman", "Joe Trohman", "Guitar", ["Guitarist"]),
        ("andy-hurley", "Andy Hurley", "Drums", ["Drummer"]),
    ],
    [("neal-avron", "Neal Avron", ["Producer"])],
    [
        ("take-this-fob", "Take This to Your Grave", 2003, [
            ("dead-on-arrival-fob", "Dead on Arrival"),
            ("grand-theft-autumn-fob", "Grand Theft Autumn/Where Is Your Boy"),
            ("saturday-fob", "Saturday"),
            ("homesick-at-space-camp-fob", "Homesick at Space Camp"),
            ("calm-before-the-storm-fob", "Calm Before the Storm"),
            ("reinventing-the-wheel-fob", "Reinventing the Wheel to Run Myself Over"),
            ("the-patron-saint-of-liars-fob", "The Patron Saint of Liars and Fakes"),
            ("chicago-is-so-two-years-ago-fob", "Chicago Is So Two Years Ago"),
        ], "neal-avron"),
        ("from-under-fob", "From Under the Cork Tree", 2005, [
            ("sugar-were-goin-down-fob", "Sugar, We're Goin Down"),
            ("dance-dance-fob", "Dance, Dance"),
            ("a-little-less-sixteen-candles-fob", "A Little Less Sixteen Candles, a Little More 'Touch Me'"),
            ("i-ve-got-a-dark-alley-fob", "I've Got a Dark Alley and a Bad Idea That Says You Should Shut Your Mouth Summer"),
            ("7-minutes-in-heaven-fob", "7 Minutes in Heaven (Atavan Halen)"),
            ("the-pros-and-cons-fob", "The Pros and Cons of Breathing"),
            ("our-lawyer-made-us-change-fob", "Our Lawyer Made Us Change the Name of This Song So We Wouldn't Get Sued"),
            ("nobody-puts-baby-in-the-corner-fob", "Nobody Puts Baby in the Corner"),
        ], "neal-avron"),
        ("infinity-on-high-fob", "Infinity on High", 2007, [
            ("this-aint-a-scene-fob", "This Ain't a Scene, It's an Arms Race"),
            ("the-take-over-fob", "The Take Over, the Breaks Over"),
            ("thnks-fr-th-mmrs-fob", "Thnks fr th Mmrs"),
            ("i-m-like-a-lawyer-fob", "I'm Like a Lawyer with the Way I'm Always Trying to Get You Off (Me & You)"),
            ("hum-hallelujah-fob", "Hum Hallelujah"),
            ("golden-fob", "Golden"),
            ("the-carpal-tunnel-of-love-fob", "The Carpal Tunnel of Love"),
            ("bang-the-doldrums-fob", "Bang the Doldrums"),
        ], "neal-avron"),
        ("folie-fob", "Folie à Deux", 2008, [
            ("i-dont-care-fob", "I Don't Care"),
            ("she-s-my-winona-fob", "She's My Winona"),
            ("america-s-suitehearts-fob", "America's Suitehearts"),
            ("headfirst-slide-fob", "Headfirst Slide into Cooperstown on a Bad Bet"),
            ("the-(after)-life-fob", "The (After) Life of the Party"),
            ("what-a-catch-donnie-fob", "What a Catch, Donnie"),
            ("twenty-dollar-nose-bleed-fob", "20 Dollar Nose Bleed"),
            ("w-a-m-s-fob", "W.A.M.S."),
        ], "neal-avron"),
    ]
)

# 13. Tool
mk_artist(
    "tool", "Tool", "Alternative Rock", "Group",
    ["alternative rock", "progressive metal", "art rock"],
    1990,
    [
        ("maynard-james-keenan", "Maynard James Keenan", "Vocals", ["Vocalist"]),
        ("adam-jones-tool", "Adam Jones", "Guitar", ["Guitarist"]),
        ("justin-chancellor", "Justin Chancellor", "Bass", ["Bassist"]),
        ("danny-carey", "Danny Carey", "Drums", ["Drummer"]),
    ],
    [("david-bottrill", "David Bottrill", ["Producer"])],
    [
        ("undertow-tl", "Undertow", 1993, [
            ("prison-sex-tl", "Prison Sex"),
            ("sober-tl", "Sober"),
            ("bottom-tl", "Bottom"),
            ("crawl-away-tl", "Crawl Away"),
            ("swamp-song-tl", "Swamp Song"),
            ("undertow-tl-song", "Undertow"),
            ("4-degrees-tl", "4°"),
            ("flood-tl", "Flood"),
        ], "adam-jones-tool"),
        ("aenima-tl", "Ænima", 1996, [
            ("stinkfist-tl", "Stinkfist"),
            ("eulogy-tl", "Eulogy"),
            ("h-tl", "H."),
            ("useful-idiot-tl", "Useful Idiot"),
            ("forty-six-two-tl", "Forty Six & 2"),
            ("message-to-harry-manback-tl", "Message to Harry Manback"),
            ("hooker-with-a-penis-tl", "Hooker with a Penis"),
            ("intermission-tl", "Intermission"),
            ("jimmy-tl", "Jimmy"),
            ("die-eier-von-satan-tl", "Die Eier von Satan"),
        ], "david-bottrill"),
        ("lateralus-tl", "Lateralus", 2001, [
            ("the-grudge-tl", "The Grudge"),
            ("eon-blue-apocalypse-tl", "Eon Blue Apocalypse"),
            ("the-patient-tl", "The Patient"),
            ("mantra-tl", "Mantra"),
            ("schism-tl", "Schism"),
            ("parabol-tl", "Parabol"),
            ("parabola-tl", "Parabola"),
            ("ticks-leeches-tl", "Ticks & Leeches"),
            ("lateralus-tl-song", "Lateralus"),
            ("disposition-tl", "Disposition"),
        ], "david-bottrill"),
        ("10000-days-tl", "10,000 Days", 2006, [
            ("vicarious-tl", "Vicarious"),
            ("jambi-tl", "Jambi"),
            ("wings-for-marie-tl", "Wings for Marie (Pt 1)"),
            ("10000-days-tl-song", "10,000 Days (Wings Pt 2)"),
            ("the-pot-tl", "The Pot"),
            ("lipan-conjuring-tl", "Lipan Conjuring"),
            ("lost-keys-tl", "Lost Keys (Blame Hofmann)"),
            ("rosetta-stoned-tl", "Rosetta Stoned"),
            ("intension-tl", "Intension"),
        ], "david-bottrill"),
        ("fear-inoculum-tl", "Fear Inoculum", 2019, [
            ("fear-inoculum-tl-song", "Fear Inoculum"),
            ("pneuma-tl", "Pneuma"),
            ("litanie-contre-la-peur-tl", "Litanie contre la Peur"),
            ("invincible-tl", "Invincible"),
            ("legion-inoculant-tl", "Legion Inoculant"),
            ("descending-tl", "Descending"),
            ("culling-voices-tl", "Culling Voices"),
            ("chocolate-chip-trip-tl", "Chocolate Chip Trip"),
            ("7empest-tl", "7empest"),
        ], "adam-jones-tool"),
    ]
)

# 14. Jack White (solo)
mk_artist(
    "jack-white", "Jack White", "Rock", "Solo",
    ["rock", "blues rock"],
    2012,
    [
        ("jack-white", "Jack White", "Vocals, Guitar", ["Vocalist", "Guitarist", "Producer", "Songwriter"]),
    ],
    [],
    [
        ("blunderbuss-jw", "Blunderbuss", 2012, [
            ("missing-pieces-jw", "Missing Pieces"),
            ("sixteen-saltines-jw", "Sixteen Saltines"),
            ("freedom-at-21-jw", "Freedom at 21"),
            ("love-interruption-jw", "Love Interruption"),
            ("blunderbuss-jw-song", "Blunderbuss"),
            ("mad-as-a-hatter-jw", "Mad as a Hatter"),
            ("the-length-jw", "The Length"),
            ("hip-eponymous-poor-jw", "Hip (Eponymous) Poor Boy"),
        ], "jack-white"),
        ("lazaretto-jw", "Lazaretto", 2014, [
            ("three-women-jw", "Three Women"),
            ("lazaretto-jw-song", "Lazaretto"),
            ("temporary-ground-jw", "Temporary Ground"),
            ("just-one-drink-jw", "Just One Drink"),
            ("would-you-fight-for-my-love-jw", "Would You Fight for My Love?"),
            ("high-ball-stepper-jw", "High Ball Stepper"),
            ("just-one-drink-alt-jw", "Just One Drink (Acoustic)"),
            ("alone-in-my-home-jw", "Alone in My Home"),
        ], "jack-white"),
        ("boarding-house-jw", "Boarding House Reach", 2018, [
            ("connected-by-love-jw", "Connected by Love"),
            ("why-walk-a-dog-jw", "Why Walk a Dog?"),
            ("corporation-jw", "Corporation"),
            ("abulia-and-akrasia-jw", "Abulia and Akrasia"),
            ("hypermisophoniac-jw", "Hypermisophoniac"),
            ("ice-station-zebra-jw", "Ice Station Zebra"),
            ("over-and-over-and-over-jw", "Over and Over and Over"),
            ("everything-you-ve-ever-learned-jw", "Everything You've Ever Learned"),
        ], "jack-white"),
    ]
)

# 15. The White Stripes
# jack-white already registered as solo artist — just reference, don't re-register
reg("meg-white", "Meg White", ["Drummer"])
band("meg-white", "the-white-stripes", "The White Stripes", "Drums")
band("jack-white", "the-white-stripes", "The White Stripes", "Vocals, Guitar")

ws_albums_data = [
    ("white-blood-cells-ws", "White Blood Cells", 2001, [
        ("fell-in-love-with-a-girl-ws", "Fell in Love with a Girl"),
        ("hotel-yorba-ws", "Hotel Yorba"),
        ("dead-leaves-ws", "Dead Leaves and the Dirty Ground"),
        ("we-re-going-to-be-friends-ws", "We're Going to Be Friends"),
        ("offend-in-every-way-ws", "Offend in Every Way"),
        ("hello-operator-ws", "Hello Operator"),
        ("little-room-ws", "Little Room"),
        ("aluminum-ws", "Aluminum"),
    ], "jack-white"),
    ("elephant-ws", "Elephant", 2003, [
        ("seven-nation-army-ws", "Seven Nation Army"),
        ("black-math-ws", "Black Math"),
        ("there-s-no-home-for-you-here-ws", "There's No Home for You Here"),
        ("i-just-don-t-know-what-to-do-ws", "I Just Don't Know What to Do with Myself"),
        ("in-the-cold-cold-night-ws", "In the Cold Cold Night"),
        ("i-want-to-be-the-boy-ws", "I Want to Be the Boy to Warm Your Mother's Heart"),
        ("you-ve-got-her-in-your-pocket-ws", "You've Got Her in Your Pocket"),
        ("ball-and-biscuit-ws", "Ball and Biscuit"),
    ], "jack-white"),
    ("icky-thump-ws", "Icky Thump", 2007, [
        ("icky-thump-ws-song", "Icky Thump"),
        ("you-don-t-know-what-love-is-ws", "You Don't Know What Love Is (You Just Know What I Want)"),
        ("300-m-p-h-torrential-outpour-blues-ws", "300 M.P.H. Torrential Outpour Blues"),
        ("conquest-ws", "Conquest"),
        ("bone-broke-ws", "Bone Broke"),
        ("prickly-thorn-ws", "Prickly Thorn, but Sweetly Worn"),
        ("st-andrew-ws", "St. Andrew (This Battle Is in the Air)"),
        ("effect-and-cause-ws", "Effect and Cause"),
    ], "jack-white"),
]

ws_members_def = [
    ("jack-white", "Jack White", "Vocals, Guitar", ["Vocalist", "Guitarist", "Producer", "Songwriter"]),
    ("meg-white", "Meg White", "Drums", ["Drummer"]),
]
genres_ws = ["alternative rock", "blues rock", "garage rock"]
genres_str_ws = yml_list_str(genres_ws)

albums_yaml_ws = ""
for (abl_slug, abl_title, abl_year, songs_list, prod_slug) in ws_albums_data:
    albums_yaml_ws += f"  - slug: {ys(abl_slug)}\n    title: {ys(abl_title)}\n    year: {abl_year}\n"

members_yaml_ws = ""
for (pslug, pname, prole, _) in ws_members_def:
    members_yaml_ws += f"  - slug: {ys(pslug)}\n    name: {ys(pname)}\n    role: {ys(prole)}\n"

ws_artist_content = f"""---
title: "The White Stripes"
slug: "the-white-stripes"
scene: "Alternative Rock"
band_type: "Group"
genres: {genres_str_ws}
formed: 1997
members:
{members_yaml_ws}albums:
{albums_yaml_ws}draft: false
---
"""
(ARTISTS_DIR / "the-white-stripes.md").write_text(ws_artist_content, encoding="utf-8")
print("  artist: the-white-stripes")

for (abl_slug, abl_title, abl_year, songs_list, prod_slug) in ws_albums_data:
    songs_yaml = ""
    for (ss, st) in songs_list:
        songs_yaml += f"  - slug: {ys(ss)}\n    title: {ys(st)}\n"
    album_content = f"""---
title: {ys(abl_title)}
slug: {ys(abl_slug)}
artist: "The White Stripes"
artist_slug: "the-white-stripes"
year: {abl_year}
genres: {genres_str_ws}
producer: {ys(prod_slug)}
songs:
{songs_yaml}draft: false
---
"""
    (ALBUMS_DIR / f"{abl_slug}.md").write_text(album_content, encoding="utf-8")
    print(f"    album: {abl_slug}")
    for (ss, st) in songs_list:
        credits_yaml = ""
        for (pslug, pname, prole, _) in ws_members_def:
            credits_yaml += f"  - person_slug: {ys(pslug)}\n    role: {ys(prole)}\n"
        credits_yaml += f"  - person_slug: {ys(prod_slug)}\n    role: \"Producer\"\n"
        song_content = f"""---
title: {ys(st)}
slug: {ys(ss)}
artist: "the-white-stripes"
album: {ys(abl_slug)}
year: {abl_year}
credits:
{credits_yaml}draft: false
---
"""
        (SONGS_DIR / f"{ss}.md").write_text(song_content, encoding="utf-8")
        for (pslug, pname, prole, _) in ws_members_def:
            add_sc(pslug, ss, st, prole)
        add_sc(prod_slug, ss, st, "Producer")
    print(f"      songs: {len(songs_list)}")

# 16. The Black Keys
mk_artist(
    "the-black-keys", "The Black Keys", "Rock", "Group",
    ["rock", "blues rock", "garage rock"],
    2001,
    [
        ("dan-auerbach", "Dan Auerbach", "Vocals, Guitar", ["Vocalist", "Guitarist", "Songwriter"]),
        ("patrick-carney", "Patrick Carney", "Drums", ["Drummer"]),
    ],
    [("danger-mouse-bk", "Danger Mouse", ["Producer"])],
    [
        ("thickfreakness-bk", "Thickfreakness", 2003, [
            ("set-you-free-bk", "Set You Free"),
            ("hard-row-bk", "Hard Row"),
            ("thickfreakness-bk-song", "Thickfreakness"),
            ("in-the-morning-bk", "In the Morning"),
            ("everywhere-i-go-bk", "Everywhere I Go"),
            ("hurt-like-mine-bk", "Hurt Like Mine"),
            ("if-you-see-me-bk", "If You See Me"),
            ("no-trust-bk", "No Trust"),
        ], "dan-auerbach"),
        ("rubber-factory-bk", "Rubber Factory", 2004, [
            ("10-a-m-automatic-bk", "10 A.M. Automatic"),
            ("just-got-to-be-bk", "Just Got to Be"),
            ("stack-shot-billy-bk", "Stack Shot Billy"),
            ("act-nice-and-gentle-bk", "Act Nice and Gentle"),
            ("the-lengths-bk", "The Lengths"),
            ("when-the-lights-go-out-bk", "When the Lights Go Out"),
            ("busted-bk", "Busted"),
            ("grown-so-ugly-bk", "Grown So Ugly"),
        ], "dan-auerbach"),
        ("brothers-bk", "Brothers", 2010, [
            ("howlin-for-you-bk", "Howlin' for You"),
            ("tighten-up-bk", "Tighten Up"),
            ("next-girl-bk", "Next Girl"),
            ("your-touch-bk", "Your Touch"),
            ("she-s-long-gone-bk", "She's Long Gone"),
            ("too-afraid-to-love-you-bk", "Too Afraid to Love You"),
            ("sinister-kid-bk", "Sinister Kid"),
            ("ten-cent-pistol-bk", "Ten Cent Pistol"),
        ], "danger-mouse-bk"),
        ("el-camino-bk", "El Camino", 2011, [
            ("lonely-boy-bk", "Lonely Boy"),
            ("dead-and-gone-bk", "Dead and Gone"),
            ("gold-on-the-ceiling-bk", "Gold on the Ceiling"),
            ("little-black-submarines-bk", "Little Black Submarines"),
            ("money-maker-bk", "Money Maker"),
            ("run-right-back-bk", "Run Right Back"),
            ("sister-bk", "Sister"),
            ("hell-of-a-season-bk", "Hell of a Season"),
        ], "danger-mouse-bk"),
        ("turn-blue-bk", "Turn Blue", 2014, [
            ("weight-of-love-bk", "Weight of Love"),
            ("in-time-bk", "In Time"),
            ("turn-blue-bk-song", "Turn Blue"),
            ("fever-bk", "Fever"),
            ("bullet-in-the-brain-bk", "Bullet in the Brain"),
            ("it-s-up-to-you-now-bk", "It's Up to You Now"),
            ("gotta-get-away-bk", "Gotta Get Away"),
            ("water-worth-bk", "Water Worth"),
        ], "danger-mouse-bk"),
    ]
)

# 17. Cage the Elephant
mk_artist(
    "cage-the-elephant", "Cage the Elephant", "Rock", "Group",
    ["rock", "indie rock", "alternative rock"],
    2006,
    [
        ("matt-shultz", "Matt Shultz", "Vocals", ["Vocalist"]),
        ("brad-shultz", "Brad Shultz", "Guitar", ["Guitarist", "Songwriter"]),
        ("nick-bockrath", "Nick Bockrath", "Guitar", ["Guitarist"]),
        ("daniel-tichenor", "Daniel Tichenor", "Bass", ["Bassist"]),
    ],
    [("jay-joyce", "Jay Joyce", ["Producer"])],
    [
        ("cage-self-cte", "Cage the Elephant", 2008, [
            ("ain-t-no-rest-for-the-wicked-cte", "Ain't No Rest for the Wicked"),
            ("in-one-ear-cte", "In One Ear"),
            ("free-love-cte", "Free Love"),
            ("back-against-the-wall-cte", "Back Against the Wall"),
            ("shake-me-down-cte", "Shake Me Down"),
            ("sabertooth-tiger-cte", "Sabertooth Tiger"),
            ("james-brown-cte", "James Brown"),
            ("always-something-cte", "Always Something"),
        ], "jay-joyce"),
        ("thank-you-happy-birthday-cte", "Thank You, Happy Birthday", 2011, [
            ("shake-me-down-2-cte", "Shake Me Down (Reprise)"),
            ("around-my-head-cte", "Around My Head"),
            ("always-something-reprise-cte", "Always Something Reprise"),
            ("shake-me-down-reprise-cte", "Shake Me Down (LP)"),
            ("Aberdeen-cte", "Aberdeen"),
            ("rubber-ball-cte", "Rubber Ball (Glue)"),
            ("right-before-my-eyes-cte", "Right Before My Eyes"),
            ("flow-cte", "Flow"),
        ], "jay-joyce"),
        ("melophobia-cte", "Melophobia", 2013, [
            ("come-a-little-closer-cte", "Come a Little Closer"),
            ("it-s-just-forever-cte", "It's Just Forever"),
            ("halo-cte", "Halo"),
            ("cigarette-daydreams-cte", "Cigarette Daydreams"),
            ("take-it-or-leave-it-cte", "Take It or Leave It"),
            ("teeth-cte", "Teeth"),
            ("hypocrite-cte", "Hypocrite"),
            ("telescope-cte", "Telescope"),
        ], "jay-joyce"),
        ("tell-me-cte", "Tell Me I'm Pretty", 2015, [
            ("mess-around-cte", "Mess Around"),
            ("sweetie-little-jean-cte", "Sweetie Little Jean"),
            ("too-late-to-say-goodbye-cte", "Too Late to Say Goodbye"),
            ("how-are-you-true-cte", "How Are You True"),
            ("shake-it-loose-cte", "Shake It Loose"),
            ("if-only-cte", "If Only"),
            ("trouble-cte", "Trouble"),
            ("portuguese-knife-fight-cte", "Portuguese Knife Fight"),
        ], "jay-joyce"),
        ("social-cues-cte", "Social Cues", 2019, [
            ("night-running-cte", "Night Running"),
            ("black-madonna-cte", "Black Madonna"),
            ("tokyo-smoke-cte", "Tokyo Smoke"),
            ("mess-around-reprise-cte", "Ready to Let Go"),
            ("love-s-the-only-way-cte", "Love's the Only Way"),
            ("house-of-glass-cte", "House of Glass"),
            ("dance-dance-cte", "Dance Dance"),
            ("goodbye-cte", "Goodbye"),
        ], "jay-joyce"),
    ]
)

# 18. Tame Impala
mk_artist(
    "tame-impala", "Tame Impala", "Indie Rock", "Group",
    ["indie rock", "psychedelic rock", "dream pop"],
    2007,
    [
        ("kevin-parker-ti", "Kevin Parker", "Vocals, Guitar, Keys, Drums", ["Vocalist", "Multi-instrumentalist", "Producer", "Songwriter"]),
    ],
    [],
    [
        ("innerspeaker-ti", "Innerspeaker", 2010, [
            ("it-is-not-meant-to-be-ti", "It Is Not Meant to Be"),
            ("desire-be-desire-go-ti", "Desire Be, Desire Go"),
            ("alter-ego-ti", "Alter Ego"),
            ("lucidity-ti", "Lucidity"),
            ("why-wont-they-talk-to-me-ti", "Why Won't They Talk to Me?"),
            ("solitude-is-bliss-ti", "Solitude Is Bliss"),
            ("jeremy-s-storm-ti", "Jeremy's Storm"),
            ("runway-houses-city-clouds-ti", "Runway, Houses, City, Clouds"),
        ], "kevin-parker-ti"),
        ("lonerism-ti", "Lonerism", 2012, [
            ("be-above-it-ti", "Be Above It"),
            ("endors-toi-ti", "Endors Toi"),
            ("apocalypse-dreams-ti", "Apocalypse Dreams"),
            ("mind-mischief-ti", "Mind Mischief"),
            ("music-to-walk-home-by-ti", "Music to Walk Home By"),
            ("why-wont-you-make-up-your-mind-ti", "Why Won't You Make Up Your Mind?"),
            ("feels-like-we-only-go-backwards-ti", "Feels Like We Only Go Backwards"),
            ("keep-on-lying-ti", "Keep on Lying"),
        ], "kevin-parker-ti"),
        ("currents-ti", "Currents", 2015, [
            ("let-it-happen-ti", "Let It Happen"),
            ("nangs-ti", "Nangs"),
            ("the-moment-ti", "The Moment"),
            ("yes-i-m-changing-ti", "Yes I'm Changing"),
            ("eventually-ti", "Eventually"),
            ("past-life-ti", "Past Life"),
            ("disciples-ti", "Disciples"),
            ("cause-i-m-a-man-ti", "Cause I'm a Man"),
            ("reality-in-motion-ti", "Reality in Motion"),
            ("love-slash-paranoia-ti", "Love/Paranoia"),
        ], "kevin-parker-ti"),
        ("slow-rush-ti", "The Slow Rush", 2020, [
            ("one-more-year-ti", "One More Year"),
            ("instant-destiny-ti", "Instant Destiny"),
            ("borderline-ti", "Borderline"),
            ("tomorrow-s-dust-ti", "Tomorrow's Dust"),
            ("on-track-ti", "On Track"),
            ("lost-in-yesterday-ti", "Lost in Yesterday"),
            ("is-it-true-ti", "Is It True"),
            ("it-might-be-time-ti", "It Might Be Time"),
            ("glimmer-ti", "Glimmer"),
        ], "kevin-parker-ti"),
    ]
)

# 19. Greta Van Fleet
mk_artist(
    "greta-van-fleet", "Greta Van Fleet", "Rock", "Group",
    ["rock", "hard rock", "blues rock"],
    2012,
    [
        ("josh-kiszka", "Josh Kiszka", "Vocals", ["Vocalist"]),
        ("jake-kiszka", "Jake Kiszka", "Guitar", ["Guitarist"]),
        ("sam-kiszka", "Sam Kiszka", "Bass, Keys", ["Bassist"]),
        ("danny-wagner", "Danny Wagner", "Drums", ["Drummer"]),
    ],
    [("greg-kurstin", "Greg Kurstin", ["Producer"])],
    [
        ("anthem-of-peaceful-army-gvf", "Anthem of the Peaceful Army", 2018, [
            ("safari-song-gvf", "Safari Song"),
            ("highway-tune-gvf", "Highway Tune"),
            ("a-new-day-yesterday-gvf", "A New Day Yesterday"),
            ("black-smoke-rising-gvf", "Black Smoke Rising"),
            ("you-re-the-one-gvf", "You're the One"),
            ("with-my-mother-gvf", "With My Mother"),
            ("lover-leaver-gvf", "Lover, Leaver (Taker, Believer)"),
            ("watching-over-gvf", "Watching Over"),
        ], "greg-kurstin"),
        ("battle-at-gardens-gate-gvf", "The Battle at Garden's Gate", 2021, [
            ("heat-above-gvf", "Heat Above"),
            ("my-way-soon-gvf", "My Way, Soon"),
            ("broken-bells-gvf", "Broken Bells"),
            ("age-of-machine-gvf", "Age of Machine"),
            ("tears-of-rain-gvf", "Tears of Rain"),
            ("treat-me-right-gvf", "Treat Me Right"),
            ("light-my-love-gvf", "Light My Love"),
            ("the-weight-of-dreams-gvf", "The Weight of Dreams"),
        ], "greg-kurstin"),
        ("starcatcher-gvf", "Starcatcher", 2023, [
            ("dancing-in-the-room-gvf", "Dancing in the Room"),
            ("meeting-the-master-gvf", "Meeting the Master"),
            ("the-falling-silver-sky-gvf", "The Falling Silver Sky"),
            ("sacred-the-thread-gvf", "Sacred the Thread"),
            ("the-new-day-gvf", "The New Day"),
            ("fate-of-the-faithful-gvf", "Fate of the Faithful"),
            ("somethin-for-thirst-gvf", "Somethin' for Thirst"),
            ("farewell-for-now-gvf", "Farewell for Now"),
        ], "greg-kurstin"),
    ]
)

# 20. Royal Blood
mk_artist(
    "royal-blood", "Royal Blood", "Rock", "Group",
    ["rock", "hard rock", "blues rock"],
    2011,
    [
        ("mike-kerr", "Mike Kerr", "Vocals, Bass", ["Vocalist", "Bassist", "Songwriter"]),
        ("ben-thatcher", "Ben Thatcher", "Drums", ["Drummer"]),
    ],
    [("tom-dalgety", "Tom Dalgety", ["Producer"])],
    [
        ("royal-blood-self-rb", "Royal Blood", 2014, [
            ("out-of-the-black-rb", "Out of the Black"),
            ("come-on-over-rb", "Come On Over"),
            ("figure-it-out-rb", "Figure It Out"),
            ("ten-tonne-skeleton-rb", "Ten Tonne Skeleton"),
            ("blood-hands-rb", "Blood Hands"),
            ("little-monster-rb", "Little Monster"),
            ("loose-change-rb", "Loose Change"),
            ("hole-rb", "Hole"),
        ], "tom-dalgety"),
        ("how-did-we-get-so-dark-rb", "How Did We Get So Dark?", 2017, [
            ("how-did-we-get-so-dark-rb-song", "How Did We Get So Dark?"),
            ("lights-out-rb", "Lights Out"),
            ("hook-line-and-sinker-rb", "Hook, Line & Sinker"),
            ("look-like-you-know-rb", "Look Like You Know"),
            ("where-are-you-now-rb", "Where Are You Now?"),
            ("don-t-tell-rb", "Don't Tell"),
            ("sleep-rb", "Sleep"),
            ("i-only-lie-rb", "I Only Lie"),
        ], "tom-dalgety"),
        ("typhoons-rb", "Typhoons", 2021, [
            ("trouble-s-coming-rb", "Trouble's Coming"),
            ("typhoons-rb-song", "Typhoons"),
            ("who-needs-friends-rb", "Who Needs Friends"),
            ("mountains-at-midnight-rb", "Mountains at Midnight"),
            ("either-you-want-it-rb", "Either You Want It"),
            ("mad-visions-rb", "Mad Visions"),
            ("limbo-rb", "Limbo"),
            ("boilermaker-rb", "Boilermaker"),
        ], "tom-dalgety"),
        ("back-to-the-water-rb", "Back to the Water Below", 2023, [
            ("pull-me-through-rb", "Pull Me Through"),
            ("shiner-in-the-dark-rb", "Shiner in the Dark"),
            ("chosen-one-rb", "Chosen One"),
            ("mountains-at-midnight-2-rb", "Mountains at Midnight II"),
            ("waves-rb", "Waves"),
            ("either-you-want-it-2-rb", "Either You Want It (Live)"),
            ("the-warmth-rb", "The Warmth"),
            ("high-waters-rb", "High Waters"),
        ], "tom-dalgety"),
    ]
)

# 21. Vampire Weekend
mk_artist(
    "vampire-weekend", "Vampire Weekend", "Indie Rock", "Group",
    ["indie rock", "indie pop", "art rock"],
    2006,
    [
        ("ezra-koenig", "Ezra Koenig", "Vocals, Guitar", ["Vocalist", "Guitarist", "Songwriter"]),
        ("chris-baio", "Chris Baio", "Bass", ["Bassist"]),
        ("chris-tomson", "Chris Tomson", "Drums", ["Drummer"]),
    ],
    [("rostam-batmanglij", "Rostam Batmanglij", ["Producer", "Multi-instrumentalist"])],
    [
        ("vampire-weekend-self-vw", "Vampire Weekend", 2008, [
            ("mansard-roof-vw", "Mansard Roof"),
            ("oxford-comma-vw", "Oxford Comma"),
            ("a-punk-vw", "A-Punk"),
            ("cape-cod-kwassa-kwassa-vw", "Cape Cod Kwassa Kwassa"),
            ("m79-vw", "M79"),
            ("campus-vw", "Campus"),
            ("bryn-vw", "Bryn"),
            ("one-blake-s-got-a-new-face-vw", "One (Blake's Got a New Face)"),
        ], "rostam-batmanglij"),
        ("contra-vw", "Contra", 2010, [
            ("horchata-vw", "Horchata"),
            ("white-sky-vw", "White Sky"),
            ("holiday-vw", "Holiday"),
            ("cousins-vw", "Cousins"),
            ("giving-up-the-gun-vw", "Giving Up the Gun"),
            ("diplomat-s-son-vw", "Diplomat's Son"),
            ("i-think-ur-a-contra-vw", "I Think Ur a Contra"),
            ("run-vw", "Run"),
        ], "rostam-batmanglij"),
        ("modern-vampires-vw", "Modern Vampires of the City", 2013, [
            ("obvious-bicycle-vw", "Obvious Bicycle"),
            ("unbelievers-vw", "Unbelievers"),
            ("step-vw", "Step"),
            ("diane-young-vw", "Diane Young"),
            ("don-t-lie-vw", "Don't Lie"),
            ("ya-hey-vw", "Ya Hey"),
            ("everlasting-arms-vw", "Everlasting Arms"),
            ("worship-you-vw", "Worship You"),
            ("hannah-hunt-vw", "Hannah Hunt"),
        ], "rostam-batmanglij"),
        ("father-of-bride-vw", "Father of the Bride", 2019, [
            ("harmony-hall-vw", "Harmony Hall"),
            ("bambina-vw", "Bambina"),
            ("this-life-vw", "This Life"),
            ("unbearably-white-vw", "Unbearably White"),
            ("rich-man-vw", "Rich Man"),
            ("sympathy-vw", "Sympathy"),
            ("how-long-vw", "How Long?"),
            ("big-blue-vw", "Big Blue"),
        ], "rostam-batmanglij"),
    ]
)

# 22. HAIM
mk_artist(
    "haim", "HAIM", "Indie Pop", "Group",
    ["indie pop", "pop rock", "soft rock"],
    2006,
    [
        ("este-haim", "Este Haim", "Bass, Vocals", ["Bassist", "Vocalist"]),
        ("danielle-haim", "Danielle Haim", "Guitar, Drums, Vocals", ["Guitarist", "Vocalist", "Songwriter"]),
        ("alana-haim", "Alana Haim", "Guitar, Keys, Vocals", ["Guitarist", "Vocalist"]),
    ],
    [("ariel-rechtshaid", "Ariel Rechtshaid", ["Producer"])],
    [
        ("days-are-gone-hm", "Days Are Gone", 2013, [
            ("falling-hm", "Falling"),
            ("the-wire-hm", "The Wire"),
            ("if-i-could-change-your-mind-hm", "If I Could Change Your Mind"),
            ("days-are-gone-hm-song", "Days Are Gone"),
            ("don-t-save-me-hm", "Don't Save Me"),
            ("my-song-5-hm", "My Song 5"),
            ("running-if-you-call-my-name-hm", "Running If You Call My Name"),
            ("let-me-go-hm", "Let Me Go"),
        ], "ariel-rechtshaid"),
        ("something-to-tell-you-hm", "Something to Tell You", 2017, [
            ("want-you-back-hm", "Want You Back"),
            ("nothing-s-wrong-hm", "Nothing's Wrong"),
            ("little-of-your-love-hm", "Little of Your Love"),
            ("ready-for-you-hm", "Ready for You"),
            ("right-now-hm", "Right Now"),
            ("found-it-in-silence-hm", "Found It in Silence"),
            ("kept-me-crying-hm", "Kept Me Crying"),
            ("walking-away-hm", "Walking Away"),
        ], "ariel-rechtshaid"),
        ("women-in-music-hm", "Women in Music Pt. III", 2020, [
            ("los-angeles-hm", "Los Angeles"),
            ("the-steps-hm", "The Steps"),
            ("all-that-ever-mattered-hm", "All That Ever Mattered"),
            ("gasoline-hm", "Gasoline"),
            ("3am-hm", "3AM"),
            ("i-know-alone-hm", "I Know Alone"),
            ("up-from-a-flame-hm", "Up from a Flame"),
            ("summer-girl-hm", "Summer Girl"),
        ], "ariel-rechtshaid"),
    ]
)

# 23. LCD Soundsystem
mk_artist(
    "lcd-soundsystem", "LCD Soundsystem", "Indie Rock", "Group",
    ["indie rock", "dance punk", "electronic rock"],
    2002,
    [
        ("james-murphy", "James Murphy", "Vocals, Multi-instrumentalist", ["Vocalist", "Multi-instrumentalist", "Songwriter", "Producer"]),
    ],
    [],
    [
        ("lcd-self-lcd", "LCD Soundsystem", 2005, [
            ("daft-punk-is-playing-at-my-house-lcd", "Daft Punk Is Playing at My House"),
            ("tribulations-lcd", "Tribulations"),
            ("disco-infiltrator-lcd", "Disco Infiltrator"),
            ("movement-lcd", "Movement"),
            ("too-much-love-lcd", "Too Much Love"),
            ("on-repeat-lcd", "On Repeat"),
            ("thrills-lcd", "Thrills"),
            ("great-release-lcd", "Great Release"),
        ], "james-murphy"),
        ("sound-of-silver-lcd", "Sound of Silver", 2007, [
            ("get-innocuous-lcd", "Get Innocuous!"),
            ("time-to-get-away-lcd", "Time to Get Away"),
            ("north-american-scum-lcd", "North American Scum"),
            ("someone-great-lcd", "Someone Great"),
            ("all-my-friends-lcd", "All My Friends"),
            ("us-v-them-lcd", "Us v Them"),
            ("watch-the-tapes-lcd", "Watch the Tapes"),
            ("sound-of-silver-lcd-song", "Sound of Silver"),
        ], "james-murphy"),
        ("american-dream-lcd", "American Dream", 2017, [
            ("oh-baby-lcd", "Oh Baby"),
            ("other-voices-lcd", "Other Voices"),
            ("i-used-to-lcd", "I Used to"),
            ("change-yr-mind-lcd", "Change Yr Mind"),
            ("how-do-you-sleep-lcd", "How Do You Sleep?"),
            ("tonite-lcd", "Tonite"),
            ("call-the-police-lcd", "Call the Police"),
            ("american-dream-lcd-song", "American Dream"),
        ], "james-murphy"),
        ("new-album-lcd", "American Dream (Deluxe)", 2018, [
            ("pulse-v-1-lcd", "pulse (v. 1)"),
            ("emotional-haircut-lcd", "Emotional Haircut"),
            ("i-can-change-lcd", "I Can Change"),
            ("new-york-i-love-you-lcd", "New York, I Love You but You're Bringing Me Down"),
            ("yr-city-s-a-sucker-lcd", "Yr City's a Sucker"),
            ("losing-my-edge-lcd", "Losing My Edge"),
            ("yeah-lcd", "Yeah (Crass Version)"),
            ("dance-yrself-clean-lcd", "Dance Yrself Clean"),
        ], "james-murphy"),
    ]
)

# 24. Big Thief
mk_artist(
    "big-thief", "Big Thief", "Folk", "Group",
    ["folk", "indie folk", "indie rock"],
    2015,
    [
        ("adrianne-lenker", "Adrianne Lenker", "Vocals, Guitar", ["Vocalist", "Guitarist", "Songwriter"]),
        ("buck-meek", "Buck Meek", "Guitar", ["Guitarist"]),
        ("max-oleary", "Max Oleary", "Bass", ["Bassist"]),
        ("james-krivchenia", "James Krivchenia", "Drums", ["Drummer"]),
    ],
    [("andrew-sarlo", "Andrew Sarlo", ["Producer"])],
    [
        ("masterpiece-bt", "Masterpiece", 2016, [
            ("masterpiece-bt-song", "Masterpiece"),
            ("real-love-bt", "Real Love"),
            ("paul-bt", "Paul"),
            ("hope-bt", "Hope"),
            ("black-diamonds-bt", "Black Diamonds"),
            ("Interstate-bt", "Interstate"),
            ("mary-bt", "Mary"),
            ("pretty-things-bt", "Pretty Things"),
        ], "andrew-sarlo"),
        ("capacity-bt", "Capacity", 2017, [
            ("mythological-beauty-bt", "Mythological Beauty"),
            ("shark-smile-bt", "Shark Smile"),
            ("capacity-bt-song", "Capacity"),
            ("objects-bt", "Objects"),
            ("coma-bt", "Coma"),
            ("pretty-things-reprise-bt", "Pretty Things (Reprise)"),
            ("parallels-bt", "Parallels"),
            ("watering-bt", "Watering"),
        ], "andrew-sarlo"),
        ("ufof-bt", "U.F.O.F.", 2019, [
            ("contact-bt", "Contact"),
            ("ufof-bt-song", "UFOF"),
            ("cattails-bt", "Cattails"),
            ("orange-bt", "Orange"),
            ("from-bt", "From"),
            ("betsy-bt", "Betsy"),
            ("century-bt", "Century"),
            ("the-canyon-bt", "The Canyon"),
        ], "andrew-sarlo"),
        ("two-hands-bt", "Two Hands", 2019, [
            ("not-bt", "Not"),
            ("the-ones-who-love-you-bt", "The Ones Who Love You"),
            ("two-hands-bt-song", "Two Hands"),
            ("rockland-bt", "Rockland"),
            ("forgotten-eyes-bt", "Forgotten Eyes"),
            ("shoulders-bt", "Shoulders"),
            ("wolf-bt", "Wolf"),
            ("replaced-bt", "Replaced"),
        ], "andrew-sarlo"),
        ("dragon-new-warm-bt", "Dragon New Warm Mountain I Believe in You", 2022, [
            ("simulation-swarm-bt", "Simulation Swarm"),
            ("time-escaping-bt", "Time Escaping"),
            ("little-things-bt", "Little Things"),
            ("heavy-dream-bt", "Heavy Dream"),
            ("flower-of-blood-bt", "Flower of Blood"),
            ("spud-infinity-bt", "Spud Infinity"),
            ("dried-roses-bt", "Dried Roses"),
            ("promise-is-a-pendulum-bt", "Promise Is a Pendulum"),
        ], "andrew-sarlo"),
    ]
)

# 25. Hozier
mk_artist(
    "hozier", "Hozier", "Folk", "Solo",
    ["folk", "indie folk", "blues rock"],
    2012,
    [
        ("andrew-hozier-byrne", "Andrew Hozier-Byrne", "Vocals, Guitar", ["Vocalist", "Guitarist", "Songwriter"]),
    ],
    [("rob-kirwan", "Rob Kirwan", ["Producer"])],
    [
        ("hozier-self-hz", "Hozier", 2014, [
            ("take-me-to-church-hz", "Take Me to Church"),
            ("angel-of-small-death-hz", "Angel of Small Death & the Codeine Scene"),
            ("like-real-people-do-hz", "Like Real People Do"),
            ("work-song-hz", "Work Song"),
            ("someone-new-hz", "Someone New"),
            ("sedated-hz", "Sedated"),
            ("from-eden-hz", "From Eden"),
            ("in-the-woods-somewhere-hz", "In the Woods Somewhere"),
            ("cherry-wine-hz", "Cherry Wine"),
        ], "rob-kirwan"),
        ("wasteland-baby-hz", "Wasteland, Baby!", 2019, [
            ("nina-cried-power-hz", "Nina Cried Power"),
            ("shrike-hz", "Shrike"),
            ("talk-hz", "Talk"),
            ("movement-hz", "Movement"),
            ("no-plan-hz", "No Plan"),
            ("nobody-hz", "Nobody"),
            ("to-be-alone-hz", "To Be Alone"),
            ("as-it-was-hz", "As It Was"),
        ], "rob-kirwan"),
        ("unreal-unearth-hz", "Unreal Unearth", 2023, [
            ("de-selby-part-1-hz", "De Selby (Part 1)"),
            ("de-selby-part-2-hz", "De Selby (Part 2)"),
            ("first-light-hz", "First Light"),
            ("i-have-a-love-hz", "I Have a Love"),
            ("all-things-end-hz", "All Things End"),
            ("through-me-the-flood-hz", "Through Me (The Flood)"),
            ("anything-but-hz", "Anything But"),
            ("who-we-are-hz", "Who We Are"),
            ("abstract-psychopomp-hz", "Abstract (Psychopomp)"),
        ], "rob-kirwan"),
    ]
)

# 26. CHVRCHES
mk_artist(
    "chvrches", "CHVRCHES", "Indie Pop", "Group",
    ["indie pop", "synth-pop", "electronic rock"],
    2011,
    [
        ("lauren-mayberry", "Lauren Mayberry", "Vocals", ["Vocalist", "Songwriter"]),
        ("iain-cook", "Iain Cook", "Keys, Guitar, Bass", ["Multi-instrumentalist"]),
        ("martin-doherty", "Martin Doherty", "Keys, Vocals", ["Multi-instrumentalist", "Vocalist"]),
    ],
    [("greg-kurstin", "Greg Kurstin", ["Producer"])],
    [
        ("bones-of-what-you-believe-ch", "The Bones of What You Believe", 2013, [
            ("the-mother-we-share-ch", "The Mother We Share"),
            ("lies-ch", "Lies"),
            ("gun-ch", "Gun"),
            ("recover-ch", "Recover"),
            ("tether-ch", "Tether"),
            ("now-is-not-the-time-ch", "Now Is Not the Time"),
            ("by-the-mouth-ch", "By the Mouth"),
            ("night-sky-ch", "Night Sky"),
            ("strong-hand-ch", "Strong Hand"),
        ], "greg-kurstin"),
        ("every-open-eye-ch", "Every Open Eye", 2015, [
            ("never-ending-circles-ch", "Never Ending Circles"),
            ("leave-a-trace-ch", "Leave a Trace"),
            ("make-them-gold-ch", "Make Them Gold"),
            ("keep-you-on-my-side-ch", "Keep You on My Side"),
            ("clearest-blue-ch", "Clearest Blue"),
            ("high-enough-to-carry-you-over-ch", "High Enough to Carry You Over"),
            ("down-side-of-me-ch", "Down Side of Me"),
            ("empty-threat-ch", "Empty Threat"),
        ], "greg-kurstin"),
        ("love-is-dead-ch", "Love Is Dead", 2018, [
            ("graffiti-ch", "Graffiti"),
            ("get-out-ch", "Get Out"),
            ("miracle-ch", "Miracle"),
            ("deliverance-ch", "Deliverance"),
            ("ii-ch", "II"),
            ("god-s-plan-ch", "God's Plan"),
            ("really-gone-ch", "Really Gone"),
            ("ici-ch", "Ici"),
        ], "greg-kurstin"),
        ("screen-violence-ch", "Screen Violence", 2021, [
            ("how-not-to-drown-ch", "How Not to Drown"),
            ("he-said-she-said-ch", "He Said She Said"),
            ("good-girls-ch", "Good Girls"),
            ("by-your-side-ch", "By Your Side"),
            ("lullabies-ch", "Lullabies"),
            ("violent-delights-ch", "Violent Delights"),
            ("nightmares-ch", "Nightmares"),
            ("final-girl-ch", "Final Girl"),
        ], "greg-kurstin"),
    ]
)

# Write all person files
print("\n=== Writing Person Files ===")
for slug, data in persons.items():
    person_path = PEOPLE_DIR / f"{slug}.md"
    if person_path.exists():
        print(f"  skip (exists): {slug}")
        continue

    roles_str = yml_list_str(data["roles"])
    bands_yaml = ""
    for b in data["bands"]:
        bands_yaml += f"  - slug: {ys(b['slug'])}\n    name: {ys(b['name'])}\n    role: {ys(b['role'])}\n"

    sc_yaml = ""
    for sc in data["song_credits"]:
        sc_yaml += f"  - slug: {ys(sc['slug'])}\n    title: {ys(sc['title'])}\n    credit: {ys(sc['credit'])}\n"

    if bands_yaml and sc_yaml:
        person_content = f"""---
title: {ys(data['title'])}
slug: {ys(slug)}
roles: {roles_str}
bands:
{bands_yaml}song_credits:
{sc_yaml}draft: false
---
"""
    elif bands_yaml:
        person_content = f"""---
title: {ys(data['title'])}
slug: {ys(slug)}
roles: {roles_str}
bands:
{bands_yaml}draft: false
---
"""
    elif sc_yaml:
        person_content = f"""---
title: {ys(data['title'])}
slug: {ys(slug)}
roles: {roles_str}
song_credits:
{sc_yaml}draft: false
---
"""
    else:
        person_content = f"""---
title: {ys(data['title'])}
slug: {ys(slug)}
roles: {roles_str}
draft: false
---
"""
    person_path.write_text(person_content, encoding="utf-8")
    print(f"  person: {slug}")

print("\n=== Done! ===")
# Count files created
artist_count = len(list(ARTISTS_DIR.glob("*.md")))
album_count = len(list(ALBUMS_DIR.glob("*.md")))
song_count = len(list(SONGS_DIR.glob("*.md")))
people_count = len(list(PEOPLE_DIR.glob("*.md")))
print(f"Artists: {artist_count}, Albums: {album_count}, Songs: {song_count}, People: {people_count}")
