#!/usr/bin/env python3
"""
Create 80s Rock/Metal content files for the MusicTree Hugo site.
All files written with Path.write_text(encoding='utf-8') — no BOM.
Existing files are skipped.
"""

from pathlib import Path
from collections import defaultdict

BASE = Path(r"c:\repo\MusicTree")
CONTENT = BASE / "content"

created_count = 0
skipped_count = 0


def q(s):
    """Quote a YAML scalar value when special characters are present."""
    s = str(s)
    if not s:
        return '""'
    special = set(":'\"#{}[]&*?!@`\\>,")
    needs = (
        any(c in s for c in special)
        or (len(s) > 0 and s[0] in "-+.")
        or (len(s) > 0 and s[0].isdigit())
        or s.lower() in ("true", "false", "null", "yes", "no", "on", "off")
        or s != s.strip()
    )
    if needs:
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return s


def wf(path, content):
    """Write file only if it does not already exist."""
    global created_count, skipped_count
    if path.exists():
        skipped_count += 1
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    created_count += 1
    return True


# person_slug -> [(song_slug, song_title, role), ...]
PERSON_CREDITS = defaultdict(list)

# ============================================================
# ARTIST DATA
# ============================================================
ARTIST_DATA = [
    # ==================== 1. VAN HALEN ====================
    {
        "slug": "van-halen", "title": "Van Halen", "band_type": "Group",
        "genres": ["Hard Rock"], "scene": "Los Angeles", "formed": 1972,
        "members": [
            ("david-lee-roth", "Vocals"), ("eddie-van-halen", "Guitar"),
            ("alex-van-halen", "Drums"), ("michael-anthony", "Bass"),
        ],
        "albums": [
            {"slug": "van-halen-1978", "title": "Van Halen", "year": 1978,
             "producer": "ted-templeman", "writers": ["eddie-van-halen", "david-lee-roth"],
             "songs": [
                 ("runnin-with-the-devil-vh", "Runnin' with the Devil"),
                 ("eruption-vh", "Eruption"),
                 ("you-really-got-me-vh", "You Really Got Me"),
                 ("aint-talkin-bout-love-vh", "Ain't Talkin' 'Bout Love"),
                 ("jamie-s-cryin-vh", "Jamie's Cryin'"),
             ]},
            {"slug": "van-halen-ii", "title": "Van Halen II", "year": 1979,
             "producer": "ted-templeman", "writers": ["eddie-van-halen", "david-lee-roth"],
             "songs": [
                 ("dance-the-night-away-vh", "Dance the Night Away"),
                 ("beautiful-girls-vh", "Beautiful Girls"),
                 ("somebody-get-me-a-doctor-vh", "Somebody Get Me a Doctor"),
                 ("you-re-no-good-vh", "You're No Good"),
             ]},
            {"slug": "women-and-children-first", "title": "Women and Children First", "year": 1980,
             "producer": "ted-templeman", "writers": ["eddie-van-halen", "david-lee-roth"],
             "songs": [
                 ("and-the-cradle-will-rock-vh", "And the Cradle Will Rock"),
                 ("could-this-be-magic-vh", "Could This Be Magic?"),
                 ("everybody-wants-some-vh", "Everybody Wants Some!!"),
             ]},
            {"slug": "fair-warning-vh", "title": "Fair Warning", "year": 1981,
             "producer": "ted-templeman", "writers": ["eddie-van-halen", "david-lee-roth"],
             "songs": [
                 ("unchained-vh", "Unchained"),
                 ("mean-streets-vh", "Mean Streets"),
                 ("dirty-movies-vh", "Dirty Movies"),
             ]},
            {"slug": "vh-1984", "title": "1984", "year": 1984,
             "producer": "ted-templeman", "writers": ["eddie-van-halen", "david-lee-roth"],
             "songs": [
                 ("jump-vh", "Jump"),
                 ("panama-vh", "Panama"),
                 ("hot-for-teacher-vh", "Hot for Teacher"),
                 ("i-ll-wait-vh", "I'll Wait"),
             ]},
            {"slug": "5150-vh", "title": "5150", "year": 1986,
             "producer": "mick-jones-producer", "writers": ["eddie-van-halen"],
             "songs": [
                 ("why-cant-this-be-love-vh", "Why Can't This Be Love"),
                 ("dreams-vh", "Dreams"),
                 ("love-walks-in-vh", "Love Walks In"),
             ]},
            {"slug": "ou812-vh", "title": "OU812", "year": 1988,
             "producer": "ted-templeman", "writers": ["eddie-van-halen"],
             "songs": [
                 ("finish-what-ya-started-vh", "Finish What Ya Started"),
                 ("when-its-love-vh", "When It's Love"),
             ]},
        ],
    },

    # ==================== 2. GUNS N' ROSES ====================
    {
        "slug": "guns-n-roses", "title": "Guns N' Roses", "band_type": "Group",
        "genres": ["Hard Rock"], "scene": "Los Angeles", "formed": 1985,
        "members": [
            ("axl-rose", "Vocals"), ("slash", "Guitar"), ("duff-mckagan", "Bass"),
            ("izzy-stradlin", "Guitar"), ("steven-adler", "Drums"), ("dizzy-reed", "Keyboards"),
        ],
        "albums": [
            {"slug": "appetite-for-destruction", "title": "Appetite for Destruction", "year": 1987,
             "producer": "mike-clink", "writers": ["axl-rose", "slash", "izzy-stradlin"],
             "songs": [
                 ("welcome-to-the-jungle-gnr", "Welcome to the Jungle"),
                 ("sweet-child-o-mine-gnr", "Sweet Child O' Mine"),
                 ("paradise-city-gnr", "Paradise City"),
                 ("nightrain-gnr", "Nightrain"),
                 ("mr-brownstone-gnr", "Mr. Brownstone"),
                 ("patience-gnr", "Patience"),
             ]},
            {"slug": "gnr-lies", "title": "GN'R Lies", "year": 1988,
             "producer": "mike-clink", "writers": ["axl-rose", "slash", "izzy-stradlin"],
             "songs": [
                 ("used-to-love-her-gnr", "Used to Love Her"),
                 ("one-in-a-million-gnr", "One in a Million"),
             ]},
            {"slug": "use-your-illusion-i", "title": "Use Your Illusion I", "year": 1991,
             "producer": "mike-clink", "writers": ["axl-rose", "slash"],
             "songs": [
                 ("november-rain-gnr", "November Rain"),
                 ("civil-war-gnr", "Civil War"),
                 ("estranged-gnr", "Estranged"),
             ]},
            {"slug": "use-your-illusion-ii", "title": "Use Your Illusion II", "year": 1991,
             "producer": "mike-clink", "writers": ["axl-rose", "slash"],
             "songs": [
                 ("live-and-let-die-gnr", "Live and Let Die"),
                 ("you-could-be-mine-gnr", "You Could Be Mine"),
                 ("knockin-on-heavens-door-gnr", "Knockin' on Heaven's Door"),
             ]},
        ],
    },

    # ==================== 3. METALLICA ====================
    {
        "slug": "metallica", "title": "Metallica", "band_type": "Group",
        "genres": ["Heavy Metal"], "scene": "San Francisco", "formed": 1981,
        "members": [
            ("james-hetfield", "Vocals/Guitar"), ("lars-ulrich", "Drums"),
            ("kirk-hammett", "Guitar"), ("robert-trujillo", "Bass"),
        ],
        "albums": [
            {"slug": "kill-em-all", "title": "Kill 'Em All", "year": 1983,
             "producer": "paul-curcio", "writers": ["james-hetfield", "lars-ulrich"],
             "songs": [
                 ("seek-and-destroy-met", "Seek & Destroy"),
                 ("hit-the-lights-met", "Hit the Lights"),
                 ("the-four-horsemen-met", "The Four Horsemen"),
             ]},
            {"slug": "ride-the-lightning", "title": "Ride the Lightning", "year": 1984,
             "producer": "flemming-rasmussen", "writers": ["james-hetfield", "lars-ulrich"],
             "songs": [
                 ("fade-to-black-met", "Fade to Black"),
                 ("for-whom-the-bell-tolls-met", "For Whom the Bell Tolls"),
                 ("creeping-death-met", "Creeping Death"),
             ]},
            {"slug": "master-of-puppets-met", "title": "Master of Puppets", "year": 1986,
             "producer": "flemming-rasmussen", "writers": ["james-hetfield", "lars-ulrich"],
             "songs": [
                 ("master-of-puppets-met", "Master of Puppets"),
                 ("battery-met", "Battery"),
                 ("orion-met", "Orion"),
             ]},
            {"slug": "and-justice-for-all", "title": "...And Justice for All", "year": 1988,
             "producer": "flemming-rasmussen", "writers": ["james-hetfield", "lars-ulrich"],
             "songs": [
                 ("one-met", "One"),
                 ("blackened-met", "Blackened"),
                 ("harvester-of-sorrow-met", "Harvester of Sorrow"),
             ]},
            {"slug": "metallica-black-album", "title": "Metallica", "year": 1991,
             "producer": "bob-rock-producer", "writers": ["james-hetfield", "lars-ulrich"],
             "songs": [
                 ("enter-sandman-met", "Enter Sandman"),
                 ("the-unforgiven-met", "The Unforgiven"),
                 ("nothing-else-matters-met", "Nothing Else Matters"),
                 ("wherever-i-may-roam-met", "Wherever I May Roam"),
                 ("sad-but-true-met", "Sad but True"),
             ]},
            {"slug": "load-met", "title": "Load", "year": 1996,
             "producer": "bob-rock-producer", "writers": ["james-hetfield", "lars-ulrich"],
             "songs": [
                 ("until-it-sleeps-met", "Until It Sleeps"),
                 ("hero-of-the-day-met", "Hero of the Day"),
                 ("king-nothing-met", "King Nothing"),
             ]},
            {"slug": "reload-met", "title": "Reload", "year": 1997,
             "producer": "bob-rock-producer", "writers": ["james-hetfield", "lars-ulrich"],
             "songs": [
                 ("the-memory-remains-met", "The Memory Remains"),
                 ("fuel-met", "Fuel"),
                 ("fixxxer-met", "Fixxxer"),
             ]},
            {"slug": "death-magnetic", "title": "Death Magnetic", "year": 2008,
             "producer": "rick-rubin", "writers": ["james-hetfield", "lars-ulrich"],
             "songs": [
                 ("the-day-that-never-comes-met", "The Day That Never Comes"),
                 ("all-nightmare-long-met", "All Nightmare Long"),
             ]},
        ],
    },

    # ==================== 4. AC/DC ====================
    {
        "slug": "ac-dc", "title": "AC/DC", "band_type": "Group",
        "genres": ["Hard Rock"], "scene": "Rock", "formed": 1973,
        "members": [
            ("angus-young", "Guitar"), ("malcolm-young", "Guitar"),
            ("brian-johnson-acdct", "Vocals"), ("phil-rudd", "Drums"), ("cliff-williams", "Bass"),
        ],
        "albums": [
            {"slug": "highway-to-hell", "title": "Highway to Hell", "year": 1979,
             "producer": "mutt-lange", "writers": ["angus-young", "malcolm-young", "bon-scott"],
             "songs": [
                 ("highway-to-hell-acdct", "Highway to Hell"),
                 ("girls-got-rhythm-acdct", "Girls Got Rhythm"),
                 ("touch-too-much-acdct", "Touch Too Much"),
                 ("shot-down-in-flames-acdct", "Shot Down in Flames"),
             ]},
            {"slug": "back-in-black", "title": "Back in Black", "year": 1980,
             "producer": "mutt-lange",
             "writers": ["angus-young", "malcolm-young", "brian-johnson-acdct"],
             "songs": [
                 ("back-in-black-acdct", "Back in Black"),
                 ("you-shook-me-all-night-long-acdct", "You Shook Me All Night Long"),
                 ("hells-bells-acdct", "Hell's Bells"),
                 ("shoot-to-thrill-acdct", "Shoot to Thrill"),
                 ("rock-and-roll-aint-noise-pollution-acdct", "Rock and Roll Ain't Noise Pollution"),
             ]},
            {"slug": "for-those-about-to-rock", "title": "For Those About to Rock", "year": 1981,
             "producer": "mutt-lange",
             "writers": ["angus-young", "malcolm-young", "brian-johnson-acdct"],
             "songs": [
                 ("for-those-about-to-rock-acdct", "For Those About to Rock"),
                 ("let-s-get-it-up-acdct", "Let's Get It Up"),
             ]},
            {"slug": "the-razors-edge", "title": "The Razor's Edge", "year": 1990,
             "producer": "bruce-fairbairn", "writers": ["angus-young", "malcolm-young"],
             "songs": [
                 ("thunderstruck-acdct", "Thunderstruck"),
                 ("moneytalks-acdct", "Moneytalks"),
                 ("are-you-ready-acdct", "Are You Ready?"),
             ]},
        ],
    },

    # ==================== 5. BON JOVI ====================
    {
        "slug": "bon-jovi", "title": "Bon Jovi", "band_type": "Group",
        "genres": ["Hard Rock"], "scene": "Rock", "formed": 1983,
        "members": [
            ("jon-bon-jovi", "Vocals"), ("richie-sambora", "Guitar"),
            ("david-bryan", "Keyboards"), ("tico-torres", "Drums"), ("alec-john-such", "Bass"),
        ],
        "albums": [
            {"slug": "slippery-when-wet", "title": "Slippery When Wet", "year": 1986,
             "producer": "bruce-fairbairn", "writers": ["jon-bon-jovi", "richie-sambora"],
             "songs": [
                 ("livin-on-a-prayer-bj", "Livin' on a Prayer"),
                 ("you-give-love-a-bad-name-bj", "You Give Love a Bad Name"),
                 ("wanted-dead-or-alive-bj", "Wanted Dead or Alive"),
                 ("social-disease-bj", "Social Disease"),
             ]},
            {"slug": "new-jersey-bj", "title": "New Jersey", "year": 1988,
             "producer": "bruce-fairbairn", "writers": ["jon-bon-jovi", "richie-sambora"],
             "songs": [
                 ("bad-medicine-bj", "Bad Medicine"),
                 ("ill-be-there-for-you-bj", "I'll Be There for You"),
                 ("born-to-be-my-baby-bj", "Born to Be My Baby"),
                 ("lay-your-hands-on-me-bj", "Lay Your Hands on Me"),
             ]},
            {"slug": "keep-the-faith-bj", "title": "Keep the Faith", "year": 1992,
             "producer": "bob-rock-producer", "writers": ["jon-bon-jovi", "richie-sambora"],
             "songs": [
                 ("keep-the-faith-bj", "Keep the Faith"),
                 ("bed-of-roses-bj", "Bed of Roses"),
                 ("in-these-arms-bj", "In These Arms"),
             ]},
            {"slug": "these-days-bj", "title": "These Days", "year": 1995,
             "producer": "peter-collins-producer", "writers": ["jon-bon-jovi", "richie-sambora"],
             "songs": [
                 ("always-bj", "Always"),
                 ("something-for-the-pain-bj", "Something for the Pain"),
                 ("this-ain-t-a-love-song-bj", "This Ain't a Love Song"),
             ]},
        ],
    },

    # ==================== 6. DEF LEPPARD ====================
    {
        "slug": "def-leppard", "title": "Def Leppard", "band_type": "Group",
        "genres": ["Hard Rock"], "scene": "Rock", "formed": 1977,
        "members": [
            ("joe-elliott", "Vocals"), ("phil-collen", "Guitar"),
            ("rick-allen", "Drums"), ("rick-savage", "Bass"),
        ],
        "albums": [
            {"slug": "pyromania", "title": "Pyromania", "year": 1983,
             "producer": "mutt-lange", "writers": ["joe-elliott", "phil-collen"],
             "songs": [
                 ("photograph-dl", "Photograph"),
                 ("rock-of-ages-dl", "Rock of Ages"),
                 ("foolin-dl", "Foolin'"),
                 ("too-late-for-love-dl", "Too Late for Love"),
             ]},
            {"slug": "hysteria-dl", "title": "Hysteria", "year": 1987,
             "producer": "mutt-lange", "writers": ["joe-elliott", "phil-collen"],
             "songs": [
                 ("pour-some-sugar-on-me-dl", "Pour Some Sugar on Me"),
                 ("love-bites-dl", "Love Bites"),
                 ("hysteria-dl", "Hysteria"),
                 ("animal-dl", "Animal"),
                 ("armageddon-it-dl", "Armageddon It"),
             ]},
            {"slug": "adrenalize", "title": "Adrenalize", "year": 1992,
             "producer": "mutt-lange", "writers": ["joe-elliott", "phil-collen"],
             "songs": [
                 ("lets-get-rocked-dl", "Let's Get Rocked"),
                 ("have-you-ever-needed-someone-so-bad-dl", "Have You Ever Needed Someone So Bad"),
                 ("stand-up-kick-love-into-motion-dl", "Stand Up (Kick Love into Motion)"),
             ]},
        ],
    },

    # ==================== 7. MOTLEY CRUE ====================
    {
        "slug": "motley-crue", "title": "Motley Crue", "band_type": "Group",
        "genres": ["Hard Rock"], "scene": "Los Angeles", "formed": 1981,
        "members": [
            ("vince-neil", "Vocals"), ("mick-mars", "Guitar"),
            ("nikki-sixx", "Bass"), ("tommy-lee", "Drums"),
        ],
        "albums": [
            {"slug": "shout-at-the-devil", "title": "Shout at the Devil", "year": 1983,
             "producer": "tom-werman", "writers": ["nikki-sixx", "vince-neil"],
             "songs": [
                 ("shout-at-the-devil-mc", "Shout at the Devil"),
                 ("looks-that-kill-mc", "Looks That Kill"),
                 ("too-young-to-fall-in-love-mc", "Too Young to Fall in Love"),
             ]},
            {"slug": "theatre-of-pain", "title": "Theatre of Pain", "year": 1985,
             "producer": "tom-werman", "writers": ["nikki-sixx", "vince-neil"],
             "songs": [
                 ("home-sweet-home-mc", "Home Sweet Home"),
                 ("smokin-in-the-boys-room-mc", "Smokin' in the Boys Room"),
             ]},
            {"slug": "girls-girls-girls-mc", "title": "Girls, Girls, Girls", "year": 1987,
             "producer": "tom-werman", "writers": ["nikki-sixx", "vince-neil"],
             "songs": [
                 ("girls-girls-girls-mc", "Girls, Girls, Girls"),
                 ("wild-side-mc", "Wild Side"),
                 ("you-re-all-i-need-mc", "You're All I Need"),
             ]},
            {"slug": "dr-feelgood", "title": "Dr. Feelgood", "year": 1989,
             "producer": "bob-rock-producer", "writers": ["nikki-sixx", "vince-neil"],
             "songs": [
                 ("kickstart-my-heart-mc", "Kickstart My Heart"),
                 ("dr-feelgood-mc", "Dr. Feelgood"),
                 ("without-you-mc", "Without You"),
             ]},
        ],
    },

    # ==================== 8. AEROSMITH ====================
    {
        "slug": "aerosmith", "title": "Aerosmith", "band_type": "Group",
        "genres": ["Hard Rock"], "scene": "Boston", "formed": 1970,
        "members": [
            ("steven-tyler", "Vocals"), ("joe-perry", "Guitar"),
            ("brad-whitford", "Guitar"), ("tom-hamilton", "Bass"), ("joey-kramer", "Drums"),
        ],
        "albums": [
            {"slug": "toys-in-the-attic", "title": "Toys in the Attic", "year": 1975,
             "producer": "jack-douglas", "writers": ["steven-tyler", "joe-perry"],
             "songs": [
                 ("walk-this-way-aero", "Walk This Way"),
                 ("sweet-emotion-aero", "Sweet Emotion"),
                 ("toys-in-the-attic-aero", "Toys in the Attic"),
             ]},
            {"slug": "rocks-aero", "title": "Rocks", "year": 1976,
             "producer": "jack-douglas", "writers": ["steven-tyler", "joe-perry"],
             "songs": [
                 ("back-in-the-saddle-aero", "Back in the Saddle"),
                 ("last-child-aero", "Last Child"),
                 ("rats-in-the-cellar-aero", "Rats in the Cellar"),
             ]},
            {"slug": "permanent-vacation", "title": "Permanent Vacation", "year": 1987,
             "producer": "bruce-fairbairn", "writers": ["steven-tyler", "joe-perry"],
             "songs": [
                 ("angel-aero", "Angel"),
                 ("dude-looks-like-a-lady-aero", "Dude (Looks Like a Lady)"),
                 ("rag-doll-aero", "Rag Doll"),
             ]},
            {"slug": "pump-aero", "title": "Pump", "year": 1989,
             "producer": "bruce-fairbairn", "writers": ["steven-tyler", "joe-perry"],
             "songs": [
                 ("love-in-an-elevator-aero", "Love in an Elevator"),
                 ("janie-s-got-a-gun-aero", "Janie's Got a Gun"),
                 ("the-other-side-aero", "The Other Side"),
             ]},
            {"slug": "get-a-grip", "title": "Get a Grip", "year": 1993,
             "producer": "bruce-fairbairn", "writers": ["steven-tyler", "joe-perry"],
             "songs": [
                 ("cryin-aero", "Cryin'"),
                 ("amazing-aero", "Amazing"),
                 ("crazy-aero", "Crazy"),
             ]},
        ],
    },

    # ==================== 9. IRON MAIDEN ====================
    {
        "slug": "iron-maiden", "title": "Iron Maiden", "band_type": "Group",
        "genres": ["Heavy Metal"], "scene": "London UK", "formed": 1975,
        "members": [
            ("bruce-dickinson", "Vocals"), ("steve-harris", "Bass/Writer"),
            ("dave-murray", "Guitar"), ("adrian-smith", "Guitar"),
            ("nicko-mcbrain", "Drums"), ("janick-gers", "Guitar"),
        ],
        "albums": [
            {"slug": "iron-maiden-1980", "title": "Iron Maiden", "year": 1980,
             "producer": "martin-birch", "writers": ["steve-harris"],
             "songs": [
                 ("running-free-im", "Running Free"),
                 ("iron-maiden-song-im", "Iron Maiden"),
                 ("phantom-of-the-opera-im", "Phantom of the Opera"),
             ]},
            {"slug": "killers-im", "title": "Killers", "year": 1981,
             "producer": "martin-birch", "writers": ["steve-harris"],
             "songs": [
                 ("wrathchild-im", "Wrathchild"),
                 ("killers-im", "Killers"),
                 ("purgatory-im", "Purgatory"),
             ]},
            {"slug": "number-of-the-beast", "title": "The Number of the Beast", "year": 1982,
             "producer": "martin-birch", "writers": ["steve-harris", "bruce-dickinson"],
             "songs": [
                 ("run-to-the-hills-im", "Run to the Hills"),
                 ("number-of-the-beast-im", "The Number of the Beast"),
                 ("hallowed-be-thy-name-im", "Hallowed Be Thy Name"),
             ]},
            {"slug": "piece-of-mind", "title": "Piece of Mind", "year": 1983,
             "producer": "martin-birch", "writers": ["steve-harris", "bruce-dickinson"],
             "songs": [
                 ("the-trooper-im", "The Trooper"),
                 ("revelations-im", "Revelations"),
                 ("flight-of-icarus-im", "Flight of Icarus"),
             ]},
            {"slug": "powerslave", "title": "Powerslave", "year": 1984,
             "producer": "martin-birch", "writers": ["steve-harris", "bruce-dickinson"],
             "songs": [
                 ("aces-high-im", "Aces High"),
                 ("two-minutes-to-midnight-im", "2 Minutes to Midnight"),
                 ("powerslave-im", "Powerslave"),
             ]},
            {"slug": "somewhere-in-time", "title": "Somewhere in Time", "year": 1986,
             "producer": "martin-birch", "writers": ["steve-harris", "bruce-dickinson"],
             "songs": [
                 ("wasted-years-im", "Wasted Years"),
                 ("stranger-in-a-strange-land-im", "Stranger in a Strange Land"),
             ]},
            {"slug": "seventh-son", "title": "Seventh Son of a Seventh Son", "year": 1988,
             "producer": "martin-birch", "writers": ["steve-harris", "bruce-dickinson"],
             "songs": [
                 ("can-i-play-with-madness-im", "Can I Play with Madness?"),
                 ("infinite-dreams-im", "Infinite Dreams"),
                 ("the-evil-that-men-do-im", "The Evil That Men Do"),
             ]},
            {"slug": "fear-of-the-dark-im", "title": "Fear of the Dark", "year": 1992,
             "producer": "martin-birch", "writers": ["steve-harris", "bruce-dickinson"],
             "songs": [
                 ("fear-of-the-dark-im", "Fear of the Dark"),
                 ("be-quick-or-be-dead-im", "Be Quick or Be Dead"),
             ]},
        ],
    },

    # ==================== 10. OZZY OSBOURNE ====================
    {
        "slug": "ozzy-osbourne", "title": "Ozzy Osbourne", "band_type": "Solo",
        "genres": ["Heavy Metal"], "scene": "Rock", "formed": 1979,
        "members": [],
        "albums": [
            {"slug": "blizzard-of-ozz", "title": "Blizzard of Ozz", "year": 1980,
             "producer": "max-norman",
             "writers": ["ozzy-osbourne-person", "randy-rhoads", "bob-daisley"],
             "songs": [
                 ("crazy-train-ozzy", "Crazy Train"),
                 ("mr-crowley-ozzy", "Mr. Crowley"),
                 ("i-don-t-know-ozzy", "I Don't Know"),
                 ("dee-ozzy", "Dee"),
             ]},
            {"slug": "diary-of-a-madman", "title": "Diary of a Madman", "year": 1981,
             "producer": "max-norman",
             "writers": ["ozzy-osbourne-person", "randy-rhoads", "bob-daisley"],
             "songs": [
                 ("over-the-mountain-ozzy", "Over the Mountain"),
                 ("flying-high-again-ozzy", "Flying High Again"),
                 ("diary-of-a-madman-ozzy", "Diary of a Madman"),
             ]},
            {"slug": "bark-at-the-moon-ozzy", "title": "Bark at the Moon", "year": 1983,
             "producer": "max-norman", "writers": ["ozzy-osbourne-person"],
             "songs": [
                 ("bark-at-the-moon-ozzy", "Bark at the Moon"),
                 ("so-tired-ozzy", "So Tired"),
             ]},
            {"slug": "the-ultimate-sin", "title": "The Ultimate Sin", "year": 1986,
             "producer": "ron-nevison", "writers": ["ozzy-osbourne-person", "zakk-wylde"],
             "songs": [
                 ("shot-in-the-dark-ozzy", "Shot in the Dark"),
                 ("the-ultimate-sin-ozzy", "The Ultimate Sin"),
             ]},
            {"slug": "no-more-tears-ozzy", "title": "No More Tears", "year": 1991,
             "producer": "duane-baron", "writers": ["ozzy-osbourne-person", "zakk-wylde"],
             "songs": [
                 ("no-more-tears-ozzy", "No More Tears"),
                 ("mama-im-coming-home-ozzy", "Mama, I'm Coming Home"),
                 ("hellraiser-ozzy", "Hellraiser"),
             ]},
        ],
    },

    # ==================== 11. JUDAS PRIEST ====================
    {
        "slug": "judas-priest", "title": "Judas Priest", "band_type": "Group",
        "genres": ["Heavy Metal"], "scene": "Rock", "formed": 1969,
        "members": [
            ("rob-halford", "Vocals"), ("glenn-tipton", "Guitar"),
            ("kk-downing", "Guitar"), ("ian-hill", "Bass"), ("dave-holland-jp", "Drums"),
        ],
        "albums": [
            {"slug": "british-steel", "title": "British Steel", "year": 1980,
             "producer": "tom-allom", "writers": ["rob-halford", "glenn-tipton"],
             "songs": [
                 ("breaking-the-law-jp", "Breaking the Law"),
                 ("livin-after-midnight-jp", "Livin' After Midnight"),
                 ("metal-gods-jp", "Metal Gods"),
             ]},
            {"slug": "screaming-for-vengeance", "title": "Screaming for Vengeance", "year": 1982,
             "producer": "tom-allom", "writers": ["rob-halford", "glenn-tipton"],
             "songs": [
                 ("youve-got-another-thing-comin-jp", "You've Got Another Thing Comin'"),
                 ("riding-on-the-wind-jp", "Riding on the Wind"),
                 ("electric-eye-jp", "Electric Eye"),
             ]},
            {"slug": "defenders-of-the-faith", "title": "Defenders of the Faith", "year": 1984,
             "producer": "tom-allom", "writers": ["rob-halford", "glenn-tipton"],
             "songs": [
                 ("freewheel-burning-jp", "Freewheel Burning"),
                 ("some-heads-are-gonna-roll-jp", "Some Heads Are Gonna Roll"),
                 ("jawbreaker-jp", "Jawbreaker"),
             ]},
            {"slug": "turbo-jp", "title": "Turbo", "year": 1986,
             "producer": "tom-allom", "writers": ["rob-halford", "glenn-tipton"],
             "songs": [
                 ("turbo-lover-jp", "Turbo Lover"),
                 ("locked-in-jp", "Locked In"),
                 ("parental-guidance-jp", "Parental Guidance"),
             ]},
            {"slug": "painkiller-jp", "title": "Painkiller", "year": 1990,
             "producer": "tom-allom", "writers": ["rob-halford", "glenn-tipton"],
             "songs": [
                 ("painkiller-jp", "Painkiller"),
                 ("hell-patrol-jp", "Hell Patrol"),
                 ("a-touch-of-evil-jp", "A Touch of Evil"),
             ]},
        ],
    },

    # ==================== 12. WHITESNAKE ====================
    {
        "slug": "whitesnake", "title": "Whitesnake", "band_type": "Group",
        "genres": ["Hard Rock"], "scene": "Rock", "formed": 1978,
        "members": [
            ("david-coverdale", "Vocals"), ("steve-vai", "Guitar"),
            ("adrian-vandenberg", "Guitar"), ("rudy-sarzo", "Bass"), ("tommy-aldridge", "Drums"),
        ],
        "albums": [
            {"slug": "whitesnake-1987", "title": "Whitesnake", "year": 1987,
             "producer": "keith-olsen", "writers": ["david-coverdale"],
             "songs": [
                 ("here-i-go-again-ws", "Here I Go Again"),
                 ("still-of-the-night-ws", "Still of the Night"),
                 ("is-this-love-ws", "Is This Love"),
                 ("give-me-all-your-love-ws", "Give Me All Your Love"),
             ]},
            {"slug": "slip-of-the-tongue", "title": "Slip of the Tongue", "year": 1989,
             "producer": "keith-olsen", "writers": ["david-coverdale"],
             "songs": [
                 ("fool-for-your-loving-ws", "Fool for Your Loving"),
                 ("judgement-day-ws", "Judgement Day"),
                 ("now-youre-gone-ws", "Now You're Gone"),
             ]},
        ],
    },

    # ==================== 13. TOM PETTY AND THE HEARTBREAKERS ====================
    {
        "slug": "tom-petty-heartbreakers",
        "title": "Tom Petty and the Heartbreakers", "band_type": "Group",
        "genres": ["Rock"], "scene": "Rock", "formed": 1976,
        "members": [
            ("tom-petty", "Vocals/Guitar"), ("mike-campbell", "Guitar"),
            ("benmont-tench", "Keyboards"), ("stan-lynch", "Drums"), ("ron-blair-tph", "Bass"),
        ],
        "albums": [
            {"slug": "damn-the-torpedoes", "title": "Damn the Torpedoes", "year": 1979,
             "producer": "jimmy-iovine", "writers": ["tom-petty"],
             "songs": [
                 ("refugee-tph", "Refugee"),
                 ("dont-do-me-like-that-tph", "Don't Do Me Like That"),
                 ("even-the-losers-tph", "Even the Losers"),
             ]},
            {"slug": "hard-promises", "title": "Hard Promises", "year": 1981,
             "producer": "jimmy-iovine", "writers": ["tom-petty"],
             "songs": [
                 ("the-waiting-tph", "The Waiting"),
                 ("a-woman-in-love-tph", "A Woman in Love"),
             ]},
            {"slug": "long-after-dark", "title": "Long After Dark", "year": 1982,
             "producer": "jimmy-iovine", "writers": ["tom-petty"],
             "songs": [
                 ("you-got-lucky-tph", "You Got Lucky"),
                 ("change-of-heart-tph", "Change of Heart"),
             ]},
            {"slug": "southern-accents", "title": "Southern Accents", "year": 1985,
             "producer": "dave-stewart-producer", "writers": ["tom-petty"],
             "songs": [
                 ("dont-come-around-here-no-more-tph", "Don't Come Around Here No More"),
                 ("make-it-better-tph", "Make It Better"),
             ]},
            {"slug": "let-me-up", "title": "Let Me Up", "year": 1987,
             "producer": "tom-petty", "writers": ["tom-petty"],
             "songs": [
                 ("jammin-me-tph", "Jammin' Me"),
                 ("my-life-your-world-tph", "My Life/Your World"),
             ]},
            {"slug": "full-moon-fever", "title": "Full Moon Fever", "year": 1989,
             "producer": "jeff-lynne", "writers": ["tom-petty"],
             "songs": [
                 ("free-fallin-tph", "Free Fallin'"),
                 ("i-wont-back-down-tph", "I Won't Back Down"),
                 ("runnin-down-a-dream-tph", "Runnin' Down a Dream"),
             ]},
            {"slug": "into-the-great-wide-open", "title": "Into the Great Wide Open", "year": 1991,
             "producer": "jeff-lynne", "writers": ["tom-petty"],
             "songs": [
                 ("learning-to-fly-tph", "Learning to Fly"),
                 ("mary-janes-last-dance-tph", "Mary Jane's Last Dance"),
             ]},
        ],
    },

    # ==================== 14. DIRE STRAITS ====================
    {
        "slug": "dire-straits", "title": "Dire Straits", "band_type": "Group",
        "genres": ["Rock"], "scene": "London UK", "formed": 1977,
        "members": [
            ("mark-knopfler", "Vocals/Guitar"), ("john-illsley", "Bass"),
            ("pick-withers", "Drums"), ("alan-clark-ds", "Keyboards"),
        ],
        "albums": [
            {"slug": "dire-straits-1978", "title": "Dire Straits", "year": 1978,
             "producer": "mark-knopfler", "writers": ["mark-knopfler"],
             "songs": [
                 ("sultans-of-swing-ds", "Sultans of Swing"),
                 ("down-to-the-waterline-ds", "Down to the Waterline"),
                 ("water-of-love-ds", "Water of Love"),
             ]},
            {"slug": "communique", "title": "Communique", "year": 1979,
             "producer": "mark-knopfler", "writers": ["mark-knopfler"],
             "songs": [
                 ("once-upon-a-time-in-the-west-ds", "Once Upon a Time in the West"),
                 ("lady-writer-ds", "Lady Writer"),
             ]},
            {"slug": "making-movies", "title": "Making Movies", "year": 1980,
             "producer": "jimmy-iovine", "writers": ["mark-knopfler"],
             "songs": [
                 ("romeo-and-juliet-ds", "Romeo and Juliet"),
                 ("tunnel-of-love-ds", "Tunnel of Love"),
                 ("skateaway-ds", "Skateaway"),
             ]},
            {"slug": "love-over-gold", "title": "Love Over Gold", "year": 1982,
             "producer": "mark-knopfler", "writers": ["mark-knopfler"],
             "songs": [
                 ("private-investigations-ds", "Private Investigations"),
                 ("industrial-disease-ds", "Industrial Disease"),
             ]},
            {"slug": "brothers-in-arms", "title": "Brothers in Arms", "year": 1985,
             "producer": "neil-dorfsman", "writers": ["mark-knopfler"],
             "songs": [
                 ("money-for-nothing-ds", "Money for Nothing"),
                 ("so-far-away-ds", "So Far Away"),
                 ("walk-of-life-ds", "Walk of Life"),
                 ("brothers-in-arms-ds", "Brothers in Arms"),
             ]},
            {"slug": "on-every-street", "title": "On Every Street", "year": 1991,
             "producer": "mark-knopfler", "writers": ["mark-knopfler"],
             "songs": [
                 ("calling-elvira-ds", "Calling Elvira"),
                 ("on-every-street-ds", "On Every Street"),
             ]},
        ],
    },

    # ==================== 15. ZZ TOP ====================
    {
        "slug": "zz-top", "title": "ZZ Top", "band_type": "Group",
        "genres": ["Hard Rock"], "scene": "Rock", "formed": 1969,
        "members": [
            ("billy-gibbons", "Vocals/Guitar"), ("dusty-hill", "Bass/Vocals"),
            ("frank-beard", "Drums"),
        ],
        "albums": [
            {"slug": "tres-hombres", "title": "Tres Hombres", "year": 1973,
             "producer": "bill-ham", "writers": ["billy-gibbons", "dusty-hill"],
             "songs": [
                 ("la-grange-zzt", "La Grange"),
                 ("waitin-for-the-bus-zzt", "Waitin' for the Bus"),
                 ("jesus-just-left-chicago-zzt", "Jesus Just Left Chicago"),
             ]},
            {"slug": "eliminator", "title": "Eliminator", "year": 1983,
             "producer": "bill-ham", "writers": ["billy-gibbons", "dusty-hill"],
             "songs": [
                 ("sharp-dressed-man-zzt", "Sharp Dressed Man"),
                 ("legs-zzt", "Legs"),
                 ("gimme-all-your-lovin-zzt", "Gimme All Your Lovin'"),
                 ("got-me-under-pressure-zzt", "Got Me Under Pressure"),
             ]},
            {"slug": "afterburner-zzt", "title": "Afterburner", "year": 1985,
             "producer": "bill-ham", "writers": ["billy-gibbons", "dusty-hill"],
             "songs": [
                 ("sleeping-bag-zzt", "Sleeping Bag"),
                 ("stages-zzt", "Stages"),
                 ("velcro-fly-zzt", "Velcro Fly"),
             ]},
            {"slug": "recycler-zzt", "title": "Recycler", "year": 1990,
             "producer": "bill-ham", "writers": ["billy-gibbons", "dusty-hill"],
             "songs": [
                 ("doubleback-zzt", "Doubleback"),
                 ("my-head-s-in-mississippi-zzt", "My Head's in Mississippi"),
             ]},
        ],
    },

    # ==================== 16. JOURNEY ====================
    {
        "slug": "journey", "title": "Journey", "band_type": "Group",
        "genres": ["Rock"], "scene": "San Francisco", "formed": 1973,
        "members": [
            ("steve-perry", "Vocals"), ("neal-schon", "Guitar"),
            ("jonathan-cain", "Keyboards"), ("ross-valory", "Bass"),
            ("steve-smith-journey", "Drums"),
        ],
        "albums": [
            {"slug": "escape-journey", "title": "Escape", "year": 1981,
             "producer": "kevin-elson", "writers": ["steve-perry", "neal-schon"],
             "songs": [
                 ("dont-stop-believin-jny", "Don't Stop Believin'"),
                 ("open-arms-jny", "Open Arms"),
                 ("whos-crying-now-jny", "Who's Crying Now"),
                 ("dead-or-alive-jny", "Dead or Alive"),
             ]},
            {"slug": "frontiers-journey", "title": "Frontiers", "year": 1983,
             "producer": "kevin-elson", "writers": ["steve-perry", "neal-schon"],
             "songs": [
                 ("separate-ways-jny", "Separate Ways"),
                 ("faithfully-jny", "Faithfully"),
                 ("send-her-my-love-jny", "Send Her My Love"),
             ]},
            {"slug": "raised-on-radio", "title": "Raised on Radio", "year": 1986,
             "producer": "kevin-elson", "writers": ["steve-perry", "neal-schon"],
             "songs": [
                 ("be-good-to-yourself-jny", "Be Good to Yourself"),
                 ("suzanne-jny", "Suzanne"),
                 ("i-ll-be-alright-without-you-jny", "I'll Be Alright Without You"),
             ]},
        ],
    },

    # ==================== 17. FOREIGNER ====================
    {
        "slug": "foreigner", "title": "Foreigner", "band_type": "Group",
        "genres": ["Rock"], "scene": "Rock", "formed": 1976,
        "members": [
            ("lou-gramm", "Vocals"), ("mick-jones-foreigner", "Guitar"),
            ("ian-mcdonald", "Guitar"), ("al-greenwood", "Keyboards"),
            ("dennis-elliott", "Drums"), ("ed-gagliardi", "Bass"),
        ],
        "albums": [
            {"slug": "double-vision", "title": "Double Vision", "year": 1978,
             "producer": "keith-olsen",
             "writers": ["lou-gramm", "mick-jones-foreigner"],
             "songs": [
                 ("hot-blooded-for", "Hot Blooded"),
                 ("double-vision-for", "Double Vision"),
                 ("blue-morning-blue-day-for", "Blue Morning, Blue Day"),
             ]},
            {"slug": "head-games", "title": "Head Games", "year": 1979,
             "producer": "roy-thomas-baker",
             "writers": ["lou-gramm", "mick-jones-foreigner"],
             "songs": [
                 ("dirty-white-boy-for", "Dirty White Boy"),
                 ("head-games-for", "Head Games"),
                 ("women-for", "Women"),
             ]},
            {"slug": "foreigner-4", "title": "4", "year": 1981,
             "producer": "mutt-lange",
             "writers": ["lou-gramm", "mick-jones-foreigner"],
             "songs": [
                 ("waiting-for-a-girl-like-you-for", "Waiting for a Girl Like You"),
                 ("juke-box-hero-for", "Juke Box Hero"),
                 ("urgent-for", "Urgent"),
                 ("night-life-for", "Night Life"),
             ]},
            {"slug": "agent-provocateur", "title": "Agent Provocateur", "year": 1984,
             "producer": "alex-sadkin",
             "writers": ["lou-gramm", "mick-jones-foreigner"],
             "songs": [
                 ("i-want-to-know-what-love-is-for", "I Want to Know What Love Is"),
                 ("that-was-yesterday-for", "That Was Yesterday"),
                 ("reaction-to-action-for", "Reaction to Action"),
             ]},
        ],
    },

    # ==================== 18. BRUCE SPRINGSTEEN ====================
    {
        "slug": "bruce-springsteen", "title": "Bruce Springsteen", "band_type": "Solo",
        "genres": ["Rock"], "scene": "Rock", "formed": 1972,
        "members": [
            ("max-weinberg", "Drums"), ("roy-bittan", "Keyboards"),
            ("steve-van-zandt", "Guitar"), ("garry-tallent", "Bass"),
            ("clarence-clemons", "Saxophone"),
        ],
        "albums": [
            {"slug": "born-to-run", "title": "Born to Run", "year": 1975,
             "producer": "jon-landau", "writers": ["bruce-springsteen-person"],
             "songs": [
                 ("born-to-run-bs", "Born to Run"),
                 ("thunder-road-bs", "Thunder Road"),
                 ("backstreets-bs", "Backstreets"),
                 ("tenth-avenue-bs", "Tenth Avenue Freeze-Out"),
             ]},
            {"slug": "darkness-on-the-edge-of-town",
             "title": "Darkness on the Edge of Town", "year": 1978,
             "producer": "jon-landau", "writers": ["bruce-springsteen-person"],
             "songs": [
                 ("badlands-bs", "Badlands"),
                 ("the-promised-land-bs", "The Promised Land"),
                 ("racing-in-the-street-bs", "Racing in the Street"),
                 ("darkness-on-the-edge-of-town-bs", "Darkness on the Edge of Town"),
             ]},
            {"slug": "the-river-bs", "title": "The River", "year": 1980,
             "producer": "jon-landau", "writers": ["bruce-springsteen-person"],
             "songs": [
                 ("hungry-heart-bs", "Hungry Heart"),
                 ("the-river-bs", "The River"),
                 ("two-hearts-bs", "Two Hearts"),
                 ("cadillac-ranch-bs", "Cadillac Ranch"),
             ]},
            {"slug": "nebraska-bs", "title": "Nebraska", "year": 1982,
             "producer": "bruce-springsteen-person",
             "writers": ["bruce-springsteen-person"],
             "songs": [
                 ("nebraska-bs", "Nebraska"),
                 ("atlantic-city-bs", "Atlantic City"),
                 ("johnny-99-bs", "Johnny 99"),
             ]},
            {"slug": "born-in-the-usa", "title": "Born in the USA", "year": 1984,
             "producer": "jon-landau", "writers": ["bruce-springsteen-person"],
             "songs": [
                 ("born-in-the-usa-bs", "Born in the U.S.A."),
                 ("dancing-in-the-dark-bs", "Dancing in the Dark"),
                 ("glory-days-bs", "Glory Days"),
                 ("im-on-fire-bs", "I'm on Fire"),
                 ("cover-me-bs", "Cover Me"),
             ]},
            {"slug": "tunnel-of-love-bs", "title": "Tunnel of Love", "year": 1987,
             "producer": "jon-landau", "writers": ["bruce-springsteen-person"],
             "songs": [
                 ("tunnel-of-love-bs", "Tunnel of Love"),
                 ("brilliant-disguise-bs", "Brilliant Disguise"),
                 ("one-step-up-bs", "One Step Up"),
             ]},
        ],
    },

    # ==================== 19. JOAN JETT AND THE BLACKHEARTS ====================
    {
        "slug": "joan-jett", "title": "Joan Jett and the Blackhearts",
        "band_type": "Group", "genres": ["Punk Rock"], "scene": "Punk Rock", "formed": 1979,
        "members": [
            ("joan-jett-person", "Vocals/Guitar"), ("ricky-byrd", "Guitar"),
            ("gary-ryan", "Bass"), ("lee-crystal", "Drums"),
        ],
        "albums": [
            {"slug": "bad-reputation-jj", "title": "Bad Reputation", "year": 1980,
             "producer": "kenny-laguna", "writers": ["joan-jett-person"],
             "songs": [
                 ("bad-reputation-jj", "Bad Reputation"),
                 ("make-believe-jj", "Make Believe"),
                 ("do-you-wanna-touch-me-jj", "Do You Wanna Touch Me"),
             ]},
            {"slug": "i-love-rock-n-roll-jj", "title": "I Love Rock n Roll", "year": 1981,
             "producer": "kenny-laguna", "writers": ["joan-jett-person"],
             "songs": [
                 ("i-love-rock-n-roll-jj", "I Love Rock 'n' Roll"),
                 ("crimson-and-clover-jj", "Crimson and Clover"),
             ]},
            {"slug": "album-jj", "title": "Album", "year": 1983,
             "producer": "kenny-laguna", "writers": ["joan-jett-person"],
             "songs": [
                 ("i-hate-myself-for-loving-you-jj", "I Hate Myself for Loving You"),
                 ("everyday-people-jj", "Everyday People"),
             ]},
            {"slug": "good-music-jj", "title": "Good Music", "year": 1986,
             "producer": "kenny-laguna", "writers": ["joan-jett-person"],
             "songs": [
                 ("good-music-jj", "Good Music"),
                 ("cherry-bomb-jj", "Cherry Bomb"),
             ]},
        ],
    },

    # ==================== 20. PAT BENATAR ====================
    {
        "slug": "pat-benatar", "title": "Pat Benatar", "band_type": "Solo",
        "genres": ["Rock"], "scene": "Rock", "formed": 1979,
        "members": [],
        "albums": [
            {"slug": "in-the-heat-of-the-night-pb",
             "title": "In the Heat of the Night", "year": 1979,
             "producer": "peter-coleman",
             "writers": ["pat-benatar-person", "neil-giraldo"],
             "songs": [
                 ("heartbreaker-pb", "Heartbreaker"),
                 ("we-live-for-love-pb", "We Live for Love"),
                 ("if-you-think-you-know-how-to-love-me-pb",
                  "If You Think You Know How to Love Me"),
             ]},
            {"slug": "crimes-of-passion-pb", "title": "Crimes of Passion", "year": 1980,
             "producer": "neil-giraldo",
             "writers": ["pat-benatar-person", "neil-giraldo"],
             "songs": [
                 ("hit-me-with-your-best-shot-pb", "Hit Me with Your Best Shot"),
                 ("hell-is-for-children-pb", "Hell Is for Children"),
                 ("treat-me-right-pb", "Treat Me Right"),
             ]},
            {"slug": "precious-time-pb", "title": "Precious Time", "year": 1981,
             "producer": "neil-giraldo",
             "writers": ["pat-benatar-person", "neil-giraldo"],
             "songs": [
                 ("promises-in-the-dark-pb", "Promises in the Dark"),
                 ("fire-and-ice-pb", "Fire and Ice"),
                 ("precious-time-pb", "Precious Time"),
             ]},
            {"slug": "get-nervous-pb", "title": "Get Nervous", "year": 1982,
             "producer": "neil-giraldo",
             "writers": ["pat-benatar-person", "neil-giraldo"],
             "songs": [
                 ("shadows-of-the-night-pb", "Shadows of the Night"),
                 ("little-too-late-pb", "Little Too Late"),
             ]},
            {"slug": "tropico-pb", "title": "Tropico", "year": 1984,
             "producer": "neil-giraldo",
             "writers": ["pat-benatar-person", "neil-giraldo"],
             "songs": [
                 ("love-is-a-battlefield-pb", "Love Is a Battlefield"),
                 ("we-belong-pb", "We Belong"),
             ]},
            {"slug": "seven-the-hard-way-pb", "title": "Seven the Hard Way", "year": 1985,
             "producer": "neil-giraldo",
             "writers": ["pat-benatar-person", "neil-giraldo"],
             "songs": [
                 ("invincible-pb", "Invincible"),
                 ("sex-as-a-weapon-pb", "Sex as a Weapon"),
             ]},
        ],
    },

    # ==================== 21. FLEETWOOD MAC ====================
    {
        "slug": "fleetwood-mac", "title": "Fleetwood Mac", "band_type": "Group",
        "genres": ["Rock"], "scene": "Los Angeles", "formed": 1967,
        "members": [
            ("stevie-nicks", "Vocals"), ("lindsey-buckingham", "Vocals/Guitar"),
            ("christine-mcvie", "Vocals/Keyboards"),
            ("john-mcvie", "Bass"), ("mick-fleetwood", "Drums"),
        ],
        "albums": [
            {"slug": "rumours", "title": "Rumours", "year": 1977,
             "producer": "ken-caillat",
             "writers": ["stevie-nicks", "lindsey-buckingham", "christine-mcvie"],
             "songs": [
                 ("go-your-own-way-fm", "Go Your Own Way"),
                 ("the-chain-fm", "The Chain"),
                 ("dreams-fm", "Dreams"),
                 ("gold-dust-woman-fm", "Gold Dust Woman"),
                 ("dont-stop-fm", "Don't Stop"),
                 ("you-make-loving-fun-fm", "You Make Loving Fun"),
             ]},
            {"slug": "tusk-fm", "title": "Tusk", "year": 1979,
             "producer": "lindsey-buckingham",
             "writers": ["stevie-nicks", "lindsey-buckingham", "christine-mcvie"],
             "songs": [
                 ("sara-fm", "Sara"),
                 ("tusk-fm", "Tusk"),
                 ("think-about-me-fm", "Think About Me"),
             ]},
            {"slug": "mirage-fm", "title": "Mirage", "year": 1982,
             "producer": "lindsey-buckingham",
             "writers": ["stevie-nicks", "lindsey-buckingham", "christine-mcvie"],
             "songs": [
                 ("hold-me-fm", "Hold Me"),
                 ("gypsy-fm", "Gypsy"),
                 ("oh-well-fm", "Oh Well"),
             ]},
            {"slug": "tango-in-the-night", "title": "Tango in the Night", "year": 1987,
             "producer": "lindsey-buckingham",
             "writers": ["stevie-nicks", "lindsey-buckingham", "christine-mcvie"],
             "songs": [
                 ("little-lies-fm", "Little Lies"),
                 ("everywhere-fm", "Everywhere"),
                 ("big-love-fm", "Big Love"),
                 ("seven-wonders-fm", "Seven Wonders"),
             ]},
            {"slug": "behind-the-mask-fm", "title": "Behind the Mask", "year": 1990,
             "producer": "greg-ladanyi",
             "writers": ["stevie-nicks", "christine-mcvie"],
             "songs": [
                 ("save-me-fm", "Save Me"),
                 ("skies-the-limit-fm", "Skies the Limit"),
             ]},
        ],
    },

    # ==================== 22. BRYAN ADAMS ====================
    {
        "slug": "bryan-adams", "title": "Bryan Adams", "band_type": "Solo",
        "genres": ["Rock"], "scene": "Canadian", "formed": 1978,
        "members": [],
        "albums": [
            {"slug": "cuts-like-a-knife", "title": "Cuts Like a Knife", "year": 1983,
             "producer": "bob-clearmountain",
             "writers": ["bryan-adams-person", "jim-vallance"],
             "songs": [
                 ("cuts-like-a-knife-ba", "Cuts Like a Knife"),
                 ("straight-from-the-heart-ba", "Straight from the Heart"),
                 ("this-time-ba", "This Time"),
             ]},
            {"slug": "reckless-ba", "title": "Reckless", "year": 1984,
             "producer": "bob-clearmountain",
             "writers": ["bryan-adams-person", "jim-vallance"],
             "songs": [
                 ("summer-of-69-ba", "Summer of '69"),
                 ("run-to-you-ba", "Run to You"),
                 ("somebody-ba", "Somebody"),
                 ("kids-wanna-rock-ba", "Kids Wanna Rock"),
             ]},
            {"slug": "into-the-fire-ba", "title": "Into the Fire", "year": 1987,
             "producer": "bob-clearmountain",
             "writers": ["bryan-adams-person", "jim-vallance"],
             "songs": [
                 ("heat-of-the-night-ba", "Heat of the Night"),
                 ("hearts-on-fire-ba", "Hearts on Fire"),
             ]},
            {"slug": "waking-up-the-neighbours",
             "title": "Waking Up the Neighbours", "year": 1991,
             "producer": "robert-john-lange",
             "writers": ["bryan-adams-person", "jim-vallance"],
             "songs": [
                 ("everything-i-do-i-do-it-for-you-ba",
                  "Everything I Do I Do It for You"),
                 ("cant-stop-this-thing-we-started-ba",
                  "Can't Stop This Thing We Started"),
                 ("do-i-have-to-say-the-words-ba",
                  "Do I Have to Say the Words?"),
             ]},
        ],
    },

    # ==================== 23. POISON ====================
    {
        "slug": "poison", "title": "Poison", "band_type": "Group",
        "genres": ["Hard Rock"], "scene": "Los Angeles", "formed": 1983,
        "members": [
            ("bret-michaels", "Vocals"), ("cc-deville", "Guitar"),
            ("bobby-dall", "Bass"), ("rikki-rockett", "Drums"),
        ],
        "albums": [
            {"slug": "look-what-the-cat-dragged-in",
             "title": "Look What the Cat Dragged In", "year": 1986,
             "producer": "ric-browde",
             "writers": ["bret-michaels", "cc-deville"],
             "songs": [
                 ("talk-dirty-to-me-poi", "Talk Dirty to Me"),
                 ("cry-tough-poi", "Cry Tough"),
                 ("i-want-action-poi", "I Want Action"),
             ]},
            {"slug": "open-up-and-say-ahh",
             "title": "Open Up and Say Ahh", "year": 1988,
             "producer": "tom-werman",
             "writers": ["bret-michaels", "cc-deville"],
             "songs": [
                 ("every-rose-has-its-thorn-poi", "Every Rose Has Its Thorn"),
                 ("nothin-but-a-good-time-poi", "Nothin' but a Good Time"),
                 ("your-mama-dont-dance-poi", "Your Mama Don't Dance"),
                 ("fallen-angel-poi", "Fallen Angel"),
             ]},
            {"slug": "flesh-and-blood-poi", "title": "Flesh and Blood", "year": 1990,
             "producer": "bruce-fairbairn",
             "writers": ["bret-michaels", "cc-deville"],
             "songs": [
                 ("unskinny-bop-poi", "Unskinny Bop"),
                 ("something-to-believe-in-poi", "Something to Believe In"),
                 ("ride-the-wind-poi", "Ride the Wind"),
             ]},
        ],
    },

    # ==================== 24. STEVIE RAY VAUGHAN ====================
    {
        "slug": "stevie-ray-vaughan", "title": "Stevie Ray Vaughan",
        "band_type": "Solo", "genres": ["Blues Rock"], "scene": "Rock", "formed": 1978,
        "members": [],
        "albums": [
            {"slug": "texas-flood", "title": "Texas Flood", "year": 1983,
             "producer": "john-hammond-jr",
             "writers": ["stevie-ray-vaughan-person"],
             "songs": [
                 ("pride-and-joy-srv", "Pride and Joy"),
                 ("texas-flood-srv", "Texas Flood"),
                 ("love-struck-baby-srv", "Love Struck Baby"),
             ]},
            {"slug": "couldnt-stand-the-weather",
             "title": "Couldn't Stand the Weather", "year": 1984,
             "producer": "john-hammond-jr",
             "writers": ["stevie-ray-vaughan-person"],
             "songs": [
                 ("couldnt-stand-the-weather-srv", "Couldn't Stand the Weather"),
                 ("the-things-that-i-used-to-do-srv", "The Things That I Used to Do"),
                 ("voodoo-chile-srv", "Voodoo Chile"),
             ]},
            {"slug": "soul-to-soul-srv", "title": "Soul to Soul", "year": 1985,
             "producer": "richard-mullen",
             "writers": ["stevie-ray-vaughan-person"],
             "songs": [
                 ("say-what-srv", "Say What!"),
                 ("look-at-little-sister-srv", "Look at Little Sister"),
                 ("change-it-srv", "Change It"),
             ]},
            {"slug": "in-step-srv", "title": "In Step", "year": 1989,
             "producer": "jim-gaines",
             "writers": ["stevie-ray-vaughan-person"],
             "songs": [
                 ("the-house-is-rockin-srv", "The House Is Rockin'"),
                 ("crossfire-srv", "Crossfire"),
                 ("wall-of-denial-srv", "Wall of Denial"),
                 ("tightrope-srv", "Tightrope"),
             ]},
        ],
    },

    # ==================== 25. REO SPEEDWAGON ====================
    {
        "slug": "reo-speedwagon", "title": "REO Speedwagon", "band_type": "Group",
        "genres": ["Rock"], "scene": "Rock", "formed": 1967,
        "members": [
            ("kevin-cronin", "Vocals/Guitar"), ("gary-richrath", "Guitar"),
            ("neal-doughty", "Keyboards"), ("bruce-hall", "Bass"), ("alan-gratzer", "Drums"),
        ],
        "albums": [
            {"slug": "hi-infidelity", "title": "Hi Infidelity", "year": 1980,
             "producer": "kevin-cronin",
             "writers": ["kevin-cronin", "gary-richrath"],
             "songs": [
                 ("keep-on-loving-you-reo", "Keep On Loving You"),
                 ("take-it-on-the-run-reo", "Take It on the Run"),
                 ("in-your-letter-reo", "In Your Letter"),
                 ("dont-let-him-go-reo", "Don't Let Him Go"),
             ]},
            {"slug": "good-trouble-reo", "title": "Good Trouble", "year": 1982,
             "producer": "kevin-cronin",
             "writers": ["kevin-cronin", "gary-richrath"],
             "songs": [
                 ("keep-the-fire-burnin-reo", "Keep the Fire Burnin'"),
                 ("sweet-time-reo", "Sweet Time"),
             ]},
            {"slug": "wheels-are-turnin-reo", "title": "Wheels Are Turnin'", "year": 1984,
             "producer": "alan-gratzer",
             "writers": ["kevin-cronin"],
             "songs": [
                 ("cant-fight-this-feeling-reo", "Can't Fight This Feeling"),
                 ("i-do-wanna-know-reo", "I Do Wanna Know"),
                 ("rock-n-roll-star-reo", "Rock 'n' Roll Star"),
             ]},
            {"slug": "life-as-we-know-it-reo", "title": "Life as We Know It", "year": 1987,
             "producer": "kevin-cronin",
             "writers": ["kevin-cronin"],
             "songs": [
                 ("that-ain-t-love-reo", "That Ain't Love"),
                 ("in-my-dreams-reo", "In My Dreams"),
             ]},
        ],
    },
]

# ============================================================
# PEOPLE DATA: (slug, title, [(band_slug, role), ...])
# ============================================================
PEOPLE_DATA = [
    # Van Halen
    ("david-lee-roth", "David Lee Roth", [("van-halen", "Vocals")]),
    ("eddie-van-halen", "Eddie Van Halen", [("van-halen", "Guitar")]),
    ("alex-van-halen", "Alex Van Halen", [("van-halen", "Drums")]),
    ("michael-anthony", "Michael Anthony", [("van-halen", "Bass")]),
    ("ted-templeman", "Ted Templeman", []),
    ("mick-jones-producer", "Mick Jones", []),
    # GNR
    ("axl-rose", "Axl Rose", [("guns-n-roses", "Vocals")]),
    ("slash", "Slash", [("guns-n-roses", "Guitar")]),
    ("duff-mckagan", "Duff McKagan", [("guns-n-roses", "Bass")]),
    ("izzy-stradlin", "Izzy Stradlin", [("guns-n-roses", "Guitar")]),
    ("steven-adler", "Steven Adler", [("guns-n-roses", "Drums")]),
    ("dizzy-reed", "Dizzy Reed", [("guns-n-roses", "Keyboards")]),
    ("mike-clink", "Mike Clink", []),
    # Metallica
    ("james-hetfield", "James Hetfield", [("metallica", "Vocals/Guitar")]),
    ("lars-ulrich", "Lars Ulrich", [("metallica", "Drums")]),
    ("kirk-hammett", "Kirk Hammett", [("metallica", "Guitar")]),
    ("robert-trujillo", "Robert Trujillo", [("metallica", "Bass")]),
    ("jason-newsted", "Jason Newsted", [("metallica", "Bass")]),
    ("cliff-burton", "Cliff Burton", [("metallica", "Bass")]),
    ("paul-curcio", "Paul Curcio", []),
    ("flemming-rasmussen", "Flemming Rasmussen", []),
    ("bob-rock-producer", "Bob Rock", []),
    ("rick-rubin", "Rick Rubin", []),
    # AC/DC
    ("angus-young", "Angus Young", [("ac-dc", "Guitar")]),
    ("malcolm-young", "Malcolm Young", [("ac-dc", "Guitar")]),
    ("brian-johnson-acdct", "Brian Johnson", [("ac-dc", "Vocals")]),
    ("phil-rudd", "Phil Rudd", [("ac-dc", "Drums")]),
    ("cliff-williams", "Cliff Williams", [("ac-dc", "Bass")]),
    ("bon-scott", "Bon Scott", [("ac-dc", "Vocals")]),
    ("mutt-lange", "Mutt Lange", []),
    # Bon Jovi
    ("jon-bon-jovi", "Jon Bon Jovi", [("bon-jovi", "Vocals")]),
    ("richie-sambora", "Richie Sambora", [("bon-jovi", "Guitar")]),
    ("david-bryan", "David Bryan", [("bon-jovi", "Keyboards")]),
    ("tico-torres", "Tico Torres", [("bon-jovi", "Drums")]),
    ("alec-john-such", "Alec John Such", [("bon-jovi", "Bass")]),
    ("bruce-fairbairn", "Bruce Fairbairn", []),
    # Def Leppard
    ("joe-elliott", "Joe Elliott", [("def-leppard", "Vocals")]),
    ("phil-collen", "Phil Collen", [("def-leppard", "Guitar")]),
    ("steve-clark", "Steve Clark", [("def-leppard", "Guitar")]),
    ("rick-allen", "Rick Allen", [("def-leppard", "Drums")]),
    ("rick-savage", "Rick Savage", [("def-leppard", "Bass")]),
    # Motley Crue
    ("vince-neil", "Vince Neil", [("motley-crue", "Vocals")]),
    ("mick-mars", "Mick Mars", [("motley-crue", "Guitar")]),
    ("nikki-sixx", "Nikki Sixx", [("motley-crue", "Bass")]),
    ("tommy-lee", "Tommy Lee", [("motley-crue", "Drums")]),
    ("tom-werman", "Tom Werman", []),
    # Aerosmith
    ("steven-tyler", "Steven Tyler", [("aerosmith", "Vocals")]),
    ("joe-perry", "Joe Perry", [("aerosmith", "Guitar")]),
    ("brad-whitford", "Brad Whitford", [("aerosmith", "Guitar")]),
    ("tom-hamilton", "Tom Hamilton", [("aerosmith", "Bass")]),
    ("joey-kramer", "Joey Kramer", [("aerosmith", "Drums")]),
    ("jack-douglas", "Jack Douglas", []),
    # Iron Maiden
    ("bruce-dickinson", "Bruce Dickinson", [("iron-maiden", "Vocals")]),
    ("steve-harris", "Steve Harris", [("iron-maiden", "Bass/Writer")]),
    ("dave-murray", "Dave Murray", [("iron-maiden", "Guitar")]),
    ("adrian-smith", "Adrian Smith", [("iron-maiden", "Guitar")]),
    ("nicko-mcbrain", "Nicko McBrain", [("iron-maiden", "Drums")]),
    ("janick-gers", "Janick Gers", [("iron-maiden", "Guitar")]),
    ("martin-birch", "Martin Birch", []),
    # Ozzy
    ("ozzy-osbourne-person", "Ozzy Osbourne", [("ozzy-osbourne", "Vocals")]),
    ("randy-rhoads", "Randy Rhoads", [("ozzy-osbourne", "Guitar")]),
    ("zakk-wylde", "Zakk Wylde", [("ozzy-osbourne", "Guitar")]),
    ("bob-daisley", "Bob Daisley", [("ozzy-osbourne", "Bass")]),
    ("lee-kerslake", "Lee Kerslake", [("ozzy-osbourne", "Drums")]),
    ("max-norman", "Max Norman", []),
    ("ron-nevison", "Ron Nevison", []),
    ("duane-baron", "Duane Baron", []),
    # Judas Priest
    ("rob-halford", "Rob Halford", [("judas-priest", "Vocals")]),
    ("glenn-tipton", "Glenn Tipton", [("judas-priest", "Guitar")]),
    ("kk-downing", "K.K. Downing", [("judas-priest", "Guitar")]),
    ("ian-hill", "Ian Hill", [("judas-priest", "Bass")]),
    ("dave-holland-jp", "Dave Holland", [("judas-priest", "Drums")]),
    ("tom-allom", "Tom Allom", []),
    # Whitesnake
    ("david-coverdale", "David Coverdale", [("whitesnake", "Vocals")]),
    ("steve-vai", "Steve Vai", [("whitesnake", "Guitar")]),
    ("adrian-vandenberg", "Adrian Vandenberg", [("whitesnake", "Guitar")]),
    ("rudy-sarzo", "Rudy Sarzo", [("whitesnake", "Bass")]),
    ("tommy-aldridge", "Tommy Aldridge", [("whitesnake", "Drums")]),
    ("keith-olsen", "Keith Olsen", []),
    # Tom Petty
    ("tom-petty", "Tom Petty", [("tom-petty-heartbreakers", "Vocals/Guitar")]),
    ("mike-campbell", "Mike Campbell", [("tom-petty-heartbreakers", "Guitar")]),
    ("benmont-tench", "Benmont Tench", [("tom-petty-heartbreakers", "Keyboards")]),
    ("stan-lynch", "Stan Lynch", [("tom-petty-heartbreakers", "Drums")]),
    ("ron-blair-tph", "Ron Blair", [("tom-petty-heartbreakers", "Bass")]),
    ("jimmy-iovine", "Jimmy Iovine", []),
    ("jeff-lynne", "Jeff Lynne", []),
    ("dave-stewart-producer", "Dave Stewart", []),
    # Dire Straits
    ("mark-knopfler", "Mark Knopfler", [("dire-straits", "Vocals/Guitar")]),
    ("john-illsley", "John Illsley", [("dire-straits", "Bass")]),
    ("pick-withers", "Pick Withers", [("dire-straits", "Drums")]),
    ("alan-clark-ds", "Alan Clark", [("dire-straits", "Keyboards")]),
    ("neil-dorfsman", "Neil Dorfsman", []),
    # ZZ Top
    ("billy-gibbons", "Billy Gibbons", [("zz-top", "Vocals/Guitar")]),
    ("dusty-hill", "Dusty Hill", [("zz-top", "Bass/Vocals")]),
    ("frank-beard", "Frank Beard", [("zz-top", "Drums")]),
    ("bill-ham", "Bill Ham", []),
    # Journey
    ("steve-perry", "Steve Perry", [("journey", "Vocals")]),
    ("neal-schon", "Neal Schon", [("journey", "Guitar")]),
    ("jonathan-cain", "Jonathan Cain", [("journey", "Keyboards")]),
    ("ross-valory", "Ross Valory", [("journey", "Bass")]),
    ("steve-smith-journey", "Steve Smith", [("journey", "Drums")]),
    ("kevin-elson", "Kevin Elson", []),
    # Foreigner
    ("lou-gramm", "Lou Gramm", [("foreigner", "Vocals")]),
    ("mick-jones-foreigner", "Mick Jones", [("foreigner", "Guitar")]),
    ("ian-mcdonald", "Ian McDonald", [("foreigner", "Guitar")]),
    ("al-greenwood", "Al Greenwood", [("foreigner", "Keyboards")]),
    ("dennis-elliott", "Dennis Elliott", [("foreigner", "Drums")]),
    ("ed-gagliardi", "Ed Gagliardi", [("foreigner", "Bass")]),
    ("roy-thomas-baker", "Roy Thomas Baker", []),
    ("alex-sadkin", "Alex Sadkin", []),
    # Bruce Springsteen
    ("bruce-springsteen-person", "Bruce Springsteen",
     [("bruce-springsteen", "Vocals/Guitar")]),
    ("max-weinberg", "Max Weinberg", [("bruce-springsteen", "Drums")]),
    ("roy-bittan", "Roy Bittan", [("bruce-springsteen", "Keyboards")]),
    ("steve-van-zandt", "Steve Van Zandt", [("bruce-springsteen", "Guitar")]),
    ("garry-tallent", "Garry Tallent", [("bruce-springsteen", "Bass")]),
    ("clarence-clemons", "Clarence Clemons", [("bruce-springsteen", "Saxophone")]),
    ("jon-landau", "Jon Landau", []),
    # Joan Jett
    ("joan-jett-person", "Joan Jett", [("joan-jett", "Vocals/Guitar")]),
    ("ricky-byrd", "Ricky Byrd", [("joan-jett", "Guitar")]),
    ("gary-ryan", "Gary Ryan", [("joan-jett", "Bass")]),
    ("lee-crystal", "Lee Crystal", [("joan-jett", "Drums")]),
    ("kenny-laguna", "Kenny Laguna", []),
    # Pat Benatar
    ("pat-benatar-person", "Pat Benatar", [("pat-benatar", "Vocals")]),
    ("neil-giraldo", "Neil Giraldo", [("pat-benatar", "Guitar")]),
    ("peter-coleman", "Peter Coleman", []),
    # Fleetwood Mac
    ("stevie-nicks", "Stevie Nicks", [("fleetwood-mac", "Vocals")]),
    ("lindsey-buckingham", "Lindsey Buckingham", [("fleetwood-mac", "Vocals/Guitar")]),
    ("christine-mcvie", "Christine McVie", [("fleetwood-mac", "Vocals/Keyboards")]),
    ("john-mcvie", "John McVie", [("fleetwood-mac", "Bass")]),
    ("mick-fleetwood", "Mick Fleetwood", [("fleetwood-mac", "Drums")]),
    ("ken-caillat", "Ken Caillat", []),
    ("greg-ladanyi", "Greg Ladanyi", []),
    # Bryan Adams
    ("bryan-adams-person", "Bryan Adams", [("bryan-adams", "Vocals/Guitar")]),
    ("bob-clearmountain", "Bob Clearmountain", []),
    ("jim-vallance", "Jim Vallance", []),
    ("robert-john-lange", "Robert John Lange", []),
    # Poison
    ("bret-michaels", "Bret Michaels", [("poison", "Vocals")]),
    ("cc-deville", "C.C. DeVille", [("poison", "Guitar")]),
    ("bobby-dall", "Bobby Dall", [("poison", "Bass")]),
    ("rikki-rockett", "Rikki Rockett", [("poison", "Drums")]),
    ("ric-browde", "Ric Browde", []),
    # SRV
    ("stevie-ray-vaughan-person", "Stevie Ray Vaughan",
     [("stevie-ray-vaughan", "Vocals/Guitar")]),
    ("tommy-shannon", "Tommy Shannon", [("stevie-ray-vaughan", "Bass")]),
    ("chris-layton", "Chris Layton", [("stevie-ray-vaughan", "Drums")]),
    ("john-hammond-jr", "John Hammond Jr.", []),
    ("richard-mullen", "Richard Mullen", []),
    ("jim-gaines", "Jim Gaines", []),
    # REO Speedwagon
    ("kevin-cronin", "Kevin Cronin", [("reo-speedwagon", "Vocals/Guitar")]),
    ("gary-richrath", "Gary Richrath", [("reo-speedwagon", "Guitar")]),
    ("neal-doughty", "Neal Doughty", [("reo-speedwagon", "Keyboards")]),
    ("bruce-hall", "Bruce Hall", [("reo-speedwagon", "Bass")]),
    ("alan-gratzer", "Alan Gratzer", [("reo-speedwagon", "Drums")]),
    ("peter-collins-producer", "Peter Collins", []),
]

# ============================================================
# FILE GENERATORS
# ============================================================

def gen_artist(a):
    lines = ["---", f"title: {q(a['title'])}", f"slug: {a['slug']}",
             f"band_type: {a['band_type']}"]
    genres_str = "[" + ", ".join(q(g) for g in a["genres"]) + "]"
    lines.append(f"genres: {genres_str}")
    lines.append(f"scene: {q(a['scene'])}")
    lines.append(f"formed: {a['formed']}")
    if a.get("members"):
        lines.append("members:")
        for slug, role in a["members"]:
            lines += [f"  - slug: {slug}", f"    role: {q(role)}"]
    if a.get("albums"):
        lines.append("albums:")
        for alb in a["albums"]:
            lines += [f"  - slug: {q(alb['slug'])}",
                      f"    title: {q(alb['title'])}",
                      f"    year: {alb['year']}"]
    lines.append("---")
    return "\n".join(lines) + "\n"


def gen_album(alb, artist_slug):
    lines = ["---", f"title: {q(alb['title'])}", f"slug: {q(alb['slug'])}",
             f"artist: {artist_slug}", f"year: {alb['year']}",
             f"producer: {alb['producer']}", "songs:"]
    for s_slug, s_title in alb["songs"]:
        lines += [f"  - slug: {q(s_slug)}", f"    title: {q(s_title)}"]
    lines.append("---")
    return "\n".join(lines) + "\n"


def gen_song(slug, title, artist_slug, album_slug, year, credits):
    lines = ["---", f"title: {q(title)}", f"slug: {q(slug)}",
             f"artist: {artist_slug}", f"album: {q(album_slug)}",
             f"year: {year}", "credits:"]
    for p_slug, role in credits:
        lines += [f"  - person_slug: {p_slug}", f"    role: {q(role)}"]
    lines.append("---")
    return "\n".join(lines) + "\n"


def gen_person(slug, title, bands, song_credits_list):
    lines = ["---", f"title: {q(title)}", f"slug: {slug}"]
    if bands:
        lines.append("bands:")
        for b_slug, role in bands:
            lines += [f"  - slug: {b_slug}", f"    role: {q(role)}"]
    if song_credits_list:
        lines.append("song_credits:")
        for s_slug, s_title, credit in song_credits_list[:20]:
            lines += [f"  - slug: {q(s_slug)}", f"    title: {q(s_title)}",
                      f"    credit: {q(credit)}"]
    lines.append("---")
    return "\n".join(lines) + "\n"


# ============================================================
# MAIN
# ============================================================

def main():
    processed_songs = set()

    for artist in ARTIST_DATA:
        a_slug = artist["slug"]

        # Artist file
        wf(CONTENT / "artists" / f"{a_slug}.md", gen_artist(artist))

        for alb in artist["albums"]:
            alb_slug = alb["slug"]

            # Album file
            wf(CONTENT / "albums" / f"{alb_slug}.md", gen_album(alb, a_slug))

            # Song files
            for s_slug, s_title in alb["songs"]:
                if s_slug in processed_songs:
                    continue
                processed_songs.add(s_slug)

                credits = []
                for w in alb["writers"]:
                    credits.append((w, "Writer"))
                    PERSON_CREDITS[w].append((s_slug, s_title, "Writer"))
                credits.append((alb["producer"], "Producer"))
                PERSON_CREDITS[alb["producer"]].append((s_slug, s_title, "Producer"))

                wf(CONTENT / "songs" / f"{s_slug}.md",
                   gen_song(s_slug, s_title, a_slug, alb_slug, alb["year"], credits))

    # People files
    for slug, title, bands in PEOPLE_DATA:
        sc = PERSON_CREDITS.get(slug, [])
        wf(CONTENT / "people" / f"{slug}.md", gen_person(slug, title, bands, sc))

    print(f"\nDone! Created: {created_count}  |  Skipped (already exist): {skipped_count}")
    print(f"Artists: {len(ARTIST_DATA)}")
    total_albums = sum(len(a["albums"]) for a in ARTIST_DATA)
    total_songs = len(processed_songs)
    print(f"Albums:  {total_albums}")
    print(f"Songs:   {total_songs}")
    print(f"People:  {len(PEOPLE_DATA)}")


if __name__ == "__main__":
    main()
