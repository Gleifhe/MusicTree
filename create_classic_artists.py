#!/usr/bin/env python3
"""
Create classic 80s/90s artists content for MusicTree (U2, The Police, Depeche Mode, etc.).
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
# PER-SONG CREDITS: song_slug -> [(person_slug, role), ...]
# ============================================================
SONG_CREDITS = {
    # U2
    "sunday-bloody-sunday-u2": [("bono", "Writer"), ("steve-lillywhite", "Producer")],
    "new-years-day-u2": [("bono", "Writer"), ("steve-lillywhite", "Producer")],
    "pride-u2": [("bono", "Writer"), ("brian-eno", "Producer"), ("daniel-lanois", "Producer")],
    "with-or-without-you-u2": [("bono", "Writer"), ("brian-eno", "Producer"), ("daniel-lanois", "Producer")],
    "where-the-streets-have-no-name-u2": [("the-edge", "Writer"), ("brian-eno", "Producer"), ("daniel-lanois", "Producer")],
    "i-still-havent-found-u2": [("bono", "Writer"), ("brian-eno", "Producer"), ("daniel-lanois", "Producer")],
    "one-u2": [("bono", "Writer"), ("daniel-lanois", "Producer")],
    "mysterious-ways-u2": [("bono", "Writer"), ("daniel-lanois", "Producer")],
    "beautiful-day-u2": [("bono", "Writer"), ("daniel-lanois", "Producer")],
    # The Police
    "roxanne-pol": [("sting", "Writer"), ("nigel-gray", "Producer")],
    "message-in-a-bottle-pol": [("sting", "Writer"), ("nigel-gray", "Producer")],
    "dont-stand-so-close-pol": [("sting", "Writer"), ("nigel-gray", "Producer")],
    "every-little-thing-pol": [("sting", "Writer"), ("hugh-padgham", "Producer")],
    "invisible-sun-pol": [("sting", "Writer"), ("hugh-padgham", "Producer")],
    "every-breath-you-take-pol": [("sting", "Writer"), ("hugh-padgham", "Producer")],
    "wrapped-around-your-finger-pol": [("sting", "Writer"), ("hugh-padgham", "Producer")],
    "king-of-pain-pol": [("sting", "Writer"), ("hugh-padgham", "Producer")],
    "de-do-do-do-pol": [("sting", "Writer"), ("nigel-gray", "Producer")],
    # Depeche Mode
    "just-cant-get-enough-dm": [("vince-clarke", "Writer"), ("daniel-miller", "Producer")],
    "people-are-people-dm": [("martin-gore", "Writer"), ("daniel-miller", "Producer")],
    "personal-jesus-dm": [("martin-gore", "Writer"), ("flood-producer", "Producer")],
    "policy-of-truth-dm": [("martin-gore", "Writer"), ("flood-producer", "Producer")],
    "enjoy-the-silence-dm": [("martin-gore", "Writer"), ("flood-producer", "Producer")],
    "master-and-servant-dm": [("martin-gore", "Writer"), ("daniel-miller", "Producer")],
    "never-let-me-down-dm": [("martin-gore", "Writer"), ("alan-wilder", "Producer")],
    "everything-counts-dm": [("martin-gore", "Writer"), ("daniel-miller", "Producer")],
    "i-feel-you-dm": [("martin-gore", "Writer"), ("flood-producer", "Producer")],
    # New Order
    "blue-monday-no": [("bernard-sumner", "Writer"), ("peter-hook", "Writer")],
    "true-faith-no": [("bernard-sumner", "Writer"), ("stephen-hague", "Producer")],
    "bizarre-love-triangle-no": [("bernard-sumner", "Writer"), ("peter-hook", "Writer")],
    "age-of-consent-no": [("bernard-sumner", "Writer"), ("peter-hook", "Writer")],
    "ceremony-no": [("bernard-sumner", "Writer"), ("peter-hook", "Writer")],
    "regret-no": [("bernard-sumner", "Writer"), ("stephen-hague", "Producer")],
    "temptation-no": [("bernard-sumner", "Writer"), ("peter-hook", "Writer")],
    # The Cure
    "boys-dont-cry-cure": [("robert-smith-cure", "Writer"), ("mike-hedges", "Producer")],
    "a-forest-cure": [("robert-smith-cure", "Writer"), ("mike-hedges", "Producer")],
    "in-between-days-cure": [("robert-smith-cure", "Writer"), ("robert-smith-cure", "Producer")],
    "close-to-me-cure": [("robert-smith-cure", "Writer"), ("robert-smith-cure", "Producer")],
    "why-cant-i-be-you-cure": [("robert-smith-cure", "Writer"), ("robert-smith-cure", "Producer")],
    "lovesong-cure": [("robert-smith-cure", "Writer"), ("robert-smith-cure", "Producer")],
    "lullaby-cure": [("robert-smith-cure", "Writer"), ("robert-smith-cure", "Producer")],
    "pictures-of-you-cure": [("robert-smith-cure", "Writer"), ("robert-smith-cure", "Producer")],
    "friday-im-in-love-cure": [("robert-smith-cure", "Writer"), ("mark-stent", "Producer")],
    # The Smiths
    "this-charming-man-smi": [("morrissey", "Writer"), ("johnny-marr", "Writer"), ("john-porter", "Producer")],
    "there-is-a-light-smi": [("morrissey", "Writer"), ("johnny-marr", "Writer"), ("stephen-street", "Producer")],
    "how-soon-is-now-smi": [("morrissey", "Writer"), ("johnny-marr", "Writer"), ("john-porter", "Producer")],
    "what-difference-does-it-make-smi": [("morrissey", "Writer"), ("johnny-marr", "Writer"), ("john-porter", "Producer")],
    "heaven-knows-smi": [("morrissey", "Writer"), ("johnny-marr", "Writer"), ("john-porter", "Producer")],
    "panic-smi": [("morrissey", "Writer"), ("johnny-marr", "Writer"), ("stephen-street", "Producer")],
    "boy-with-thorn-smi": [("morrissey", "Writer"), ("johnny-marr", "Writer"), ("stephen-street", "Producer")],
    "girlfriend-in-a-coma-smi": [("morrissey", "Writer"), ("johnny-marr", "Writer"), ("stephen-street", "Producer")],
    "ask-smi": [("morrissey", "Writer"), ("johnny-marr", "Writer"), ("stephen-street", "Producer")],
    # Talking Heads
    "psycho-killer-th": [("david-byrne", "Writer"), ("chris-frantz", "Writer")],
    "once-in-a-lifetime-th": [("david-byrne", "Writer"), ("brian-eno", "Producer")],
    "burning-down-the-house-th": [("david-byrne", "Writer"), ("chris-frantz", "Writer")],
    "life-during-wartime-th": [("david-byrne", "Writer"), ("brian-eno", "Producer")],
    "this-must-be-the-place-th": [("david-byrne", "Writer"), ("chris-frantz", "Writer"), ("david-byrne", "Producer")],
    "road-to-nowhere-th": [("david-byrne", "Writer"), ("david-byrne", "Producer")],
    "wild-wild-life-th": [("david-byrne", "Writer"), ("david-byrne", "Producer")],
    # INXS
    "need-you-tonight-inxs": [("michael-hutchence", "Writer"), ("andrew-farriss", "Writer"), ("chris-thomas-inxs", "Producer")],
    "never-tear-us-apart-inxs": [("andrew-farriss", "Writer"), ("michael-hutchence", "Writer"), ("chris-thomas-inxs", "Producer")],
    "devil-inside-inxs": [("andrew-farriss", "Writer"), ("michael-hutchence", "Writer"), ("chris-thomas-inxs", "Producer")],
    "new-sensation-inxs": [("andrew-farriss", "Writer"), ("michael-hutchence", "Writer"), ("chris-thomas-inxs", "Producer")],
    "what-you-need-inxs": [("andrew-farriss", "Writer"), ("michael-hutchence", "Writer"), ("chris-thomas-inxs", "Producer")],
    "mystify-inxs": [("michael-hutchence", "Writer"), ("andrew-farriss", "Writer"), ("chris-thomas-inxs", "Producer")],
    "the-one-thing-inxs": [("andrew-farriss", "Writer"), ("michael-hutchence", "Writer"), ("mark-opitz", "Producer")],
    "dont-change-inxs": [("andrew-farriss", "Writer"), ("michael-hutchence", "Writer"), ("mark-opitz", "Producer")],
    "beautiful-girl-inxs": [("andrew-farriss", "Writer"), ("michael-hutchence", "Writer"), ("chris-thomas-inxs", "Producer")],
    # Eurythmics
    "sweet-dreams-eur": [("annie-lennox", "Writer"), ("dave-stewart", "Writer"), ("dave-stewart", "Producer")],
    "here-comes-the-rain-eur": [("annie-lennox", "Writer"), ("dave-stewart", "Writer"), ("dave-stewart", "Producer")],
    "would-i-lie-to-you-eur": [("annie-lennox", "Writer"), ("dave-stewart", "Writer"), ("dave-stewart", "Producer")],
    "there-must-be-an-angel-eur": [("annie-lennox", "Writer"), ("dave-stewart", "Writer"), ("dave-stewart", "Producer")],
    "sisters-are-doin-it-eur": [("annie-lennox", "Writer"), ("dave-stewart", "Writer"), ("dave-stewart", "Producer")],
    "thorn-in-my-side-eur": [("annie-lennox", "Writer"), ("dave-stewart", "Writer"), ("dave-stewart", "Producer")],
    "missionary-man-eur": [("annie-lennox", "Writer"), ("dave-stewart", "Writer"), ("dave-stewart", "Producer")],
    # Tears for Fears
    "mad-world-tff": [("roland-orzabal", "Writer"), ("chris-hughes-tff", "Producer")],
    "pale-shelter-tff": [("roland-orzabal", "Writer"), ("chris-hughes-tff", "Producer")],
    "everybody-wants-to-rule-tff": [("roland-orzabal", "Writer"), ("curt-smith-tff", "Writer"), ("chris-hughes-tff", "Producer")],
    "shout-tff": [("roland-orzabal", "Writer"), ("curt-smith-tff", "Writer"), ("chris-hughes-tff", "Producer")],
    "head-over-heels-tff": [("roland-orzabal", "Writer"), ("chris-hughes-tff", "Producer")],
    "sowing-the-seeds-tff": [("roland-orzabal", "Writer"), ("curt-smith-tff", "Writer"), ("roland-orzabal", "Producer")],
    "woman-in-chains-tff": [("roland-orzabal", "Writer"), ("roland-orzabal", "Producer")],
    # Duran Duran
    "hungry-like-the-wolf-dd": [("simon-le-bon", "Writer"), ("nick-rhodes", "Writer"), ("colin-thurston", "Producer")],
    "girls-on-film-dd": [("simon-le-bon", "Writer"), ("nick-rhodes", "Writer"), ("colin-thurston", "Producer")],
    "rio-song-dd": [("simon-le-bon", "Writer"), ("nick-rhodes", "Writer"), ("colin-thurston", "Producer")],
    "is-there-something-dd": [("simon-le-bon", "Writer"), ("nick-rhodes", "Writer"), ("alex-sadkin", "Producer")],
    "the-reflex-dd": [("simon-le-bon", "Writer"), ("nick-rhodes", "Writer"), ("alex-sadkin", "Producer")],
    "the-wild-boys-dd": [("simon-le-bon", "Writer"), ("nick-rhodes", "Writer"), ("alex-sadkin", "Producer")],
    "notorious-song-dd": [("simon-le-bon", "Writer"), ("nick-rhodes", "Writer"), ("nile-rodgers", "Producer")],
    "ordinary-world-dd": [("simon-le-bon", "Writer"), ("nick-rhodes", "Writer"), ("john-taylor-dd", "Producer")],
    "come-undone-dd": [("simon-le-bon", "Writer"), ("nick-rhodes", "Writer"), ("john-taylor-dd", "Producer")],
    # David Bowie
    "heroes-bowie-song": [("david-bowie-person", "Writer"), ("brian-eno", "Writer"), ("tony-visconti", "Producer")],
    "life-on-mars-bowie": [("david-bowie-person", "Writer"), ("david-bowie-person", "Producer")],
    "ziggy-stardust-bowie": [("david-bowie-person", "Writer"), ("david-bowie-person", "Producer")],
    "changes-bowie": [("david-bowie-person", "Writer"), ("david-bowie-person", "Producer")],
    "lets-dance-bowie-song": [("david-bowie-person", "Writer"), ("nile-rodgers", "Producer")],
    "modern-love-bowie": [("david-bowie-person", "Writer"), ("nile-rodgers", "Producer")],
    "rebel-rebel-bowie": [("david-bowie-person", "Writer"), ("david-bowie-person", "Producer")],
    "space-oddity-bowie": [("david-bowie-person", "Writer"), ("tony-visconti", "Producer")],
    "fame-bowie": [("david-bowie-person", "Writer"), ("david-bowie-person", "Producer")],
    "china-girl-bowie": [("david-bowie-person", "Writer"), ("nile-rodgers", "Producer")],
    "golden-years-bowie": [("david-bowie-person", "Writer"), ("david-bowie-person", "Producer")],
    # Michael Jackson
    "thriller-mj": [("michael-jackson-person", "Writer"), ("quincy-jones", "Producer")],
    "billie-jean-mj": [("michael-jackson-person", "Writer"), ("quincy-jones", "Producer")],
    "beat-it-mj": [("michael-jackson-person", "Writer"), ("quincy-jones", "Producer")],
    "wanna-be-startin-mj": [("michael-jackson-person", "Writer"), ("quincy-jones", "Producer")],
    "man-in-the-mirror-mj": [("michael-jackson-person", "Writer"), ("quincy-jones", "Producer")],
    "smooth-criminal-mj": [("michael-jackson-person", "Writer"), ("quincy-jones", "Producer")],
    "black-or-white-mj": [("michael-jackson-person", "Writer"), ("teddy-riley", "Producer")],
    "bad-song-mj": [("michael-jackson-person", "Writer"), ("quincy-jones", "Producer")],
    "rock-with-you-mj": [("michael-jackson-person", "Writer"), ("quincy-jones", "Producer")],
    "dont-stop-til-you-get-enough-mj": [("michael-jackson-person", "Writer"), ("quincy-jones", "Producer")],
    "human-nature-mj": [("michael-jackson-person", "Writer"), ("quincy-jones", "Producer")],
    # Prince
    "purple-rain-prince": [("prince-person", "Writer"), ("prince-person", "Producer")],
    "when-doves-cry-prince": [("prince-person", "Writer"), ("prince-person", "Producer")],
    "little-red-corvette-prince": [("prince-person", "Writer"), ("prince-person", "Producer")],
    "1999-prince-song": [("prince-person", "Writer"), ("prince-person", "Producer")],
    "lets-go-crazy-prince": [("prince-person", "Writer"), ("prince-person", "Producer")],
    "kiss-prince": [("prince-person", "Writer"), ("prince-person", "Producer")],
    "sign-o-the-times-prince": [("prince-person", "Writer"), ("prince-person", "Producer")],
    "raspberry-beret-prince": [("prince-person", "Writer"), ("prince-person", "Producer")],
    "i-would-die-4-u-prince": [("prince-person", "Writer"), ("prince-person", "Producer")],
    "baby-im-a-star-prince": [("prince-person", "Writer"), ("prince-person", "Producer")],
    # Madonna
    "like-a-virgin-mad": [("madonna-person", "Writer"), ("nile-rodgers", "Producer")],
    "material-girl-mad": [("madonna-person", "Writer"), ("nile-rodgers", "Producer")],
    "holiday-mad": [("madonna-person", "Writer"), ("madonna-person", "Producer")],
    "like-a-prayer-mad": [("madonna-person", "Writer"), ("patrick-leonard", "Producer")],
    "express-yourself-mad": [("madonna-person", "Writer"), ("patrick-leonard", "Producer")],
    "vogue-mad": [("madonna-person", "Writer"), ("madonna-person", "Producer")],
    "papa-dont-preach-mad": [("madonna-person", "Writer"), ("madonna-person", "Producer")],
    "open-your-heart-mad": [("madonna-person", "Writer"), ("madonna-person", "Producer")],
    "la-isla-bonita-mad": [("madonna-person", "Writer"), ("madonna-person", "Producer")],
    "ray-of-light-mad": [("madonna-person", "Writer"), ("william-orbit", "Producer")],
    "frozen-mad": [("madonna-person", "Writer"), ("william-orbit", "Producer")],
    # a-ha
    "take-on-me-aha": [("morten-harket", "Writer"), ("paul-waaktaar-savoy", "Writer"), ("alan-tarney", "Producer")],
    "the-sun-always-shines-aha": [("paul-waaktaar-savoy", "Writer"), ("alan-tarney", "Producer")],
    "train-of-thought-aha": [("paul-waaktaar-savoy", "Writer"), ("alan-tarney", "Producer")],
    "manhattan-skyline-aha": [("paul-waaktaar-savoy", "Writer"), ("alan-tarney", "Producer")],
    "crying-in-the-rain-aha": [("paul-waaktaar-savoy", "Writer"), ("morten-harket", "Writer"), ("alan-tarney", "Producer")],
    # The B-52s
    "rock-lobster-b52": [("fred-schneider", "Writer"), ("keith-strickland", "Writer")],
    "love-shack-b52": [("fred-schneider", "Writer"), ("kate-pierson", "Writer"), ("don-was", "Producer")],
    "roam-b52": [("kate-pierson", "Writer"), ("cindy-wilson", "Writer"), ("don-was", "Producer")],
    "quiche-lorraine-b52": [("fred-schneider", "Writer"), ("keith-strickland", "Writer")],
    "private-idaho-b52": [("fred-schneider", "Writer"), ("keith-strickland", "Writer")],
    "planet-claire-b52": [("fred-schneider", "Writer"), ("keith-strickland", "Writer")],
    # The Pretenders
    "brass-in-pocket-pre": [("chrissie-hynde", "Writer"), ("james-honeyman-scott", "Writer"), ("chris-thomas-inxs", "Producer")],
    "talk-of-the-town-pre": [("chrissie-hynde", "Writer"), ("chris-thomas-inxs", "Producer")],
    "back-on-the-chain-gang-pre": [("chrissie-hynde", "Writer"), ("chris-thomas-inxs", "Producer")],
    "ill-stand-by-you-pre": [("chrissie-hynde", "Writer"), ("chrissie-hynde", "Producer")],
    "dont-get-me-wrong-pre": [("chrissie-hynde", "Writer"), ("jimmy-iovine", "Producer")],
    "middle-of-the-road-pre": [("chrissie-hynde", "Writer"), ("chris-thomas-inxs", "Producer")],
    "2000-miles-pre": [("chrissie-hynde", "Writer"), ("chris-thomas-inxs", "Producer")],
    # Pet Shop Boys
    "west-end-girls-psb": [("neil-tennant", "Writer"), ("chris-lowe", "Writer"), ("stephen-hague", "Producer")],
    "its-a-sin-psb": [("neil-tennant", "Writer"), ("chris-lowe", "Writer"), ("neil-tennant", "Producer")],
    "always-on-my-mind-psb": [("neil-tennant", "Writer"), ("chris-lowe", "Writer"), ("neil-tennant", "Producer")],
    "what-have-i-done-psb": [("neil-tennant", "Writer"), ("chris-lowe", "Writer"), ("neil-tennant", "Producer")],
    "opportunities-psb": [("neil-tennant", "Writer"), ("chris-lowe", "Writer"), ("stephen-hague", "Producer")],
    "go-west-psb": [("neil-tennant", "Writer"), ("chris-lowe", "Writer"), ("neil-tennant", "Producer")],
    "being-boring-psb": [("neil-tennant", "Writer"), ("chris-lowe", "Writer"), ("neil-tennant", "Producer")],
    "left-to-my-own-devices-psb": [("neil-tennant", "Writer"), ("chris-lowe", "Writer"), ("neil-tennant", "Producer")],
    # Simple Minds
    "dont-you-forget-about-me-sm": [("jim-kerr", "Writer"), ("charlie-burchill", "Writer"), ("keith-forsey", "Producer")],
    "alive-and-kicking-sm": [("jim-kerr", "Writer"), ("charlie-burchill", "Writer"), ("jimmy-iovine", "Producer")],
    "sanctify-yourself-sm": [("jim-kerr", "Writer"), ("charlie-burchill", "Writer"), ("jimmy-iovine", "Producer")],
    "all-the-things-she-said-sm": [("jim-kerr", "Writer"), ("charlie-burchill", "Writer"), ("jim-kerr", "Producer")],
    "waterfront-sm": [("jim-kerr", "Writer"), ("charlie-burchill", "Writer"), ("steve-hillage", "Producer")],
    "up-on-the-catwalk-sm": [("jim-kerr", "Writer"), ("charlie-burchill", "Writer"), ("steve-hillage", "Producer")],
    # Blondie
    "heart-of-glass-blo": [("debbie-harry", "Writer"), ("chris-stein", "Writer"), ("mike-chapman-prod", "Producer")],
    "call-me-blo": [("debbie-harry", "Writer"), ("giorgio-moroder", "Producer")],
    "rapture-blo": [("debbie-harry", "Writer"), ("chris-stein", "Writer"), ("mike-chapman-prod", "Producer")],
    "the-tide-is-high-blo": [("debbie-harry", "Writer"), ("mike-chapman-prod", "Producer")],
    "atomic-blo": [("debbie-harry", "Writer"), ("chris-stein", "Writer"), ("mike-chapman-prod", "Producer")],
    "one-way-or-another-blo": [("debbie-harry", "Writer"), ("mike-chapman-prod", "Producer")],
    "dreaming-blo": [("debbie-harry", "Writer"), ("chris-stein", "Writer"), ("mike-chapman-prod", "Producer")],
    "hanging-on-the-telephone-blo": [("debbie-harry", "Writer"), ("mike-chapman-prod", "Producer")],
    # Cyndi Lauper
    "girls-just-want-to-have-fun-cl": [("cyndi-lauper-person", "Writer"), ("rick-chertoff", "Producer")],
    "time-after-time-cl": [("cyndi-lauper-person", "Writer"), ("rick-chertoff", "Producer")],
    "she-bop-cl": [("cyndi-lauper-person", "Writer"), ("rick-chertoff", "Producer")],
    "true-colors-cl": [("cyndi-lauper-person", "Writer"), ("rick-chertoff", "Producer")],
    "i-drove-all-night-cl": [("cyndi-lauper-person", "Writer"), ("rick-chertoff", "Producer")],
    "change-of-heart-cl": [("cyndi-lauper-person", "Writer"), ("rick-chertoff", "Producer")],
    # Billy Idol
    "white-wedding-bi": [("billy-idol-person", "Writer"), ("keith-forsey", "Producer")],
    "rebel-yell-bi": [("billy-idol-person", "Writer"), ("steve-stevens", "Writer"), ("keith-forsey", "Producer")],
    "eyes-without-a-face-bi": [("billy-idol-person", "Writer"), ("keith-forsey", "Producer")],
    "flesh-for-fantasy-bi": [("billy-idol-person", "Writer"), ("keith-forsey", "Producer")],
    "mony-mony-bi": [("billy-idol-person", "Writer"), ("keith-forsey", "Producer")],
    "cradle-of-love-bi": [("billy-idol-person", "Writer"), ("keith-forsey", "Producer")],
    # Tracy Chapman
    "fast-car-tc": [("tracy-chapman-person", "Writer"), ("david-kershenbaum", "Producer")],
    "give-me-one-reason-tc": [("tracy-chapman-person", "Writer"), ("tracy-chapman-person", "Producer")],
    "talkin-bout-a-revolution-tc": [("tracy-chapman-person", "Writer"), ("david-kershenbaum", "Producer")],
    "baby-can-i-hold-you-tc": [("tracy-chapman-person", "Writer"), ("david-kershenbaum", "Producer")],
    "the-promise-tc": [("tracy-chapman-person", "Writer"), ("tracy-chapman-person", "Producer")],
    "mountains-o-things-tc": [("tracy-chapman-person", "Writer"), ("david-kershenbaum", "Producer")],
    # Sinead O'Connor
    "nothing-compares-2-u-soc": [("sinead-oconnor-person", "Writer"), ("sinead-oconnor-person", "Producer")],
    "mandinka-soc": [("sinead-oconnor-person", "Writer"), ("nigel-grainge", "Producer")],
    "troy-soc": [("sinead-oconnor-person", "Writer"), ("nigel-grainge", "Producer")],
    "emperors-new-clothes-soc": [("sinead-oconnor-person", "Writer"), ("sinead-oconnor-person", "Producer")],
    "last-day-of-our-acquaintance-soc": [("sinead-oconnor-person", "Writer"), ("sinead-oconnor-person", "Producer")],
    "fire-on-babylon-soc": [("sinead-oconnor-person", "Writer"), ("sinead-oconnor-person", "Producer")],
}

# ============================================================
# ARTIST DATA
# Each album: slug, title, year, producer, songs: [(slug, title), ...]
# ============================================================
ARTIST_DATA = [
    # ==================== 1. U2 ====================
    {
        "slug": "u2", "title": "U2", "band_type": "Group",
        "genres": ["Rock"], "scene": "Rock", "formed": 1976,
        "members": [
            ("bono", "Vocals"), ("the-edge", "Guitar"),
            ("adam-clayton", "Bass"), ("larry-mullen-jr", "Drums"),
        ],
        "albums": [
            {"slug": "boy", "title": "Boy", "year": 1980,
             "producer": "steve-lillywhite", "songs": []},
            {"slug": "october-u2", "title": "October", "year": 1981,
             "producer": "steve-lillywhite", "songs": []},
            {"slug": "war-u2", "title": "War", "year": 1983,
             "producer": "steve-lillywhite", "songs": [
                 ("sunday-bloody-sunday-u2", "Sunday Bloody Sunday"),
                 ("new-years-day-u2", "New Year's Day"),
             ]},
            {"slug": "the-unforgettable-fire", "title": "The Unforgettable Fire", "year": 1984,
             "producer": "brian-eno", "songs": [
                 ("pride-u2", "Pride (In the Name of Love)"),
             ]},
            {"slug": "the-joshua-tree", "title": "The Joshua Tree", "year": 1987,
             "producer": "daniel-lanois", "songs": [
                 ("with-or-without-you-u2", "With or Without You"),
                 ("where-the-streets-have-no-name-u2", "Where the Streets Have No Name"),
                 ("i-still-havent-found-u2", "I Still Haven't Found What I'm Looking For"),
             ]},
            {"slug": "rattle-and-hum", "title": "Rattle and Hum", "year": 1988,
             "producer": "daniel-lanois", "songs": []},
            {"slug": "achtung-baby", "title": "Achtung Baby", "year": 1991,
             "producer": "daniel-lanois", "songs": [
                 ("one-u2", "One"),
                 ("mysterious-ways-u2", "Mysterious Ways"),
             ]},
            {"slug": "zooropa", "title": "Zooropa", "year": 1993,
             "producer": "flood-producer", "songs": []},
            {"slug": "pop-u2", "title": "Pop", "year": 1997,
             "producer": "flood-producer", "songs": []},
            {"slug": "all-that-you-cant-leave-behind", "title": "All That You Can't Leave Behind", "year": 2000,
             "producer": "daniel-lanois", "songs": [
                 ("beautiful-day-u2", "Beautiful Day"),
             ]},
        ],
    },

    # ==================== 2. THE POLICE ====================
    {
        "slug": "the-police", "title": "The Police", "band_type": "Group",
        "genres": ["Rock"], "scene": "Rock", "formed": 1977, "disbanded": 1986,
        "members": [
            ("sting", "Vocals/Bass"), ("andy-summers", "Guitar"),
            ("stewart-copeland", "Drums"),
        ],
        "albums": [
            {"slug": "outlandos-damour", "title": "Outlandos d'Amour", "year": 1978,
             "producer": "nigel-gray", "songs": [
                 ("roxanne-pol", "Roxanne"),
             ]},
            {"slug": "reggatta-de-blanc", "title": "Reggatta de Blanc", "year": 1979,
             "producer": "nigel-gray", "songs": [
                 ("message-in-a-bottle-pol", "Message in a Bottle"),
             ]},
            {"slug": "zenyatta-mondatta", "title": "Zenyatta Mondatta", "year": 1980,
             "producer": "nigel-gray", "songs": [
                 ("dont-stand-so-close-pol", "Don't Stand So Close to Me"),
                 ("de-do-do-do-pol", "De Do Do Do De Da Da Da"),
             ]},
            {"slug": "ghost-in-the-machine", "title": "Ghost in the Machine", "year": 1981,
             "producer": "hugh-padgham", "songs": [
                 ("every-little-thing-pol", "Every Little Thing She Does Is Magic"),
                 ("invisible-sun-pol", "Invisible Sun"),
             ]},
            {"slug": "synchronicity", "title": "Synchronicity", "year": 1983,
             "producer": "hugh-padgham", "songs": [
                 ("every-breath-you-take-pol", "Every Breath You Take"),
                 ("wrapped-around-your-finger-pol", "Wrapped Around Your Finger"),
                 ("king-of-pain-pol", "King of Pain"),
             ]},
        ],
    },

    # ==================== 3. DEPECHE MODE ====================
    {
        "slug": "depeche-mode", "title": "Depeche Mode", "band_type": "Group",
        "genres": ["Electronic"], "scene": "London UK", "formed": 1980,
        "members": [
            ("dave-gahan", "Vocals"), ("martin-gore", "Guitar/Keyboards/Vocals"),
            ("andrew-fletcher", "Keyboards"), ("alan-wilder", "Keyboards"),
            ("vince-clarke", "Keyboards"),
        ],
        "albums": [
            {"slug": "speak-and-spell", "title": "Speak and Spell", "year": 1981,
             "producer": "daniel-miller", "songs": [
                 ("just-cant-get-enough-dm", "Just Can't Get Enough"),
             ]},
            {"slug": "a-broken-frame", "title": "A Broken Frame", "year": 1982,
             "producer": "daniel-miller", "songs": []},
            {"slug": "construction-time-again", "title": "Construction Time Again", "year": 1983,
             "producer": "daniel-miller", "songs": [
                 ("everything-counts-dm", "Everything Counts"),
             ]},
            {"slug": "some-great-reward", "title": "Some Great Reward", "year": 1984,
             "producer": "daniel-miller", "songs": [
                 ("people-are-people-dm", "People Are People"),
                 ("master-and-servant-dm", "Master and Servant"),
             ]},
            {"slug": "black-celebration", "title": "Black Celebration", "year": 1986,
             "producer": "daniel-miller", "songs": []},
            {"slug": "music-for-the-masses", "title": "Music for the Masses", "year": 1987,
             "producer": "alan-wilder", "songs": [
                 ("never-let-me-down-dm", "Never Let Me Down Again"),
             ]},
            {"slug": "violator", "title": "Violator", "year": 1990,
             "producer": "flood-producer", "songs": [
                 ("personal-jesus-dm", "Personal Jesus"),
                 ("policy-of-truth-dm", "Policy of Truth"),
                 ("enjoy-the-silence-dm", "Enjoy the Silence"),
             ]},
            {"slug": "songs-of-faith-and-devotion", "title": "Songs of Faith and Devotion", "year": 1993,
             "producer": "flood-producer", "songs": [
                 ("i-feel-you-dm", "I Feel You"),
             ]},
            {"slug": "ultra-dm", "title": "Ultra", "year": 1997,
             "producer": "martin-gore", "songs": []},
        ],
    },

    # ==================== 4. NEW ORDER ====================
    {
        "slug": "new-order", "title": "New Order", "band_type": "Group",
        "genres": ["Alternative Rock"], "scene": "Alternative Rock", "formed": 1980,
        "members": [
            ("bernard-sumner", "Vocals/Guitar"), ("peter-hook", "Bass"),
            ("stephen-morris", "Drums"), ("gillian-gilbert", "Keyboards"),
        ],
        "albums": [
            {"slug": "movement-no", "title": "Movement", "year": 1981,
             "producer": "bernard-sumner", "songs": [
                 ("ceremony-no", "Ceremony"),
             ]},
            {"slug": "power-corruption-and-lies", "title": "Power Corruption and Lies", "year": 1983,
             "producer": "bernard-sumner", "songs": [
                 ("blue-monday-no", "Blue Monday"),
                 ("age-of-consent-no", "Age of Consent"),
                 ("temptation-no", "Temptation"),
             ]},
            {"slug": "low-life", "title": "Low-Life", "year": 1985,
             "producer": "bernard-sumner", "songs": []},
            {"slug": "brotherhood-no", "title": "Brotherhood", "year": 1986,
             "producer": "bernard-sumner", "songs": [
                 ("bizarre-love-triangle-no", "Bizarre Love Triangle"),
             ]},
            {"slug": "technique", "title": "Technique", "year": 1989,
             "producer": "bernard-sumner", "songs": []},
            {"slug": "republic-no", "title": "Republic", "year": 1993,
             "producer": "stephen-hague", "songs": [
                 ("regret-no", "Regret"),
                 ("true-faith-no", "True Faith"),
             ]},
        ],
    },

    # ==================== 5. THE CURE ====================
    {
        "slug": "the-cure", "title": "The Cure", "band_type": "Group",
        "genres": ["Alternative Rock"], "scene": "Alternative Rock", "formed": 1976,
        "members": [
            ("robert-smith-cure", "Vocals/Guitar"), ("lol-tolhurst", "Drums/Keyboards"),
            ("simon-gallup", "Bass"), ("porl-thompson", "Guitar"),
        ],
        "albums": [
            {"slug": "three-imaginary-boys", "title": "Three Imaginary Boys", "year": 1979,
             "producer": "mike-hedges", "songs": [
                 ("boys-dont-cry-cure", "Boys Don't Cry"),
             ]},
            {"slug": "seventeen-seconds", "title": "Seventeen Seconds", "year": 1980,
             "producer": "mike-hedges", "songs": [
                 ("a-forest-cure", "A Forest"),
             ]},
            {"slug": "faith-cure", "title": "Faith", "year": 1981,
             "producer": "mike-hedges", "songs": []},
            {"slug": "pornography-cure", "title": "Pornography", "year": 1982,
             "producer": "robert-smith-cure", "songs": []},
            {"slug": "the-head-on-the-door", "title": "The Head on the Door", "year": 1985,
             "producer": "robert-smith-cure", "songs": [
                 ("in-between-days-cure", "In Between Days"),
                 ("close-to-me-cure", "Close to Me"),
             ]},
            {"slug": "kiss-me-kiss-me-kiss-me", "title": "Kiss Me Kiss Me Kiss Me", "year": 1987,
             "producer": "robert-smith-cure", "songs": [
                 ("why-cant-i-be-you-cure", "Why Can't I Be You?"),
             ]},
            {"slug": "disintegration", "title": "Disintegration", "year": 1989,
             "producer": "robert-smith-cure", "songs": [
                 ("lovesong-cure", "Lovesong"),
                 ("lullaby-cure", "Lullaby"),
                 ("pictures-of-you-cure", "Pictures of You"),
             ]},
            {"slug": "wish-cure", "title": "Wish", "year": 1992,
             "producer": "robert-smith-cure", "songs": [
                 ("friday-im-in-love-cure", "Friday I'm in Love"),
             ]},
        ],
    },

    # ==================== 6. THE SMITHS ====================
    {
        "slug": "the-smiths", "title": "The Smiths", "band_type": "Group",
        "genres": ["Alternative Rock"], "scene": "Alternative Rock", "formed": 1982, "disbanded": 1987,
        "members": [
            ("morrissey", "Vocals"), ("johnny-marr", "Guitar"),
            ("andy-rourke", "Bass"), ("mike-joyce-smiths", "Drums"),
        ],
        "albums": [
            {"slug": "the-smiths-album", "title": "The Smiths", "year": 1984,
             "producer": "john-porter", "songs": [
                 ("this-charming-man-smi", "This Charming Man"),
                 ("what-difference-does-it-make-smi", "What Difference Does It Make?"),
             ]},
            {"slug": "meat-is-murder", "title": "Meat Is Murder", "year": 1985,
             "producer": "john-porter", "songs": [
                 ("how-soon-is-now-smi", "How Soon Is Now?"),
                 ("heaven-knows-smi", "Heaven Knows I'm Miserable Now"),
             ]},
            {"slug": "the-queen-is-dead", "title": "The Queen Is Dead", "year": 1986,
             "producer": "stephen-street", "songs": [
                 ("there-is-a-light-smi", "There Is a Light That Never Goes Out"),
                 ("panic-smi", "Panic"),
                 ("boy-with-thorn-smi", "The Boy with the Thorn in His Side"),
             ]},
            {"slug": "strangeways-here-we-come", "title": "Strangeways Here We Come", "year": 1987,
             "producer": "stephen-street", "songs": [
                 ("girlfriend-in-a-coma-smi", "Girlfriend in a Coma"),
                 ("ask-smi", "Ask"),
             ]},
        ],
    },

    # ==================== 7. TALKING HEADS ====================
    {
        "slug": "talking-heads", "title": "Talking Heads", "band_type": "Group",
        "genres": ["Alternative Rock"], "scene": "Alternative Rock", "formed": 1975, "disbanded": 1991,
        "members": [
            ("david-byrne", "Vocals/Guitar"), ("chris-frantz", "Drums"),
            ("tina-weymouth", "Bass"), ("jerry-harrison", "Guitar/Keyboards"),
        ],
        "albums": [
            {"slug": "talking-heads-77", "title": "Talking Heads: 77", "year": 1977,
             "producer": "david-byrne", "songs": [
                 ("psycho-killer-th", "Psycho Killer"),
             ]},
            {"slug": "more-songs-about-buildings", "title": "More Songs About Buildings and Food", "year": 1978,
             "producer": "brian-eno", "songs": []},
            {"slug": "fear-of-music", "title": "Fear of Music", "year": 1979,
             "producer": "brian-eno", "songs": [
                 ("life-during-wartime-th", "Life During Wartime"),
             ]},
            {"slug": "remain-in-light", "title": "Remain in Light", "year": 1980,
             "producer": "brian-eno", "songs": [
                 ("once-in-a-lifetime-th", "Once in a Lifetime"),
             ]},
            {"slug": "speaking-in-tongues", "title": "Speaking in Tongues", "year": 1983,
             "producer": "david-byrne", "songs": [
                 ("burning-down-the-house-th", "Burning Down the House"),
                 ("this-must-be-the-place-th", "This Must Be the Place"),
             ]},
            {"slug": "little-creatures", "title": "Little Creatures", "year": 1985,
             "producer": "david-byrne", "songs": [
                 ("road-to-nowhere-th", "Road to Nowhere"),
             ]},
            {"slug": "true-stories-th", "title": "True Stories", "year": 1986,
             "producer": "david-byrne", "songs": [
                 ("wild-wild-life-th", "Wild Wild Life"),
             ]},
            {"slug": "naked-th", "title": "Naked", "year": 1988,
             "producer": "david-byrne", "songs": []},
        ],
    },

    # ==================== 8. INXS ====================
    {
        "slug": "inxs", "title": "INXS", "band_type": "Group",
        "genres": ["Alternative Rock"], "scene": "Alternative Rock", "formed": 1977,
        "members": [
            ("michael-hutchence", "Vocals"), ("andrew-farriss", "Keyboards/Guitar"),
            ("tim-farriss", "Guitar"), ("jon-farriss", "Drums"),
            ("garry-gary-beers", "Bass"), ("kirk-pengilly", "Guitar"),
        ],
        "albums": [
            {"slug": "shabooh-shoobah", "title": "Shabooh Shoobah", "year": 1982,
             "producer": "mark-opitz", "songs": [
                 ("the-one-thing-inxs", "The One Thing"),
                 ("dont-change-inxs", "Don't Change"),
             ]},
            {"slug": "the-swing", "title": "The Swing", "year": 1984,
             "producer": "mark-opitz", "songs": []},
            {"slug": "listen-like-thieves", "title": "Listen Like Thieves", "year": 1985,
             "producer": "chris-thomas-inxs", "songs": [
                 ("what-you-need-inxs", "What You Need"),
             ]},
            {"slug": "kick-inxs", "title": "Kick", "year": 1987,
             "producer": "chris-thomas-inxs", "songs": [
                 ("need-you-tonight-inxs", "Need You Tonight"),
                 ("never-tear-us-apart-inxs", "Never Tear Us Apart"),
                 ("devil-inside-inxs", "Devil Inside"),
                 ("new-sensation-inxs", "New Sensation"),
             ]},
            {"slug": "x-inxs", "title": "X", "year": 1990,
             "producer": "chris-thomas-inxs", "songs": [
                 ("mystify-inxs", "Mystify"),
             ]},
            {"slug": "welcome-to-wherever-you-are", "title": "Welcome to Wherever You Are", "year": 1992,
             "producer": "chris-thomas-inxs", "songs": [
                 ("beautiful-girl-inxs", "Beautiful Girl"),
             ]},
        ],
    },

    # ==================== 9. EURYTHMICS ====================
    {
        "slug": "eurythmics", "title": "Eurythmics", "band_type": "Group",
        "genres": ["Alternative Rock"], "scene": "Alternative Rock", "formed": 1980, "disbanded": 1990,
        "members": [
            ("annie-lennox", "Vocals"), ("dave-stewart", "Guitar/Keyboards"),
        ],
        "albums": [
            {"slug": "sweet-dreams-album", "title": "Sweet Dreams", "year": 1983,
             "producer": "dave-stewart", "songs": [
                 ("sweet-dreams-eur", "Sweet Dreams (Are Made of This)"),
             ]},
            {"slug": "touch-eurythmics", "title": "Touch", "year": 1983,
             "producer": "dave-stewart", "songs": [
                 ("here-comes-the-rain-eur", "Here Comes the Rain Again"),
             ]},
            {"slug": "be-yourself-tonight", "title": "Be Yourself Tonight", "year": 1985,
             "producer": "dave-stewart", "songs": [
                 ("would-i-lie-to-you-eur", "Would I Lie to You?"),
                 ("there-must-be-an-angel-eur", "There Must Be an Angel"),
                 ("sisters-are-doin-it-eur", "Sisters Are Doin' It for Themselves"),
             ]},
            {"slug": "revenge-eurythmics", "title": "Revenge", "year": 1986,
             "producer": "dave-stewart", "songs": [
                 ("thorn-in-my-side-eur", "Thorn in My Side"),
                 ("missionary-man-eur", "Missionary Man"),
             ]},
            {"slug": "savage-eurythmics", "title": "Savage", "year": 1987,
             "producer": "dave-stewart", "songs": []},
            {"slug": "we-too-are-one", "title": "We Too Are One", "year": 1989,
             "producer": "dave-stewart", "songs": []},
        ],
    },

    # ==================== 10. TEARS FOR FEARS ====================
    {
        "slug": "tears-for-fears", "title": "Tears for Fears", "band_type": "Group",
        "genres": ["Alternative Rock"], "scene": "Alternative Rock", "formed": 1981,
        "members": [
            ("roland-orzabal", "Vocals/Guitar"), ("curt-smith-tff", "Bass/Vocals"),
        ],
        "albums": [
            {"slug": "the-hurting", "title": "The Hurting", "year": 1983,
             "producer": "chris-hughes-tff", "songs": [
                 ("mad-world-tff", "Mad World"),
                 ("pale-shelter-tff", "Pale Shelter"),
             ]},
            {"slug": "songs-from-the-big-chair", "title": "Songs from the Big Chair", "year": 1985,
             "producer": "chris-hughes-tff", "songs": [
                 ("everybody-wants-to-rule-tff", "Everybody Wants to Rule the World"),
                 ("shout-tff", "Shout"),
                 ("head-over-heels-tff", "Head Over Heels"),
             ]},
            {"slug": "the-seeds-of-love", "title": "The Seeds of Love", "year": 1989,
             "producer": "roland-orzabal", "songs": [
                 ("sowing-the-seeds-tff", "Sowing the Seeds of Love"),
                 ("woman-in-chains-tff", "Woman in Chains"),
             ]},
            {"slug": "elemental-tff", "title": "Elemental", "year": 1993,
             "producer": "roland-orzabal", "songs": []},
        ],
    },

    # ==================== 11. DURAN DURAN ====================
    {
        "slug": "duran-duran", "title": "Duran Duran", "band_type": "Group",
        "genres": ["Alternative Rock"], "scene": "Alternative Rock", "formed": 1978,
        "members": [
            ("simon-le-bon", "Vocals"), ("nick-rhodes", "Keyboards"),
            ("john-taylor-dd", "Bass"), ("roger-taylor-dd", "Drums"),
            ("andy-taylor-dd", "Guitar"),
        ],
        "albums": [
            {"slug": "duran-duran-album", "title": "Duran Duran", "year": 1981,
             "producer": "colin-thurston", "songs": [
                 ("girls-on-film-dd", "Girls on Film"),
             ]},
            {"slug": "rio-dd", "title": "Rio", "year": 1982,
             "producer": "colin-thurston", "songs": [
                 ("hungry-like-the-wolf-dd", "Hungry Like the Wolf"),
                 ("rio-song-dd", "Rio"),
             ]},
            {"slug": "seven-and-the-ragged-tiger", "title": "Seven and the Ragged Tiger", "year": 1983,
             "producer": "alex-sadkin", "songs": [
                 ("is-there-something-dd", "Is There Something I Should Know?"),
                 ("the-reflex-dd", "The Reflex"),
             ]},
            {"slug": "arena-dd", "title": "Arena", "year": 1984,
             "producer": "alex-sadkin", "songs": [
                 ("the-wild-boys-dd", "The Wild Boys"),
             ]},
            {"slug": "notorious-dd", "title": "Notorious", "year": 1986,
             "producer": "nile-rodgers", "songs": [
                 ("notorious-song-dd", "Notorious"),
             ]},
            {"slug": "big-thing", "title": "Big Thing", "year": 1988,
             "producer": "john-taylor-dd", "songs": []},
            {"slug": "liberty-dd", "title": "Liberty", "year": 1990,
             "producer": "john-taylor-dd", "songs": []},
            {"slug": "duran-duran-93", "title": "Duran Duran", "year": 1993,
             "producer": "john-taylor-dd", "songs": [
                 ("ordinary-world-dd", "Ordinary World"),
                 ("come-undone-dd", "Come Undone"),
             ]},
        ],
    },

    # ==================== 12. DAVID BOWIE ====================
    {
        "slug": "david-bowie", "title": "David Bowie", "band_type": "Solo",
        "genres": ["Rock"], "scene": "Rock", "formed": 1962, "disbanded": 2016,
        "members": [],
        "albums": [
            {"slug": "ziggy-stardust", "title": "The Rise and Fall of Ziggy Stardust", "year": 1972,
             "producer": "david-bowie-person", "songs": [
                 ("ziggy-stardust-bowie", "Ziggy Stardust"),
                 ("changes-bowie", "Changes"),
                 ("space-oddity-bowie", "Space Oddity"),
             ]},
            {"slug": "aladdin-sane", "title": "Aladdin Sane", "year": 1973,
             "producer": "david-bowie-person", "songs": [
                 ("life-on-mars-bowie", "Life on Mars?"),
             ]},
            {"slug": "diamond-dogs", "title": "Diamond Dogs", "year": 1974,
             "producer": "david-bowie-person", "songs": [
                 ("rebel-rebel-bowie", "Rebel Rebel"),
             ]},
            {"slug": "young-americans", "title": "Young Americans", "year": 1975,
             "producer": "david-bowie-person", "songs": [
                 ("fame-bowie", "Fame"),
             ]},
            {"slug": "station-to-station", "title": "Station to Station", "year": 1976,
             "producer": "david-bowie-person", "songs": [
                 ("golden-years-bowie", "Golden Years"),
             ]},
            {"slug": "heroes-bowie", "title": "Heroes", "year": 1977,
             "producer": "tony-visconti", "songs": [
                 ("heroes-bowie-song", "Heroes"),
             ]},
            {"slug": "scary-monsters", "title": "Scary Monsters", "year": 1980,
             "producer": "tony-visconti", "songs": []},
            {"slug": "lets-dance", "title": "Let's Dance", "year": 1983,
             "producer": "nile-rodgers", "songs": [
                 ("lets-dance-bowie-song", "Let's Dance"),
                 ("modern-love-bowie", "Modern Love"),
                 ("china-girl-bowie", "China Girl"),
             ]},
            {"slug": "never-let-me-down-bowie", "title": "Never Let Me Down", "year": 1987,
             "producer": "david-bowie-person", "songs": []},
            {"slug": "black-tie-white-noise", "title": "Black Tie White Noise", "year": 1993,
             "producer": "nile-rodgers", "songs": []},
            {"slug": "outside-bowie", "title": "Outside", "year": 1995,
             "producer": "brian-eno", "songs": []},
            {"slug": "heathen-bowie", "title": "Heathen", "year": 2002,
             "producer": "tony-visconti", "songs": []},
            {"slug": "the-next-day", "title": "The Next Day", "year": 2013,
             "producer": "tony-visconti", "songs": []},
            {"slug": "blackstar", "title": "Blackstar", "year": 2016,
             "producer": "tony-visconti", "songs": []},
        ],
    },

    # ==================== 13. MICHAEL JACKSON ====================
    {
        "slug": "michael-jackson", "title": "Michael Jackson", "band_type": "Solo",
        "genres": ["Pop"], "scene": "Pop", "formed": 1964,
        "members": [],
        "albums": [
            {"slug": "off-the-wall-mj", "title": "Off the Wall", "year": 1979,
             "producer": "quincy-jones", "songs": [
                 ("rock-with-you-mj", "Rock with You"),
                 ("dont-stop-til-you-get-enough-mj", "Don't Stop 'Til You Get Enough"),
             ]},
            {"slug": "thriller-album", "title": "Thriller", "year": 1982,
             "producer": "quincy-jones", "songs": [
                 ("thriller-mj", "Thriller"),
                 ("billie-jean-mj", "Billie Jean"),
                 ("beat-it-mj", "Beat It"),
                 ("wanna-be-startin-mj", "Wanna Be Startin' Somethin'"),
                 ("human-nature-mj", "Human Nature"),
             ]},
            {"slug": "bad-album-mj", "title": "Bad", "year": 1987,
             "producer": "quincy-jones", "songs": [
                 ("man-in-the-mirror-mj", "Man in the Mirror"),
                 ("smooth-criminal-mj", "Smooth Criminal"),
                 ("bad-song-mj", "Bad"),
             ]},
            {"slug": "dangerous-album-mj", "title": "Dangerous", "year": 1991,
             "producer": "teddy-riley", "songs": [
                 ("black-or-white-mj", "Black or White"),
             ]},
            {"slug": "history-album-mj", "title": "HIStory", "year": 1995,
             "producer": "quincy-jones", "songs": []},
            {"slug": "invincible-mj", "title": "Invincible", "year": 2001,
             "producer": "teddy-riley", "songs": []},
        ],
    },

    # ==================== 14. PRINCE ====================
    {
        "slug": "prince", "title": "Prince", "band_type": "Solo",
        "genres": ["Pop"], "scene": "Pop", "formed": 1976,
        "members": [],
        "albums": [
            {"slug": "dirty-mind-prince", "title": "Dirty Mind", "year": 1980,
             "producer": "prince-person", "songs": []},
            {"slug": "controversy-prince", "title": "Controversy", "year": 1981,
             "producer": "prince-person", "songs": []},
            {"slug": "1999-prince", "title": "1999", "year": 1982,
             "producer": "prince-person", "songs": [
                 ("little-red-corvette-prince", "Little Red Corvette"),
                 ("1999-prince-song", "1999"),
             ]},
            {"slug": "purple-rain-album", "title": "Purple Rain", "year": 1984,
             "producer": "prince-person", "songs": [
                 ("purple-rain-prince", "Purple Rain"),
                 ("when-doves-cry-prince", "When Doves Cry"),
                 ("lets-go-crazy-prince", "Let's Go Crazy"),
                 ("i-would-die-4-u-prince", "I Would Die 4 U"),
                 ("baby-im-a-star-prince", "Baby I'm a Star"),
             ]},
            {"slug": "around-the-world-prince", "title": "Around the World in a Day", "year": 1985,
             "producer": "prince-person", "songs": [
                 ("raspberry-beret-prince", "Raspberry Beret"),
             ]},
            {"slug": "sign-o-the-times", "title": "Sign O the Times", "year": 1987,
             "producer": "prince-person", "songs": [
                 ("kiss-prince", "Kiss"),
                 ("sign-o-the-times-prince", "Sign 'O' the Times"),
             ]},
            {"slug": "lovesexy", "title": "Lovesexy", "year": 1988,
             "producer": "prince-person", "songs": []},
            {"slug": "diamonds-and-pearls", "title": "Diamonds and Pearls", "year": 1991,
             "producer": "prince-person", "songs": []},
        ],
    },

    # ==================== 15. MADONNA ====================
    {
        "slug": "madonna", "title": "Madonna", "band_type": "Solo",
        "genres": ["Pop"], "scene": "Pop", "formed": 1979,
        "members": [],
        "albums": [
            {"slug": "madonna-album", "title": "Madonna", "year": 1983,
             "producer": "madonna-person", "songs": [
                 ("holiday-mad", "Holiday"),
             ]},
            {"slug": "like-a-virgin-album", "title": "Like a Virgin", "year": 1984,
             "producer": "nile-rodgers", "songs": [
                 ("like-a-virgin-mad", "Like a Virgin"),
                 ("material-girl-mad", "Material Girl"),
             ]},
            {"slug": "true-blue-album", "title": "True Blue", "year": 1986,
             "producer": "madonna-person", "songs": [
                 ("papa-dont-preach-mad", "Papa Don't Preach"),
                 ("open-your-heart-mad", "Open Your Heart"),
                 ("la-isla-bonita-mad", "La Isla Bonita"),
             ]},
            {"slug": "like-a-prayer-album", "title": "Like a Prayer", "year": 1989,
             "producer": "patrick-leonard", "songs": [
                 ("like-a-prayer-mad", "Like a Prayer"),
                 ("express-yourself-mad", "Express Yourself"),
                 ("vogue-mad", "Vogue"),
             ]},
            {"slug": "erotica-album", "title": "Erotica", "year": 1992,
             "producer": "madonna-person", "songs": []},
            {"slug": "bedtime-stories", "title": "Bedtime Stories", "year": 1994,
             "producer": "madonna-person", "songs": []},
            {"slug": "ray-of-light", "title": "Ray of Light", "year": 1998,
             "producer": "william-orbit", "songs": [
                 ("ray-of-light-mad", "Ray of Light"),
                 ("frozen-mad", "Frozen"),
             ]},
        ],
    },

    # ==================== 16. A-HA ====================
    {
        "slug": "a-ha", "title": "a-ha", "band_type": "Group",
        "genres": ["Alternative Rock"], "scene": "Alternative Rock", "formed": 1982,
        "members": [
            ("morten-harket", "Vocals"), ("paul-waaktaar-savoy", "Guitar"),
            ("mags-furuholmen", "Keyboards"),
        ],
        "albums": [
            {"slug": "hunting-high-and-low", "title": "Hunting High and Low", "year": 1985,
             "producer": "alan-tarney", "songs": [
                 ("take-on-me-aha", "Take On Me"),
                 ("the-sun-always-shines-aha", "The Sun Always Shines on T.V."),
                 ("train-of-thought-aha", "Train of Thought"),
             ]},
            {"slug": "scoundrel-days", "title": "Scoundrel Days", "year": 1986,
             "producer": "alan-tarney", "songs": [
                 ("manhattan-skyline-aha", "Manhattan Skyline"),
             ]},
            {"slug": "stay-on-these-roads", "title": "Stay on These Roads", "year": 1988,
             "producer": "alan-tarney", "songs": [
                 ("crying-in-the-rain-aha", "Crying in the Rain"),
             ]},
            {"slug": "east-of-the-sun", "title": "East of the Sun West of the Moon", "year": 1990,
             "producer": "alan-tarney", "songs": []},
        ],
    },

    # ==================== 17. THE B-52S ====================
    {
        "slug": "the-b-52s", "title": "The B-52s", "band_type": "Group",
        "genres": ["Alternative Rock"], "scene": "Athens GA", "formed": 1976,
        "members": [
            ("fred-schneider", "Vocals"), ("kate-pierson", "Vocals/Keyboards"),
            ("cindy-wilson", "Vocals"), ("ricky-wilson-b52", "Guitar"),
            ("keith-strickland", "Drums/Guitar"),
        ],
        "albums": [
            {"slug": "the-b-52s-album", "title": "The B-52s", "year": 1979,
             "producer": "fred-schneider", "songs": [
                 ("rock-lobster-b52", "Rock Lobster"),
                 ("planet-claire-b52", "Planet Claire"),
             ]},
            {"slug": "wild-planet", "title": "Wild Planet", "year": 1980,
             "producer": "fred-schneider", "songs": [
                 ("quiche-lorraine-b52", "Quiche Lorraine"),
                 ("private-idaho-b52", "Private Idaho"),
             ]},
            {"slug": "whammy", "title": "Whammy!", "year": 1983,
             "producer": "keith-strickland", "songs": []},
            {"slug": "bouncing-off-the-satellites", "title": "Bouncing Off the Satellites", "year": 1986,
             "producer": "keith-strickland", "songs": []},
            {"slug": "cosmic-thing", "title": "Cosmic Thing", "year": 1989,
             "producer": "don-was", "songs": [
                 ("love-shack-b52", "Love Shack"),
                 ("roam-b52", "Roam"),
             ]},
        ],
    },

    # ==================== 18. THE PRETENDERS ====================
    {
        "slug": "the-pretenders", "title": "The Pretenders", "band_type": "Group",
        "genres": ["Rock"], "scene": "Rock", "formed": 1978,
        "members": [
            ("chrissie-hynde", "Vocals/Guitar"), ("james-honeyman-scott", "Guitar"),
            ("martin-chambers-pretenders", "Drums"),
        ],
        "albums": [
            {"slug": "pretenders-album", "title": "Pretenders", "year": 1980,
             "producer": "chris-thomas-inxs", "songs": [
                 ("brass-in-pocket-pre", "Brass in Pocket"),
                 ("talk-of-the-town-pre", "Talk of the Town"),
             ]},
            {"slug": "pretenders-ii", "title": "Pretenders II", "year": 1981,
             "producer": "chris-thomas-inxs", "songs": []},
            {"slug": "learning-to-crawl", "title": "Learning to Crawl", "year": 1984,
             "producer": "chris-thomas-inxs", "songs": [
                 ("back-on-the-chain-gang-pre", "Back on the Chain Gang"),
                 ("middle-of-the-road-pre", "Middle of the Road"),
                 ("2000-miles-pre", "2000 Miles"),
             ]},
            {"slug": "get-close", "title": "Get Close", "year": 1986,
             "producer": "jimmy-iovine", "songs": [
                 ("dont-get-me-wrong-pre", "Don't Get Me Wrong"),
                 ("ill-stand-by-you-pre", "I'll Stand by You"),
             ]},
            {"slug": "packed", "title": "Packed!", "year": 1990,
             "producer": "chrissie-hynde", "songs": []},
        ],
    },

    # ==================== 19. PET SHOP BOYS ====================
    {
        "slug": "pet-shop-boys", "title": "Pet Shop Boys", "band_type": "Group",
        "genres": ["Electronic"], "scene": "London UK", "formed": 1981,
        "members": [
            ("neil-tennant", "Vocals"), ("chris-lowe", "Keyboards"),
        ],
        "albums": [
            {"slug": "please-psb", "title": "Please", "year": 1986,
             "producer": "stephen-hague", "songs": [
                 ("west-end-girls-psb", "West End Girls"),
                 ("opportunities-psb", "Opportunities (Let's Make Lots of Money)"),
             ]},
            {"slug": "actually-psb", "title": "Actually", "year": 1987,
             "producer": "neil-tennant", "songs": [
                 ("its-a-sin-psb", "It's a Sin"),
                 ("always-on-my-mind-psb", "Always on My Mind"),
                 ("what-have-i-done-psb", "What Have I Done to Deserve This?"),
             ]},
            {"slug": "introspective-psb", "title": "Introspective", "year": 1988,
             "producer": "neil-tennant", "songs": [
                 ("left-to-my-own-devices-psb", "Left to My Own Devices"),
             ]},
            {"slug": "behaviour-psb", "title": "Behaviour", "year": 1990,
             "producer": "neil-tennant", "songs": [
                 ("being-boring-psb", "Being Boring"),
             ]},
            {"slug": "very-psb", "title": "Very", "year": 1993,
             "producer": "neil-tennant", "songs": [
                 ("go-west-psb", "Go West"),
             ]},
            {"slug": "bilingual-psb", "title": "Bilingual", "year": 1996,
             "producer": "neil-tennant", "songs": []},
        ],
    },

    # ==================== 20. SIMPLE MINDS ====================
    {
        "slug": "simple-minds", "title": "Simple Minds", "band_type": "Group",
        "genres": ["Alternative Rock"], "scene": "Alternative Rock", "formed": 1977,
        "members": [
            ("jim-kerr", "Vocals"), ("charlie-burchill", "Guitar"),
            ("mick-macneil", "Keyboards"),
        ],
        "albums": [
            {"slug": "sons-and-fascination", "title": "Sons and Fascination", "year": 1981,
             "producer": "steve-hillage", "songs": []},
            {"slug": "new-gold-dream", "title": "New Gold Dream", "year": 1982,
             "producer": "jim-kerr", "songs": [
                 ("all-the-things-she-said-sm", "All the Things She Said"),
             ]},
            {"slug": "sparkle-in-the-rain", "title": "Sparkle in the Rain", "year": 1984,
             "producer": "steve-hillage", "songs": [
                 ("waterfront-sm", "Waterfront"),
                 ("up-on-the-catwalk-sm", "Up on the Catwalk"),
             ]},
            {"slug": "once-upon-a-time", "title": "Once Upon a Time", "year": 1985,
             "producer": "jimmy-iovine", "songs": [
                 ("dont-you-forget-about-me-sm", "Don't You (Forget About Me)"),
                 ("alive-and-kicking-sm", "Alive and Kicking"),
                 ("sanctify-yourself-sm", "Sanctify Yourself"),
             ]},
            {"slug": "street-fighting-years", "title": "Street Fighting Years", "year": 1989,
             "producer": "jim-kerr", "songs": []},
        ],
    },

    # ==================== 21. BLONDIE ====================
    {
        "slug": "blondie", "title": "Blondie", "band_type": "Group",
        "genres": ["Punk Rock"], "scene": "Punk Rock", "formed": 1974,
        "members": [
            ("debbie-harry", "Vocals"), ("chris-stein", "Guitar"),
            ("clem-burke", "Drums"), ("nigel-harrison", "Bass"),
        ],
        "albums": [
            {"slug": "blondie-album", "title": "Blondie", "year": 1976,
             "producer": "chris-stein", "songs": []},
            {"slug": "plastic-letters", "title": "Plastic Letters", "year": 1978,
             "producer": "chris-stein", "songs": []},
            {"slug": "parallel-lines", "title": "Parallel Lines", "year": 1978,
             "producer": "mike-chapman-prod", "songs": [
                 ("heart-of-glass-blo", "Heart of Glass"),
                 ("one-way-or-another-blo", "One Way or Another"),
                 ("hanging-on-the-telephone-blo", "Hanging on the Telephone"),
             ]},
            {"slug": "eat-to-the-beat", "title": "Eat to the Beat", "year": 1979,
             "producer": "mike-chapman-prod", "songs": [
                 ("atomic-blo", "Atomic"),
                 ("dreaming-blo", "Dreaming"),
             ]},
            {"slug": "autoamerican", "title": "Autoamerican", "year": 1980,
             "producer": "mike-chapman-prod", "songs": [
                 ("call-me-blo", "Call Me"),
                 ("rapture-blo", "Rapture"),
                 ("the-tide-is-high-blo", "The Tide Is High"),
             ]},
            {"slug": "the-hunter-blondie", "title": "The Hunter", "year": 1982,
             "producer": "mike-chapman-prod", "songs": []},
            {"slug": "no-exit-blondie", "title": "No Exit", "year": 1999,
             "producer": "debbie-harry", "songs": []},
        ],
    },

    # ==================== 22. CYNDI LAUPER ====================
    {
        "slug": "cyndi-lauper", "title": "Cyndi Lauper", "band_type": "Solo",
        "genres": ["Pop"], "scene": "Pop", "formed": 1979,
        "members": [],
        "albums": [
            {"slug": "shes-so-unusual", "title": "She's So Unusual", "year": 1983,
             "producer": "rick-chertoff", "songs": [
                 ("girls-just-want-to-have-fun-cl", "Girls Just Want to Have Fun"),
                 ("time-after-time-cl", "Time After Time"),
                 ("she-bop-cl", "She Bop"),
             ]},
            {"slug": "true-colors-album", "title": "True Colors", "year": 1986,
             "producer": "rick-chertoff", "songs": [
                 ("true-colors-cl", "True Colors"),
                 ("change-of-heart-cl", "Change of Heart"),
             ]},
            {"slug": "a-night-to-remember", "title": "A Night to Remember", "year": 1989,
             "producer": "rick-chertoff", "songs": [
                 ("i-drove-all-night-cl", "I Drove All Night"),
             ]},
            {"slug": "hat-full-of-stars", "title": "Hat Full of Stars", "year": 1993,
             "producer": "rick-chertoff", "songs": []},
        ],
    },

    # ==================== 23. BILLY IDOL ====================
    {
        "slug": "billy-idol", "title": "Billy Idol", "band_type": "Solo",
        "genres": ["Punk Rock"], "scene": "Punk Rock", "formed": 1981,
        "members": [],
        "albums": [
            {"slug": "billy-idol-album", "title": "Billy Idol", "year": 1982,
             "producer": "keith-forsey", "songs": [
                 ("white-wedding-bi", "White Wedding"),
             ]},
            {"slug": "rebel-yell-album", "title": "Rebel Yell", "year": 1983,
             "producer": "keith-forsey", "songs": [
                 ("rebel-yell-bi", "Rebel Yell"),
                 ("eyes-without-a-face-bi", "Eyes Without a Face"),
                 ("flesh-for-fantasy-bi", "Flesh for Fantasy"),
             ]},
            {"slug": "whiplash-smile", "title": "Whiplash Smile", "year": 1986,
             "producer": "keith-forsey", "songs": []},
            {"slug": "charmed-life", "title": "Charmed Life", "year": 1990,
             "producer": "keith-forsey", "songs": [
                 ("mony-mony-bi", "Mony Mony"),
                 ("cradle-of-love-bi", "Cradle of Love"),
             ]},
        ],
    },

    # ==================== 24. TRACY CHAPMAN ====================
    {
        "slug": "tracy-chapman", "title": "Tracy Chapman", "band_type": "Solo",
        "genres": ["Folk"], "scene": "Folk", "formed": 1987,
        "members": [],
        "albums": [
            {"slug": "tracy-chapman-album", "title": "Tracy Chapman", "year": 1988,
             "producer": "david-kershenbaum", "songs": [
                 ("fast-car-tc", "Fast Car"),
                 ("talkin-bout-a-revolution-tc", "Talkin' Bout a Revolution"),
                 ("baby-can-i-hold-you-tc", "Baby Can I Hold You"),
                 ("mountains-o-things-tc", "Mountains o' Things"),
             ]},
            {"slug": "crossroads-tc", "title": "Crossroads", "year": 1989,
             "producer": "david-kershenbaum", "songs": []},
            {"slug": "matters-of-the-heart", "title": "Matters of the Heart", "year": 1992,
             "producer": "tracy-chapman-person", "songs": []},
            {"slug": "new-beginning", "title": "New Beginning", "year": 1995,
             "producer": "tracy-chapman-person", "songs": [
                 ("give-me-one-reason-tc", "Give Me One Reason"),
                 ("the-promise-tc", "The Promise"),
             ]},
        ],
    },

    # ==================== 25. SINEAD O'CONNOR ====================
    {
        "slug": "sinead-oconnor", "title": "Sinead O'Connor", "band_type": "Solo",
        "genres": ["Alternative Rock"], "scene": "Alternative Rock", "formed": 1985,
        "members": [],
        "albums": [
            {"slug": "the-lion-and-the-cobra", "title": "The Lion and the Cobra", "year": 1987,
             "producer": "nigel-grainge", "songs": [
                 ("mandinka-soc", "Mandinka"),
                 ("troy-soc", "Troy"),
             ]},
            {"slug": "i-do-not-want", "title": "I Do Not Want What I Haven't Got", "year": 1990,
             "producer": "sinead-oconnor-person", "songs": [
                 ("nothing-compares-2-u-soc", "Nothing Compares 2 U"),
                 ("emperors-new-clothes-soc", "Emperor's New Clothes"),
                 ("last-day-of-our-acquaintance-soc", "The Last Day of Our Acquaintance"),
             ]},
            {"slug": "am-i-not-your-girl", "title": "Am I Not Your Girl?", "year": 1992,
             "producer": "sinead-oconnor-person", "songs": []},
            {"slug": "universal-mother", "title": "Universal Mother", "year": 1994,
             "producer": "sinead-oconnor-person", "songs": [
                 ("fire-on-babylon-soc", "Fire on Babylon"),
             ]},
        ],
    },
]

# ============================================================
# PEOPLE DATA: (slug, full_name, [(band_slug, role), ...])
# song_credits are derived automatically from SONG_CREDITS
# ============================================================
PEOPLE_DATA = [
    # U2
    ("bono", "Bono", [("u2", "Vocals")]),
    ("the-edge", "The Edge", [("u2", "Guitar")]),
    ("adam-clayton", "Adam Clayton", [("u2", "Bass")]),
    ("larry-mullen-jr", "Larry Mullen Jr.", [("u2", "Drums")]),
    ("brian-eno", "Brian Eno", []),
    ("daniel-lanois", "Daniel Lanois", []),
    ("steve-lillywhite", "Steve Lillywhite", []),
    # The Police
    ("sting", "Sting", [("the-police", "Vocals/Bass")]),
    ("andy-summers", "Andy Summers", [("the-police", "Guitar")]),
    ("stewart-copeland", "Stewart Copeland", [("the-police", "Drums")]),
    ("nigel-gray", "Nigel Gray", []),
    ("hugh-padgham", "Hugh Padgham", []),
    # Depeche Mode
    ("dave-gahan", "Dave Gahan", [("depeche-mode", "Vocals")]),
    ("martin-gore", "Martin Gore", [("depeche-mode", "Guitar/Keyboards/Vocals")]),
    ("andrew-fletcher", "Andrew Fletcher", [("depeche-mode", "Keyboards")]),
    ("alan-wilder", "Alan Wilder", [("depeche-mode", "Keyboards")]),
    ("vince-clarke", "Vince Clarke", [("depeche-mode", "Keyboards")]),
    ("flood-producer", "Flood", []),
    ("daniel-miller", "Daniel Miller", []),
    # New Order
    ("bernard-sumner", "Bernard Sumner", [("new-order", "Vocals/Guitar")]),
    ("peter-hook", "Peter Hook", [("new-order", "Bass")]),
    ("stephen-morris", "Stephen Morris", [("new-order", "Drums")]),
    ("gillian-gilbert", "Gillian Gilbert", [("new-order", "Keyboards")]),
    ("stephen-hague", "Stephen Hague", []),
    # The Cure
    ("robert-smith-cure", "Robert Smith", [("the-cure", "Vocals/Guitar")]),
    ("lol-tolhurst", "Lol Tolhurst", [("the-cure", "Drums/Keyboards")]),
    ("simon-gallup", "Simon Gallup", [("the-cure", "Bass")]),
    ("porl-thompson", "Porl Thompson", [("the-cure", "Guitar")]),
    ("mike-hedges", "Mike Hedges", []),
    ("mark-stent", "Mark Stent", []),
    # The Smiths
    ("morrissey", "Morrissey", [("the-smiths", "Vocals")]),
    ("johnny-marr", "Johnny Marr", [("the-smiths", "Guitar")]),
    ("andy-rourke", "Andy Rourke", [("the-smiths", "Bass")]),
    ("mike-joyce-smiths", "Mike Joyce", [("the-smiths", "Drums")]),
    ("stephen-street", "Stephen Street", []),
    ("john-porter", "John Porter", []),
    # Talking Heads
    ("david-byrne", "David Byrne", [("talking-heads", "Vocals/Guitar")]),
    ("chris-frantz", "Chris Frantz", [("talking-heads", "Drums")]),
    ("tina-weymouth", "Tina Weymouth", [("talking-heads", "Bass")]),
    ("jerry-harrison", "Jerry Harrison", [("talking-heads", "Guitar/Keyboards")]),
    # INXS
    ("michael-hutchence", "Michael Hutchence", [("inxs", "Vocals")]),
    ("andrew-farriss", "Andrew Farriss", [("inxs", "Keyboards/Guitar")]),
    ("tim-farriss", "Tim Farriss", [("inxs", "Guitar")]),
    ("jon-farriss", "Jon Farriss", [("inxs", "Drums")]),
    ("garry-gary-beers", "Garry Gary Beers", [("inxs", "Bass")]),
    ("kirk-pengilly", "Kirk Pengilly", [("inxs", "Guitar")]),
    ("chris-thomas-inxs", "Chris Thomas", []),
    ("mark-opitz", "Mark Opitz", []),
    # Eurythmics
    ("annie-lennox", "Annie Lennox", [("eurythmics", "Vocals")]),
    ("dave-stewart", "Dave Stewart", [("eurythmics", "Guitar/Keyboards")]),
    # Tears for Fears
    ("roland-orzabal", "Roland Orzabal", [("tears-for-fears", "Vocals/Guitar")]),
    ("curt-smith-tff", "Curt Smith", [("tears-for-fears", "Bass/Vocals")]),
    ("chris-hughes-tff", "Chris Hughes", []),
    # Duran Duran
    ("simon-le-bon", "Simon Le Bon", [("duran-duran", "Vocals")]),
    ("nick-rhodes", "Nick Rhodes", [("duran-duran", "Keyboards")]),
    ("john-taylor-dd", "John Taylor", [("duran-duran", "Bass")]),
    ("roger-taylor-dd", "Roger Taylor", [("duran-duran", "Drums")]),
    ("andy-taylor-dd", "Andy Taylor", [("duran-duran", "Guitar")]),
    ("colin-thurston", "Colin Thurston", []),
    ("nile-rodgers", "Nile Rodgers", []),
    # David Bowie
    ("david-bowie-person", "David Bowie", []),
    ("tony-visconti", "Tony Visconti", []),
    ("mick-ronson", "Mick Ronson", []),
    # Michael Jackson
    ("michael-jackson-person", "Michael Jackson", []),
    ("quincy-jones", "Quincy Jones", []),
    ("teddy-riley", "Teddy Riley", []),
    # Prince
    ("prince-person", "Prince", []),
    # Madonna
    ("madonna-person", "Madonna", []),
    ("patrick-leonard", "Patrick Leonard", []),
    ("william-orbit", "William Orbit", []),
    # a-ha
    ("morten-harket", "Morten Harket", [("a-ha", "Vocals")]),
    ("paul-waaktaar-savoy", "Paul Waaktaar-Savoy", [("a-ha", "Guitar")]),
    ("mags-furuholmen", "Mags Furuholmen", [("a-ha", "Keyboards")]),
    ("alan-tarney", "Alan Tarney", []),
    # The B-52s
    ("fred-schneider", "Fred Schneider", [("the-b-52s", "Vocals")]),
    ("kate-pierson", "Kate Pierson", [("the-b-52s", "Vocals/Keyboards")]),
    ("cindy-wilson", "Cindy Wilson", [("the-b-52s", "Vocals")]),
    ("ricky-wilson-b52", "Ricky Wilson", [("the-b-52s", "Guitar")]),
    ("keith-strickland", "Keith Strickland", [("the-b-52s", "Drums/Guitar")]),
    ("don-was", "Don Was", []),
    # The Pretenders
    ("chrissie-hynde", "Chrissie Hynde", [("the-pretenders", "Vocals/Guitar")]),
    ("james-honeyman-scott", "James Honeyman-Scott", [("the-pretenders", "Guitar")]),
    ("martin-chambers-pretenders", "Martin Chambers", [("the-pretenders", "Drums")]),
    # jimmy-iovine already listed in existing script; will be skipped if exists
    ("jimmy-iovine", "Jimmy Iovine", []),
    # Pet Shop Boys
    ("neil-tennant", "Neil Tennant", [("pet-shop-boys", "Vocals")]),
    ("chris-lowe", "Chris Lowe", [("pet-shop-boys", "Keyboards")]),
    # Simple Minds
    ("jim-kerr", "Jim Kerr", [("simple-minds", "Vocals")]),
    ("charlie-burchill", "Charlie Burchill", [("simple-minds", "Guitar")]),
    ("mick-macneil", "Mick MacNeil", [("simple-minds", "Keyboards")]),
    ("keith-forsey", "Keith Forsey", []),
    ("steve-hillage", "Steve Hillage", []),
    # Blondie
    ("debbie-harry", "Debbie Harry", [("blondie", "Vocals")]),
    ("chris-stein", "Chris Stein", [("blondie", "Guitar")]),
    ("clem-burke", "Clem Burke", [("blondie", "Drums")]),
    ("nigel-harrison", "Nigel Harrison", [("blondie", "Bass")]),
    ("mike-chapman-prod", "Mike Chapman", []),
    ("giorgio-moroder", "Giorgio Moroder", []),
    # Cyndi Lauper
    ("cyndi-lauper-person", "Cyndi Lauper", []),
    ("rick-chertoff", "Rick Chertoff", []),
    # Billy Idol
    ("billy-idol-person", "Billy Idol", []),
    ("steve-stevens", "Steve Stevens", []),
    # Tracy Chapman
    ("tracy-chapman-person", "Tracy Chapman", []),
    ("david-kershenbaum", "David Kershenbaum", []),
    # Sinead O'Connor
    ("sinead-oconnor-person", "Sinéad O'Connor", []),
    ("nigel-grainge", "Nigel Grainge", []),
    # alex-sadkin listed in existing script; will be skipped if exists
    ("alex-sadkin", "Alex Sadkin", []),
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
    if a.get("disbanded"):
        lines.append(f"disbanded: {a['disbanded']}")
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
             f"producer: {alb['producer']}"]
    songs = alb.get("songs", [])
    if songs:
        lines.append("songs:")
        for s_slug, s_title in songs:
            lines += [f"  - slug: {q(s_slug)}", f"    title: {q(s_title)}"]
    else:
        lines.append("songs: []")
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
        for s_slug, s_title, credit in song_credits_list:
            lines += [f"  - slug: {q(s_slug)}", f"    title: {q(s_title)}",
                      f"    credit: {q(credit)}"]
    lines.append("---")
    return "\n".join(lines) + "\n"


# ============================================================
# MAIN
# ============================================================

def main():
    # Build PERSON_CREDITS from SONG_CREDITS and ARTIST_DATA
    # First build a lookup: song_slug -> (title, artist_slug, album_slug, year)
    song_info = {}
    for artist in ARTIST_DATA:
        for alb in artist["albums"]:
            for s_slug, s_title in alb.get("songs", []):
                song_info[s_slug] = (s_title, artist["slug"], alb["slug"], alb["year"])

    # Build PERSON_CREDITS
    for s_slug, credits in SONG_CREDITS.items():
        if s_slug not in song_info:
            print(f"  WARNING: song {s_slug} in SONG_CREDITS but not in any album")
            continue
        s_title = song_info[s_slug][0]
        for p_slug, role in credits:
            PERSON_CREDITS[p_slug].append((s_slug, s_title, role))

    processed_songs = set()

    # Write artist, album, and song files
    for artist in ARTIST_DATA:
        a_slug = artist["slug"]
        wf(CONTENT / "artists" / f"{a_slug}.md", gen_artist(artist))

        for alb in artist["albums"]:
            alb_slug = alb["slug"]
            wf(CONTENT / "albums" / f"{alb_slug}.md", gen_album(alb, a_slug))

            for s_slug, s_title in alb.get("songs", []):
                if s_slug in processed_songs:
                    continue
                processed_songs.add(s_slug)

                credits = SONG_CREDITS.get(s_slug, [])
                if not credits:
                    print(f"  WARNING: no credits for song {s_slug}")
                    credits = [(a_slug, "Writer")]

                wf(CONTENT / "songs" / f"{s_slug}.md",
                   gen_song(s_slug, s_title, a_slug, alb_slug, alb["year"], credits))

    # Write people files
    for slug, title, bands in PEOPLE_DATA:
        sc = PERSON_CREDITS.get(slug, [])
        wf(CONTENT / "people" / f"{slug}.md", gen_person(slug, title, bands, sc))

    print(f"\nDone! Created: {created_count}  |  Skipped (already exist): {skipped_count}")
    print(f"Artists: {len(ARTIST_DATA)}")
    total_albums = sum(len(a["albums"]) for a in ARTIST_DATA)
    print(f"Albums:  {total_albums}")
    print(f"Songs:   {len(processed_songs)}")
    print(f"People:  {len(PEOPLE_DATA)}")


if __name__ == "__main__":
    main()
