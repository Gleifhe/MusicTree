#!/usr/bin/env python3
"""
create_batch2_content.py — Batch-creates Hugo content for 25 artists.
Idempotent: skips existing files.
Uses Path.write_text(encoding="utf-8") — no BOM.
"""
from pathlib import Path

ROOT   = Path(__file__).parent.parent
ARTISTS = ROOT / "content" / "artists"
ALBUMS  = ROOT / "content" / "albums"
SONGS   = ROOT / "content" / "songs"
PEOPLE  = ROOT / "content" / "people"


def write(path: Path, content: str) -> None:
    if path.exists():
        print(f"  skip   {path.relative_to(ROOT)}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  create {path.relative_to(ROOT)}")


def q(s: str) -> str:
    """Wrap string in YAML double-quotes, escaping inner double-quotes."""
    return '"' + s.replace('"', '\\"') + '"'


def artist_md(slug, title, band_type, genres, scene, formed, members, album_refs,
              disbanded=None):
    lines = ["---",
             f"title: {q(title)}", f"slug: {slug}", f"band_type: {band_type}",
             f"genres: [{', '.join(genres)}]", f"scene: {scene}", f"formed: {formed}"]
    if disbanded:
        lines.append(f"disbanded: {disbanded}")
    if members:
        lines.append("members:")
        for ms, mr in members:
            lines += [f"  - slug: {ms}", f"    role: {mr}"]
    if album_refs:
        lines.append("albums:")
        for a in album_refs:
            lines.append(f"  - slug: {a}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def album_md(slug, title, artist, year, songs, producer=None):
    lines = ["---", f"title: {q(title)}", f"slug: {slug}",
             f"artist: {artist}", f"year: {year}"]
    if producer:
        lines.append(f"producer: {producer}")
    if songs:
        lines.append("songs:")
        for ss, st in songs:
            lines += [f"  - slug: {ss}", f"    title: {q(st)}"]
    lines.append("---")
    return "\n".join(lines) + "\n"


def song_md(slug, title, artist, album, year, credits):
    lines = ["---", f"title: {q(title)}", f"slug: {slug}",
             f"artist: {artist}", f"album: {album}", f"year: {year}"]
    if credits:
        lines.append("credits:")
        for ps, role in credits:
            lines += [f"  - person_slug: {ps}", f"    role: {role}"]
    lines.append("---")
    return "\n".join(lines) + "\n"


def person_md(slug, title, bands, song_credits):
    lines = ["---", f"title: {q(title)}", f"slug: {slug}"]
    if bands:
        lines.append("bands:")
        for bs, br in bands:
            lines += [f"  - slug: {bs}", f"    role: {br}"]
    if song_credits:
        lines.append("song_credits:")
        for scs, sct, scc in song_credits:
            lines += [f"  - slug: {scs}", f"    title: {q(sct)}", f"    credit: {scc}"]
    lines.append("---")
    return "\n".join(lines) + "\n"


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — EMF
# ═══════════════════════════════════════════════════════════════════════════════
write(ARTISTS / "emf.md", artist_md(
    "emf", "EMF", "Group", ["Alternative Rock"], "Alternative Rock", 1989,
    [("james-atkin", "Vocals"), ("derry-brownson", "Keyboards"),
     ("mark-decloedt", "Drums"), ("ian-dench", "Guitar"), ("zac-foley", "Bass")],
    ["schubert-dip-emf"], disbanded=1995
))
write(ALBUMS / "schubert-dip-emf.md", album_md(
    "schubert-dip-emf", "Schubert Dip", "emf", 1991,
    [("unbelievable-emf", "Unbelievable"), ("lies-emf", "Lies"),
     ("i-believe-emf", "I Believe")]
))
write(SONGS / "unbelievable-emf.md", song_md(
    "unbelievable-emf", "Unbelievable", "emf", "schubert-dip-emf", 1991,
    [("james-atkin", "Vocals"), ("ian-dench", "Writer")]
))
write(SONGS / "lies-emf.md", song_md(
    "lies-emf", "Lies", "emf", "schubert-dip-emf", 1991,
    [("james-atkin", "Vocals"), ("ian-dench", "Writer")]
))
write(SONGS / "i-believe-emf.md", song_md(
    "i-believe-emf", "I Believe", "emf", "schubert-dip-emf", 1992,
    [("james-atkin", "Vocals"), ("ian-dench", "Writer")]
))
write(PEOPLE / "james-atkin.md", person_md(
    "james-atkin", "James Atkin", [("emf", "Vocals")],
    [("unbelievable-emf", "Unbelievable", "Vocals"),
     ("lies-emf", "Lies", "Vocals"),
     ("i-believe-emf", "I Believe", "Vocals")]
))
write(PEOPLE / "derry-brownson.md", person_md(
    "derry-brownson", "Derry Brownson", [("emf", "Keyboards")], []
))
write(PEOPLE / "mark-decloedt.md", person_md(
    "mark-decloedt", "Mark De Cloedt", [("emf", "Drums")], []
))
write(PEOPLE / "ian-dench.md", person_md(
    "ian-dench", "Ian Dench", [("emf", "Guitar")],
    [("unbelievable-emf", "Unbelievable", "Writer"),
     ("lies-emf", "Lies", "Writer"),
     ("i-believe-emf", "I Believe", "Writer")]
))
write(PEOPLE / "zac-foley.md", person_md(
    "zac-foley", "Zac Foley", [("emf", "Bass")], []
))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — MAMMOTH WVH
# ═══════════════════════════════════════════════════════════════════════════════
write(ARTISTS / "mammoth-wvh.md", artist_md(
    "mammoth-wvh", "Mammoth WVH", "Group", ["Rock"], "Rock", 2020,
    [("wolfgang-van-halen", "Vocals")],
    ["mammoth-wvh-album"]
))
write(ALBUMS / "mammoth-wvh-album.md", album_md(
    "mammoth-wvh-album", "Mammoth WVH", "mammoth-wvh", 2021,
    [("distance-mvh", "Distance"), ("think-it-over-mvh", "Think It Over"),
     ("mammoth-mvh", "Mammoth")]
))
write(SONGS / "distance-mvh.md", song_md(
    "distance-mvh", "Distance", "mammoth-wvh", "mammoth-wvh-album", 2021,
    [("wolfgang-van-halen", "Vocals")]
))
write(SONGS / "think-it-over-mvh.md", song_md(
    "think-it-over-mvh", "Think It Over", "mammoth-wvh", "mammoth-wvh-album", 2021,
    [("wolfgang-van-halen", "Vocals")]
))
write(SONGS / "mammoth-mvh.md", song_md(
    "mammoth-mvh", "Mammoth", "mammoth-wvh", "mammoth-wvh-album", 2021,
    [("wolfgang-van-halen", "Vocals")]
))
write(PEOPLE / "wolfgang-van-halen.md", person_md(
    "wolfgang-van-halen", "Wolfgang Van Halen", [("mammoth-wvh", "Vocals")],
    [("distance-mvh", "Distance", "Vocals"),
     ("think-it-over-mvh", "Think It Over", "Vocals"),
     ("mammoth-mvh", "Mammoth", "Vocals")]
))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — THE NOTORIOUS B.I.G.
# ═══════════════════════════════════════════════════════════════════════════════
write(ARTISTS / "notorious-big.md", artist_md(
    "notorious-big", "The Notorious B.I.G.", "Solo", ["Hip-Hop"], "Hip-Hop", 1991,
    [("christopher-wallace", "Rapper")],
    ["ready-to-die-big", "life-after-death-big"], disbanded=1997
))
write(ALBUMS / "ready-to-die-big.md", album_md(
    "ready-to-die-big", "Ready to Die", "notorious-big", 1994,
    [("juicy-big", "Juicy"), ("big-poppa-big", "Big Poppa"),
     ("one-more-chance-big", "One More Chance")]
))
write(ALBUMS / "life-after-death-big.md", album_md(
    "life-after-death-big", "Life After Death", "notorious-big", 1997,
    [("hypnotize-big", "Hypnotize"),
     ("mo-money-mo-problems-big", "Mo Money Mo Problems"),
     ("notorious-thugs-big", "Notorious Thugs")]
))
write(SONGS / "juicy-big.md", song_md(
    "juicy-big", "Juicy", "notorious-big", "ready-to-die-big", 1994,
    [("christopher-wallace", "Rapper")]
))
write(SONGS / "big-poppa-big.md", song_md(
    "big-poppa-big", "Big Poppa", "notorious-big", "ready-to-die-big", 1994,
    [("christopher-wallace", "Rapper")]
))
write(SONGS / "one-more-chance-big.md", song_md(
    "one-more-chance-big", "One More Chance", "notorious-big", "ready-to-die-big", 1995,
    [("christopher-wallace", "Rapper"), ("dj-premier", "Producer")]
))
write(SONGS / "hypnotize-big.md", song_md(
    "hypnotize-big", "Hypnotize", "notorious-big", "life-after-death-big", 1997,
    [("christopher-wallace", "Rapper"), ("dj-premier", "Producer")]
))
write(SONGS / "mo-money-mo-problems-big.md", song_md(
    "mo-money-mo-problems-big", "Mo Money Mo Problems", "notorious-big",
    "life-after-death-big", 1997,
    [("christopher-wallace", "Rapper")]
))
write(SONGS / "notorious-thugs-big.md", song_md(
    "notorious-thugs-big", "Notorious Thugs", "notorious-big",
    "life-after-death-big", 1997,
    [("christopher-wallace", "Rapper"), ("rza", "Producer")]
))
write(PEOPLE / "christopher-wallace.md", person_md(
    "christopher-wallace", "Christopher Wallace", [("notorious-big", "Rapper")],
    [("juicy-big", "Juicy", "Rapper"),
     ("big-poppa-big", "Big Poppa", "Rapper"),
     ("one-more-chance-big", "One More Chance", "Rapper"),
     ("hypnotize-big", "Hypnotize", "Rapper"),
     ("mo-money-mo-problems-big", "Mo Money Mo Problems", "Rapper"),
     ("notorious-thugs-big", "Notorious Thugs", "Rapper")]
))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — TUPAC SHAKUR
# ═══════════════════════════════════════════════════════════════════════════════
write(ARTISTS / "tupac-shakur.md", artist_md(
    "tupac-shakur", "2Pac", "Solo", ["Hip-Hop"], "Hip-Hop", 1991,
    [("tupac-shakur-person", "Rapper")],
    ["me-against-the-world-tupac", "all-eyez-on-me-tupac"], disbanded=1996
))
write(ALBUMS / "me-against-the-world-tupac.md", album_md(
    "me-against-the-world-tupac", "Me Against the World", "tupac-shakur", 1995,
    [("dear-mama-tupac", "Dear Mama"), ("keep-ya-head-up-tupac", "Keep Ya Head Up")]
))
write(ALBUMS / "all-eyez-on-me-tupac.md", album_md(
    "all-eyez-on-me-tupac", "All Eyez on Me", "tupac-shakur", 1996,
    [("california-love-tupac", "California Love"),
     ("ambitionz-az-a-ridah-tupac", "Ambitionz Az a Ridah"),
     ("hit-em-up-tupac", "Hit 'Em Up")],
    producer="dr-dre-person"
))
write(SONGS / "dear-mama-tupac.md", song_md(
    "dear-mama-tupac", "Dear Mama", "tupac-shakur",
    "me-against-the-world-tupac", 1995,
    [("tupac-shakur-person", "Rapper")]
))
write(SONGS / "keep-ya-head-up-tupac.md", song_md(
    "keep-ya-head-up-tupac", "Keep Ya Head Up", "tupac-shakur",
    "me-against-the-world-tupac", 1993,
    [("tupac-shakur-person", "Rapper")]
))
write(SONGS / "california-love-tupac.md", song_md(
    "california-love-tupac", "California Love", "tupac-shakur",
    "all-eyez-on-me-tupac", 1996,
    [("tupac-shakur-person", "Rapper"), ("dr-dre-person", "Producer")]
))
write(SONGS / "ambitionz-az-a-ridah-tupac.md", song_md(
    "ambitionz-az-a-ridah-tupac", "Ambitionz Az a Ridah", "tupac-shakur",
    "all-eyez-on-me-tupac", 1996,
    [("tupac-shakur-person", "Rapper"), ("dr-dre-person", "Producer")]
))
write(SONGS / "hit-em-up-tupac.md", song_md(
    "hit-em-up-tupac", "Hit 'Em Up", "tupac-shakur",
    "all-eyez-on-me-tupac", 1996,
    [("tupac-shakur-person", "Rapper"), ("dr-dre-person", "Producer")]
))
write(PEOPLE / "tupac-shakur-person.md", person_md(
    "tupac-shakur-person", "Tupac Shakur", [("tupac-shakur", "Rapper")],
    [("dear-mama-tupac", "Dear Mama", "Rapper"),
     ("keep-ya-head-up-tupac", "Keep Ya Head Up", "Rapper"),
     ("california-love-tupac", "California Love", "Rapper"),
     ("ambitionz-az-a-ridah-tupac", "Ambitionz Az a Ridah", "Rapper"),
     ("hit-em-up-tupac", "Hit 'Em Up", "Rapper")]
))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — WU-TANG CLAN
# ═══════════════════════════════════════════════════════════════════════════════
write(ARTISTS / "wu-tang-clan.md", artist_md(
    "wu-tang-clan", "Wu-Tang Clan", "Group", ["Hip-Hop"], "Hip-Hop", 1992,
    [("rza", "Producer"), ("gza", "Rapper"), ("method-man", "Rapper"),
     ("raekwon", "Rapper"), ("ghostface-killah", "Rapper"),
     ("inspectah-deck", "Rapper"), ("u-god", "Rapper"),
     ("masta-killa", "Rapper"), ("ol-dirty-bastard", "Rapper")],
    ["enter-the-wu-tang-36-chambers", "wu-tang-forever"]
))
write(ALBUMS / "enter-the-wu-tang-36-chambers.md", album_md(
    "enter-the-wu-tang-36-chambers", "Enter the Wu-Tang (36 Chambers)",
    "wu-tang-clan", 1993,
    [("c-r-e-a-m-wtc", "C.R.E.A.M."), ("protect-ya-neck-wtc", "Protect Ya Neck"),
     ("method-man-wtc", "Method Man")],
    producer="rza"
))
write(ALBUMS / "wu-tang-forever.md", album_md(
    "wu-tang-forever", "Wu-Tang Forever", "wu-tang-clan", 1997,
    [("triumph-wtc", "Triumph"), ("gravel-pit-wtc", "Gravel Pit")],
    producer="rza"
))
write(SONGS / "c-r-e-a-m-wtc.md", song_md(
    "c-r-e-a-m-wtc", "C.R.E.A.M.", "wu-tang-clan",
    "enter-the-wu-tang-36-chambers", 1993,
    [("rza", "Producer"), ("method-man", "Rapper")]
))
write(SONGS / "protect-ya-neck-wtc.md", song_md(
    "protect-ya-neck-wtc", "Protect Ya Neck", "wu-tang-clan",
    "enter-the-wu-tang-36-chambers", 1993,
    [("rza", "Producer"), ("ol-dirty-bastard", "Rapper")]
))
write(SONGS / "method-man-wtc.md", song_md(
    "method-man-wtc", "Method Man", "wu-tang-clan",
    "enter-the-wu-tang-36-chambers", 1993,
    [("rza", "Producer"), ("method-man", "Rapper")]
))
write(SONGS / "triumph-wtc.md", song_md(
    "triumph-wtc", "Triumph", "wu-tang-clan", "wu-tang-forever", 1997,
    [("rza", "Producer"), ("inspectah-deck", "Rapper")]
))
write(SONGS / "gravel-pit-wtc.md", song_md(
    "gravel-pit-wtc", "Gravel Pit", "wu-tang-clan", "wu-tang-forever", 2000,
    [("rza", "Producer")]
))
# RZA — consolidated with section 3
write(PEOPLE / "rza.md", person_md(
    "rza", "RZA", [("wu-tang-clan", "Producer")],
    [("notorious-thugs-big", "Notorious Thugs", "Producer"),
     ("c-r-e-a-m-wtc", "C.R.E.A.M.", "Producer"),
     ("protect-ya-neck-wtc", "Protect Ya Neck", "Producer"),
     ("method-man-wtc", "Method Man", "Producer"),
     ("triumph-wtc", "Triumph", "Producer"),
     ("gravel-pit-wtc", "Gravel Pit", "Producer")]
))
write(PEOPLE / "gza.md", person_md(
    "gza", "GZA", [("wu-tang-clan", "Rapper")], []
))
write(PEOPLE / "method-man.md", person_md(
    "method-man", "Method Man", [("wu-tang-clan", "Rapper")],
    [("c-r-e-a-m-wtc", "C.R.E.A.M.", "Rapper"),
     ("method-man-wtc", "Method Man", "Rapper")]
))
write(PEOPLE / "raekwon.md", person_md(
    "raekwon", "Raekwon", [("wu-tang-clan", "Rapper")], []
))
write(PEOPLE / "ghostface-killah.md", person_md(
    "ghostface-killah", "Ghostface Killah", [("wu-tang-clan", "Rapper")], []
))
write(PEOPLE / "inspectah-deck.md", person_md(
    "inspectah-deck", "Inspectah Deck", [("wu-tang-clan", "Rapper")],
    [("triumph-wtc", "Triumph", "Rapper")]
))
write(PEOPLE / "u-god.md", person_md(
    "u-god", "U-God", [("wu-tang-clan", "Rapper")], []
))
write(PEOPLE / "masta-killa.md", person_md(
    "masta-killa", "Masta Killa", [("wu-tang-clan", "Rapper")], []
))
write(PEOPLE / "ol-dirty-bastard.md", person_md(
    "ol-dirty-bastard", "Ol' Dirty Bastard", [("wu-tang-clan", "Rapper")],
    [("protect-ya-neck-wtc", "Protect Ya Neck", "Rapper")]
))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 6 — A TRIBE CALLED QUEST
# ═══════════════════════════════════════════════════════════════════════════════
write(ARTISTS / "a-tribe-called-quest.md", artist_md(
    "a-tribe-called-quest", "A Tribe Called Quest", "Group", ["Hip-Hop"], "Hip-Hop", 1985,
    [("q-tip", "Rapper"), ("phife-dawg", "Rapper"),
     ("ali-shaheed-muhammad", "DJ"), ("jarobi-white", "Rapper")],
    ["peoples-instinctive-travels-atcq", "low-end-theory-atcq",
     "midnight-marauders-atcq"], disbanded=1998
))
write(ALBUMS / "peoples-instinctive-travels-atcq.md", album_md(
    "peoples-instinctive-travels-atcq",
    "People's Instinctive Travels and the Paths of Rhythm",
    "a-tribe-called-quest", 1990,
    [("bonita-applebum-atcq", "Bonita Applebum"),
     ("can-i-kick-it-atcq", "Can I Kick It?")],
    producer="q-tip"
))
write(ALBUMS / "low-end-theory-atcq.md", album_md(
    "low-end-theory-atcq", "The Low End Theory",
    "a-tribe-called-quest", 1991,
    [("check-the-rhime-atcq", "Check the Rhime")],
    producer="q-tip"
))
write(ALBUMS / "midnight-marauders-atcq.md", album_md(
    "midnight-marauders-atcq", "Midnight Marauders",
    "a-tribe-called-quest", 1993,
    [("electric-relaxation-atcq", "Electric Relaxation"),
     ("award-tour-atcq", "Award Tour")],
    producer="q-tip"
))
write(SONGS / "bonita-applebum-atcq.md", song_md(
    "bonita-applebum-atcq", "Bonita Applebum", "a-tribe-called-quest",
    "peoples-instinctive-travels-atcq", 1990,
    [("q-tip", "Rapper")]
))
write(SONGS / "can-i-kick-it-atcq.md", song_md(
    "can-i-kick-it-atcq", "Can I Kick It?", "a-tribe-called-quest",
    "peoples-instinctive-travels-atcq", 1990,
    [("q-tip", "Rapper")]
))
write(SONGS / "check-the-rhime-atcq.md", song_md(
    "check-the-rhime-atcq", "Check the Rhime", "a-tribe-called-quest",
    "low-end-theory-atcq", 1991,
    [("q-tip", "Rapper"), ("phife-dawg", "Rapper")]
))
write(SONGS / "electric-relaxation-atcq.md", song_md(
    "electric-relaxation-atcq", "Electric Relaxation", "a-tribe-called-quest",
    "midnight-marauders-atcq", 1993,
    [("q-tip", "Rapper"), ("phife-dawg", "Rapper")]
))
write(SONGS / "award-tour-atcq.md", song_md(
    "award-tour-atcq", "Award Tour", "a-tribe-called-quest",
    "midnight-marauders-atcq", 1993,
    [("q-tip", "Rapper"), ("phife-dawg", "Rapper")]
))
write(PEOPLE / "q-tip.md", person_md(
    "q-tip", "Q-Tip", [("a-tribe-called-quest", "Rapper")],
    [("bonita-applebum-atcq", "Bonita Applebum", "Rapper"),
     ("can-i-kick-it-atcq", "Can I Kick It?", "Rapper"),
     ("check-the-rhime-atcq", "Check the Rhime", "Rapper"),
     ("electric-relaxation-atcq", "Electric Relaxation", "Rapper"),
     ("award-tour-atcq", "Award Tour", "Rapper")]
))
write(PEOPLE / "phife-dawg.md", person_md(
    "phife-dawg", "Phife Dawg", [("a-tribe-called-quest", "Rapper")],
    [("check-the-rhime-atcq", "Check the Rhime", "Rapper"),
     ("electric-relaxation-atcq", "Electric Relaxation", "Rapper"),
     ("award-tour-atcq", "Award Tour", "Rapper")]
))
write(PEOPLE / "ali-shaheed-muhammad.md", person_md(
    "ali-shaheed-muhammad", "Ali Shaheed Muhammad",
    [("a-tribe-called-quest", "DJ")], []
))
write(PEOPLE / "jarobi-white.md", person_md(
    "jarobi-white", "Jarobi White",
    [("a-tribe-called-quest", "Rapper")], []
))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 7 — DR. DRE
# ═══════════════════════════════════════════════════════════════════════════════
write(ARTISTS / "dr-dre.md", artist_md(
    "dr-dre", "Dr. Dre", "Solo", ["Hip-Hop"], "Hip-Hop", 1987,
    [("dr-dre-person", "Rapper")],
    ["the-chronic-dre", "2001-dre"]
))
write(ALBUMS / "the-chronic-dre.md", album_md(
    "the-chronic-dre", "The Chronic", "dr-dre", 1992,
    [("nuthin-but-a-g-thang-dre", "Nuthin' But a 'G' Thang")],
    producer="dr-dre-person"
))
write(ALBUMS / "2001-dre.md", album_md(
    "2001-dre", "2001", "dr-dre", 1999,
    [("still-dre-dre", "Still D.R.E."), ("next-episode-dre", "The Next Episode"),
     ("forget-about-dre", "Forgot About Dre")],
    producer="dr-dre-person"
))
write(SONGS / "nuthin-but-a-g-thang-dre.md", song_md(
    "nuthin-but-a-g-thang-dre", "Nuthin' But a 'G' Thang", "dr-dre",
    "the-chronic-dre", 1992,
    [("dr-dre-person", "Rapper")]
))
write(SONGS / "still-dre-dre.md", song_md(
    "still-dre-dre", "Still D.R.E.", "dr-dre", "2001-dre", 1999,
    [("dr-dre-person", "Rapper")]
))
write(SONGS / "next-episode-dre.md", song_md(
    "next-episode-dre", "The Next Episode", "dr-dre", "2001-dre", 1999,
    [("dr-dre-person", "Rapper"), ("snoop-dogg", "Vocals")]
))
write(SONGS / "forget-about-dre.md", song_md(
    "forget-about-dre", "Forgot About Dre", "dr-dre", "2001-dre", 1999,
    [("dr-dre-person", "Rapper")]
))
# DR. DRE PERSON — consolidated with section 4
write(PEOPLE / "dr-dre-person.md", person_md(
    "dr-dre-person", "Dr. Dre", [("dr-dre", "Rapper")],
    [("california-love-tupac", "California Love", "Producer"),
     ("ambitionz-az-a-ridah-tupac", "Ambitionz Az a Ridah", "Producer"),
     ("hit-em-up-tupac", "Hit 'Em Up", "Producer"),
     ("nuthin-but-a-g-thang-dre", "Nuthin' But a 'G' Thang", "Rapper"),
     ("still-dre-dre", "Still D.R.E.", "Rapper"),
     ("next-episode-dre", "The Next Episode", "Rapper"),
     ("forget-about-dre", "Forgot About Dre", "Rapper")]
))
write(PEOPLE / "snoop-dogg.md", person_md(
    "snoop-dogg", "Snoop Dogg", [],
    [("next-episode-dre", "The Next Episode", "Vocals")]
))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 8 — JAY-Z
# ═══════════════════════════════════════════════════════════════════════════════
write(ARTISTS / "jay-z.md", artist_md(
    "jay-z", "Jay-Z", "Solo", ["Hip-Hop"], "Hip-Hop", 1994,
    [("shawn-carter", "Rapper")],
    ["reasonable-doubt-jayz", "vol2-hard-knock-life-jayz", "the-blueprint-jayz"]
))
write(ALBUMS / "reasonable-doubt-jayz.md", album_md(
    "reasonable-doubt-jayz", "Reasonable Doubt", "jay-z", 1996,
    [("dead-presidents-ii-jayz", "Dead Presidents II")],
    producer="dj-premier"
))
write(ALBUMS / "vol2-hard-knock-life-jayz.md", album_md(
    "vol2-hard-knock-life-jayz", "Vol. 2... Hard Knock Life", "jay-z", 1998,
    [("hard-knock-life-jayz", "Hard Knock Life (Ghetto Anthem)")],
    producer="dj-premier"
))
write(ALBUMS / "the-blueprint-jayz.md", album_md(
    "the-blueprint-jayz", "The Blueprint", "jay-z", 2001,
    [("izzo-h-o-v-a-jayz", "Izzo (H.O.V.A.)")],
    producer="kanye-west-prod"
))
write(SONGS / "dead-presidents-ii-jayz.md", song_md(
    "dead-presidents-ii-jayz", "Dead Presidents II", "jay-z",
    "reasonable-doubt-jayz", 1996,
    [("shawn-carter", "Rapper"), ("dj-premier", "Producer")]
))
write(SONGS / "hard-knock-life-jayz.md", song_md(
    "hard-knock-life-jayz", "Hard Knock Life (Ghetto Anthem)", "jay-z",
    "vol2-hard-knock-life-jayz", 1998,
    [("shawn-carter", "Rapper"), ("dj-premier", "Producer")]
))
write(SONGS / "izzo-h-o-v-a-jayz.md", song_md(
    "izzo-h-o-v-a-jayz", "Izzo (H.O.V.A.)", "jay-z", "the-blueprint-jayz", 2001,
    [("shawn-carter", "Rapper"), ("kanye-west-prod", "Producer")]
))
write(PEOPLE / "shawn-carter.md", person_md(
    "shawn-carter", "Shawn Carter", [("jay-z", "Rapper")],
    [("dead-presidents-ii-jayz", "Dead Presidents II", "Rapper"),
     ("hard-knock-life-jayz", "Hard Knock Life (Ghetto Anthem)", "Rapper"),
     ("izzo-h-o-v-a-jayz", "Izzo (H.O.V.A.)", "Rapper")]
))
# DJ PREMIER — consolidated with section 3
write(PEOPLE / "dj-premier.md", person_md(
    "dj-premier", "DJ Premier", [],
    [("one-more-chance-big", "One More Chance", "Producer"),
     ("hypnotize-big", "Hypnotize", "Producer"),
     ("dead-presidents-ii-jayz", "Dead Presidents II", "Producer"),
     ("hard-knock-life-jayz", "Hard Knock Life (Ghetto Anthem)", "Producer")]
))
write(PEOPLE / "kanye-west-prod.md", person_md(
    "kanye-west-prod", "Kanye West", [],
    [("izzo-h-o-v-a-jayz", "Izzo (H.O.V.A.)", "Producer")]
))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 9 — BEASTIE BOYS
# ═══════════════════════════════════════════════════════════════════════════════
write(ARTISTS / "beastie-boys.md", artist_md(
    "beastie-boys", "Beastie Boys", "Group", ["Hip-Hop"], "Hip-Hop", 1981,
    [("mike-d", "Rapper"), ("ad-rock", "Rapper"), ("mca", "Rapper")],
    ["licensed-to-ill-bb", "ill-communication-bb", "hello-nasty-bb"],
    disbanded=2012
))
write(ALBUMS / "licensed-to-ill-bb.md", album_md(
    "licensed-to-ill-bb", "Licensed to Ill", "beastie-boys", 1986,
    [("fight-for-your-right-bb", "(You Gotta) Fight for Your Right (to Party!)"),
     ("no-sleep-till-brooklyn-bb", "No Sleep Till Brooklyn")],
    producer="rick-rubin"
))
write(ALBUMS / "ill-communication-bb.md", album_md(
    "ill-communication-bb", "Ill Communication", "beastie-boys", 1994,
    [("sabotage-bb", "Sabotage"), ("sure-shot-bb", "Sure Shot")]
))
write(ALBUMS / "hello-nasty-bb.md", album_md(
    "hello-nasty-bb", "Hello Nasty", "beastie-boys", 1998,
    [("intergalactic-bb", "Intergalactic")]
))
write(SONGS / "fight-for-your-right-bb.md", song_md(
    "fight-for-your-right-bb",
    "(You Gotta) Fight for Your Right (to Party!)",
    "beastie-boys", "licensed-to-ill-bb", 1986,
    [("mike-d", "Rapper"), ("rick-rubin", "Producer")]
))
write(SONGS / "no-sleep-till-brooklyn-bb.md", song_md(
    "no-sleep-till-brooklyn-bb", "No Sleep Till Brooklyn",
    "beastie-boys", "licensed-to-ill-bb", 1986,
    [("mike-d", "Rapper"), ("rick-rubin", "Producer")]
))
write(SONGS / "sabotage-bb.md", song_md(
    "sabotage-bb", "Sabotage", "beastie-boys", "ill-communication-bb", 1994,
    [("mike-d", "Writer"), ("ad-rock", "Writer")]
))
write(SONGS / "sure-shot-bb.md", song_md(
    "sure-shot-bb", "Sure Shot", "beastie-boys", "ill-communication-bb", 1994,
    [("mike-d", "Rapper")]
))
write(SONGS / "intergalactic-bb.md", song_md(
    "intergalactic-bb", "Intergalactic", "beastie-boys", "hello-nasty-bb", 1998,
    [("mike-d", "Rapper")]
))
write(PEOPLE / "mike-d.md", person_md(
    "mike-d", "Mike D", [("beastie-boys", "Rapper")],
    [("fight-for-your-right-bb",
      "(You Gotta) Fight for Your Right (to Party!)", "Rapper"),
     ("no-sleep-till-brooklyn-bb", "No Sleep Till Brooklyn", "Rapper"),
     ("sabotage-bb", "Sabotage", "Writer"),
     ("sure-shot-bb", "Sure Shot", "Rapper"),
     ("intergalactic-bb", "Intergalactic", "Rapper")]
))
write(PEOPLE / "ad-rock.md", person_md(
    "ad-rock", "Ad-Rock", [("beastie-boys", "Rapper")],
    [("sabotage-bb", "Sabotage", "Writer")]
))
write(PEOPLE / "mca.md", person_md(
    "mca", "MCA", [("beastie-boys", "Rapper")], []
))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 10 — PUBLIC ENEMY
# ═══════════════════════════════════════════════════════════════════════════════
write(ARTISTS / "public-enemy.md", artist_md(
    "public-enemy", "Public Enemy", "Group", ["Hip-Hop"], "Hip-Hop", 1985,
    [("chuck-d", "Rapper"), ("flavor-flav", "Rapper"),
     ("terminator-x", "DJ"), ("professor-griff", "Rapper")],
    ["it-takes-a-nation-pe", "fear-of-a-black-planet-pe"]
))
write(ALBUMS / "it-takes-a-nation-pe.md", album_md(
    "it-takes-a-nation-pe",
    "It Takes a Nation of Millions to Hold Us Back",
    "public-enemy", 1988,
    [("dont-believe-the-hype-pe", "Don't Believe the Hype"),
     ("public-enemy-number-one-pe", "Public Enemy No. 1")],
    producer="hank-shocklee"
))
write(ALBUMS / "fear-of-a-black-planet-pe.md", album_md(
    "fear-of-a-black-planet-pe", "Fear of a Black Planet",
    "public-enemy", 1990,
    [("fight-the-power-pe", "Fight the Power"),
     ("911-is-a-joke-pe", "911 Is a Joke")],
    producer="hank-shocklee"
))
write(SONGS / "dont-believe-the-hype-pe.md", song_md(
    "dont-believe-the-hype-pe", "Don't Believe the Hype",
    "public-enemy", "it-takes-a-nation-pe", 1988,
    [("chuck-d", "Rapper"), ("hank-shocklee", "Producer")]
))
write(SONGS / "public-enemy-number-one-pe.md", song_md(
    "public-enemy-number-one-pe", "Public Enemy No. 1",
    "public-enemy", "it-takes-a-nation-pe", 1988,
    [("chuck-d", "Rapper"), ("hank-shocklee", "Producer")]
))
write(SONGS / "fight-the-power-pe.md", song_md(
    "fight-the-power-pe", "Fight the Power",
    "public-enemy", "fear-of-a-black-planet-pe", 1989,
    [("chuck-d", "Rapper"), ("hank-shocklee", "Producer")]
))
write(SONGS / "911-is-a-joke-pe.md", song_md(
    "911-is-a-joke-pe", "911 Is a Joke",
    "public-enemy", "fear-of-a-black-planet-pe", 1990,
    [("flavor-flav", "Rapper"), ("hank-shocklee", "Producer")]
))
write(PEOPLE / "chuck-d.md", person_md(
    "chuck-d", "Chuck D", [("public-enemy", "Rapper")],
    [("dont-believe-the-hype-pe", "Don't Believe the Hype", "Rapper"),
     ("public-enemy-number-one-pe", "Public Enemy No. 1", "Rapper"),
     ("fight-the-power-pe", "Fight the Power", "Rapper")]
))
write(PEOPLE / "flavor-flav.md", person_md(
    "flavor-flav", "Flavor Flav", [("public-enemy", "Rapper")],
    [("911-is-a-joke-pe", "911 Is a Joke", "Rapper")]
))
write(PEOPLE / "terminator-x.md", person_md(
    "terminator-x", "Terminator X", [("public-enemy", "DJ")], []
))
write(PEOPLE / "professor-griff.md", person_md(
    "professor-griff", "Professor Griff", [("public-enemy", "Rapper")], []
))
write(PEOPLE / "hank-shocklee.md", person_md(
    "hank-shocklee", "Hank Shocklee", [],
    [("dont-believe-the-hype-pe", "Don't Believe the Hype", "Producer"),
     ("public-enemy-number-one-pe", "Public Enemy No. 1", "Producer"),
     ("fight-the-power-pe", "Fight the Power", "Producer"),
     ("911-is-a-joke-pe", "911 Is a Joke", "Producer")]
))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 11 — TLC
# ═══════════════════════════════════════════════════════════════════════════════
write(ARTISTS / "tlc.md", artist_md(
    "tlc", "TLC", "Group", ["R&B"], "R&B", 1990,
    [("tionne-watkins", "Vocals"), ("lisa-lopes", "Vocals"),
     ("rozonda-thomas", "Vocals")],
    ["ooooooohhh-on-the-tlc-tip", "crazysexycool-tlc", "fanmail-tlc"],
    disbanded=2002
))
write(ALBUMS / "ooooooohhh-on-the-tlc-tip.md", album_md(
    "ooooooohhh-on-the-tlc-tip", "Ooooooohhh... On the TLC Tip", "tlc", 1992,
    [("creep-tlc", "Creep")]
))
write(ALBUMS / "crazysexycool-tlc.md", album_md(
    "crazysexycool-tlc", "CrazySexyCool", "tlc", 1994,
    [("waterfalls-tlc", "Waterfalls"), ("red-light-special-tlc", "Red Light Special")],
    producer="dallas-austin"
))
write(ALBUMS / "fanmail-tlc.md", album_md(
    "fanmail-tlc", "FanMail", "tlc", 1999,
    [("no-scrubs-tlc", "No Scrubs"), ("unpretty-tlc", "Unpretty")],
    producer="dallas-austin"
))
write(SONGS / "creep-tlc.md", song_md(
    "creep-tlc", "Creep", "tlc", "ooooooohhh-on-the-tlc-tip", 1992,
    [("tionne-watkins", "Vocals"), ("dallas-austin", "Producer")]
))
write(SONGS / "waterfalls-tlc.md", song_md(
    "waterfalls-tlc", "Waterfalls", "tlc", "crazysexycool-tlc", 1995,
    [("tionne-watkins", "Vocals"), ("dallas-austin", "Producer")]
))
write(SONGS / "red-light-special-tlc.md", song_md(
    "red-light-special-tlc", "Red Light Special", "tlc", "crazysexycool-tlc", 1994,
    [("tionne-watkins", "Vocals"), ("babyface", "Writer")]
))
write(SONGS / "no-scrubs-tlc.md", song_md(
    "no-scrubs-tlc", "No Scrubs", "tlc", "fanmail-tlc", 1999,
    [("tionne-watkins", "Vocals"), ("kevin-briggs-prod", "Writer")]
))
write(SONGS / "unpretty-tlc.md", song_md(
    "unpretty-tlc", "Unpretty", "tlc", "fanmail-tlc", 1999,
    [("tionne-watkins", "Vocals"), ("lisa-lopes", "Writer")]
))
write(PEOPLE / "tionne-watkins.md", person_md(
    "tionne-watkins", "Tionne Watkins", [("tlc", "Vocals")],
    [("creep-tlc", "Creep", "Vocals"),
     ("waterfalls-tlc", "Waterfalls", "Vocals"),
     ("red-light-special-tlc", "Red Light Special", "Vocals"),
     ("no-scrubs-tlc", "No Scrubs", "Vocals"),
     ("unpretty-tlc", "Unpretty", "Vocals")]
))
write(PEOPLE / "lisa-lopes.md", person_md(
    "lisa-lopes", "Lisa Lopes", [("tlc", "Vocals")],
    [("unpretty-tlc", "Unpretty", "Writer")]
))
write(PEOPLE / "rozonda-thomas.md", person_md(
    "rozonda-thomas", "Rozonda Thomas", [("tlc", "Vocals")], []
))
write(PEOPLE / "dallas-austin.md", person_md(
    "dallas-austin", "Dallas Austin", [],
    [("creep-tlc", "Creep", "Producer"),
     ("waterfalls-tlc", "Waterfalls", "Producer")]
))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 12 — MARIAH CAREY
# ═══════════════════════════════════════════════════════════════════════════════
write(ARTISTS / "mariah-carey.md", artist_md(
    "mariah-carey", "Mariah Carey", "Solo", ["Pop"], "Pop", 1990,
    [("mariah-carey-person", "Vocals")],
    ["mariah-carey-album", "music-box-mc", "merry-christmas-mc",
     "daydream-mc", "emancipation-of-mimi-mc"]
))
write(ALBUMS / "mariah-carey-album.md", album_md(
    "mariah-carey-album", "Mariah Carey", "mariah-carey", 1990,
    [("vision-of-love-mc", "Vision of Love")],
    producer="walter-afanasieff"
))
write(ALBUMS / "music-box-mc.md", album_md(
    "music-box-mc", "Music Box", "mariah-carey", 1993,
    [("dreamlover-mc", "Dreamlover"), ("hero-mc", "Hero")],
    producer="walter-afanasieff"
))
write(ALBUMS / "merry-christmas-mc.md", album_md(
    "merry-christmas-mc", "Merry Christmas", "mariah-carey", 1994,
    [("all-i-want-for-christmas-mc", "All I Want for Christmas Is You")],
    producer="walter-afanasieff"
))
write(ALBUMS / "daydream-mc.md", album_md(
    "daydream-mc", "Daydream", "mariah-carey", 1995,
    [("fantasy-mc", "Fantasy"), ("one-sweet-day-mc", "One Sweet Day"),
     ("always-be-my-baby-mc", "Always Be My Baby")],
    producer="walter-afanasieff"
))
write(ALBUMS / "emancipation-of-mimi-mc.md", album_md(
    "emancipation-of-mimi-mc", "The Emancipation of Mimi", "mariah-carey", 2005,
    [("we-belong-together-mc", "We Belong Together")]
))
write(SONGS / "vision-of-love-mc.md", song_md(
    "vision-of-love-mc", "Vision of Love", "mariah-carey",
    "mariah-carey-album", 1990,
    [("mariah-carey-person", "Vocals"), ("walter-afanasieff", "Producer")]
))
write(SONGS / "dreamlover-mc.md", song_md(
    "dreamlover-mc", "Dreamlover", "mariah-carey", "music-box-mc", 1993,
    [("mariah-carey-person", "Vocals"), ("walter-afanasieff", "Producer")]
))
write(SONGS / "hero-mc.md", song_md(
    "hero-mc", "Hero", "mariah-carey", "music-box-mc", 1993,
    [("mariah-carey-person", "Vocals"), ("walter-afanasieff", "Producer")]
))
write(SONGS / "all-i-want-for-christmas-mc.md", song_md(
    "all-i-want-for-christmas-mc", "All I Want for Christmas Is You",
    "mariah-carey", "merry-christmas-mc", 1994,
    [("mariah-carey-person", "Vocals"), ("walter-afanasieff", "Writer")]
))
write(SONGS / "fantasy-mc.md", song_md(
    "fantasy-mc", "Fantasy", "mariah-carey", "daydream-mc", 1995,
    [("mariah-carey-person", "Vocals"), ("walter-afanasieff", "Producer")]
))
write(SONGS / "one-sweet-day-mc.md", song_md(
    "one-sweet-day-mc", "One Sweet Day", "mariah-carey", "daydream-mc", 1995,
    [("mariah-carey-person", "Vocals"), ("walter-afanasieff", "Producer")]
))
write(SONGS / "always-be-my-baby-mc.md", song_md(
    "always-be-my-baby-mc", "Always Be My Baby", "mariah-carey", "daydream-mc", 1995,
    [("mariah-carey-person", "Vocals"), ("walter-afanasieff", "Producer")]
))
write(SONGS / "we-belong-together-mc.md", song_md(
    "we-belong-together-mc", "We Belong Together", "mariah-carey",
    "emancipation-of-mimi-mc", 2005,
    [("mariah-carey-person", "Vocals"), ("mariah-carey-person", "Writer")]
))
write(PEOPLE / "mariah-carey-person.md", person_md(
    "mariah-carey-person", "Mariah Carey", [("mariah-carey", "Vocals")],
    [("vision-of-love-mc", "Vision of Love", "Vocals"),
     ("dreamlover-mc", "Dreamlover", "Vocals"),
     ("hero-mc", "Hero", "Vocals"),
     ("all-i-want-for-christmas-mc", "All I Want for Christmas Is You", "Vocals"),
     ("fantasy-mc", "Fantasy", "Vocals"),
     ("one-sweet-day-mc", "One Sweet Day", "Vocals"),
     ("always-be-my-baby-mc", "Always Be My Baby", "Vocals"),
     ("we-belong-together-mc", "We Belong Together", "Vocals")]
))
write(PEOPLE / "walter-afanasieff.md", person_md(
    "walter-afanasieff", "Walter Afanasieff", [],
    [("vision-of-love-mc", "Vision of Love", "Producer"),
     ("dreamlover-mc", "Dreamlover", "Producer"),
     ("hero-mc", "Hero", "Producer"),
     ("all-i-want-for-christmas-mc", "All I Want for Christmas Is You", "Writer"),
     ("fantasy-mc", "Fantasy", "Producer"),
     ("one-sweet-day-mc", "One Sweet Day", "Producer"),
     ("always-be-my-baby-mc", "Always Be My Baby", "Producer")]
))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 13 — WHITNEY HOUSTON
# ═══════════════════════════════════════════════════════════════════════════════
write(ARTISTS / "whitney-houston.md", artist_md(
    "whitney-houston", "Whitney Houston", "Solo", ["Pop"], "Pop", 1983,
    [("whitney-houston-person", "Vocals")],
    ["whitney-houston-album", "whitney-1987", "the-bodyguard-wh",
     "my-love-is-your-love-wh"],
    disbanded=2012
))
write(ALBUMS / "whitney-houston-album.md", album_md(
    "whitney-houston-album", "Whitney Houston", "whitney-houston", 1985,
    [("greatest-love-of-all-wh", "Greatest Love of All")]
))
write(ALBUMS / "whitney-1987.md", album_md(
    "whitney-1987", "Whitney", "whitney-houston", 1987,
    [("i-wanna-dance-with-somebody-wh", "I Wanna Dance with Somebody (Who Loves Me)")]
))
write(ALBUMS / "the-bodyguard-wh.md", album_md(
    "the-bodyguard-wh", "The Bodyguard: Original Soundtrack Album",
    "whitney-houston", 1992,
    [("i-will-always-love-you-wh", "I Will Always Love You")]
))
write(ALBUMS / "my-love-is-your-love-wh.md", album_md(
    "my-love-is-your-love-wh", "My Love Is Your Love", "whitney-houston", 1998,
    [("exhale-shoop-wh", "Exhale (Shoop Shoop)")],
    producer="babyface"
))
write(SONGS / "greatest-love-of-all-wh.md", song_md(
    "greatest-love-of-all-wh", "Greatest Love of All", "whitney-houston",
    "whitney-houston-album", 1985,
    [("whitney-houston-person", "Vocals")]
))
write(SONGS / "i-wanna-dance-with-somebody-wh.md", song_md(
    "i-wanna-dance-with-somebody-wh",
    "I Wanna Dance with Somebody (Who Loves Me)",
    "whitney-houston", "whitney-1987", 1987,
    [("whitney-houston-person", "Vocals")]
))
write(SONGS / "i-will-always-love-you-wh.md", song_md(
    "i-will-always-love-you-wh", "I Will Always Love You", "whitney-houston",
    "the-bodyguard-wh", 1992,
    [("whitney-houston-person", "Vocals")]
))
write(SONGS / "exhale-shoop-wh.md", song_md(
    "exhale-shoop-wh", "Exhale (Shoop Shoop)", "whitney-houston",
    "my-love-is-your-love-wh", 1995,
    [("whitney-houston-person", "Vocals"), ("babyface", "Writer")]
))
write(PEOPLE / "whitney-houston-person.md", person_md(
    "whitney-houston-person", "Whitney Houston", [("whitney-houston", "Vocals")],
    [("greatest-love-of-all-wh", "Greatest Love of All", "Vocals"),
     ("i-wanna-dance-with-somebody-wh",
      "I Wanna Dance with Somebody (Who Loves Me)", "Vocals"),
     ("i-will-always-love-you-wh", "I Will Always Love You", "Vocals"),
     ("exhale-shoop-wh", "Exhale (Shoop Shoop)", "Vocals")]
))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 14 — BOYZ II MEN
# ═══════════════════════════════════════════════════════════════════════════════
write(ARTISTS / "boyz-ii-men.md", artist_md(
    "boyz-ii-men", "Boyz II Men", "Group", ["R&B"], "R&B", 1988,
    [("wanya-morris", "Vocals"), ("michael-mccary", "Vocals"),
     ("nathan-morris", "Vocals"), ("shawn-stockman", "Vocals")],
    ["cooleyhighharmony-b2m", "ii-b2m", "evolution-b2m"]
))
write(ALBUMS / "cooleyhighharmony-b2m.md", album_md(
    "cooleyhighharmony-b2m", "Cooleyhighharmony", "boyz-ii-men", 1991,
    [("motownphilly-b2m", "Motownphilly"),
     ("end-of-the-road-b2m", "End of the Road")]
))
write(ALBUMS / "ii-b2m.md", album_md(
    "ii-b2m", "II", "boyz-ii-men", 1994,
    [("ill-make-love-to-you-b2m", "I'll Make Love to You"),
     ("on-bended-knee-b2m", "On Bended Knee")],
    producer="babyface"
))
write(ALBUMS / "evolution-b2m.md", album_md(
    "evolution-b2m", "Evolution", "boyz-ii-men", 1997,
    [("a-song-for-mama-b2m", "A Song for Mama")],
    producer="babyface"
))
write(SONGS / "motownphilly-b2m.md", song_md(
    "motownphilly-b2m", "Motownphilly", "boyz-ii-men",
    "cooleyhighharmony-b2m", 1991,
    [("wanya-morris", "Vocals")]
))
write(SONGS / "end-of-the-road-b2m.md", song_md(
    "end-of-the-road-b2m", "End of the Road", "boyz-ii-men",
    "cooleyhighharmony-b2m", 1992,
    [("wanya-morris", "Vocals"), ("babyface", "Writer")]
))
write(SONGS / "ill-make-love-to-you-b2m.md", song_md(
    "ill-make-love-to-you-b2m", "I'll Make Love to You", "boyz-ii-men",
    "ii-b2m", 1994,
    [("wanya-morris", "Vocals"), ("babyface", "Writer")]
))
write(SONGS / "on-bended-knee-b2m.md", song_md(
    "on-bended-knee-b2m", "On Bended Knee", "boyz-ii-men", "ii-b2m", 1994,
    [("wanya-morris", "Vocals"), ("babyface", "Writer")]
))
write(SONGS / "a-song-for-mama-b2m.md", song_md(
    "a-song-for-mama-b2m", "A Song for Mama", "boyz-ii-men",
    "evolution-b2m", 1997,
    [("wanya-morris", "Vocals"), ("babyface", "Writer")]
))
write(PEOPLE / "wanya-morris.md", person_md(
    "wanya-morris", "Wanya Morris", [("boyz-ii-men", "Vocals")],
    [("motownphilly-b2m", "Motownphilly", "Vocals"),
     ("end-of-the-road-b2m", "End of the Road", "Vocals"),
     ("ill-make-love-to-you-b2m", "I'll Make Love to You", "Vocals"),
     ("on-bended-knee-b2m", "On Bended Knee", "Vocals"),
     ("a-song-for-mama-b2m", "A Song for Mama", "Vocals")]
))
write(PEOPLE / "michael-mccary.md", person_md(
    "michael-mccary", "Michael McCary", [("boyz-ii-men", "Vocals")], []
))
write(PEOPLE / "nathan-morris.md", person_md(
    "nathan-morris", "Nathan Morris", [("boyz-ii-men", "Vocals")], []
))
write(PEOPLE / "shawn-stockman.md", person_md(
    "shawn-stockman", "Shawn Stockman", [("boyz-ii-men", "Vocals")], []
))
# BABYFACE — consolidated across sections 11, 13, 14
write(PEOPLE / "babyface.md", person_md(
    "babyface", "Babyface", [],
    [("red-light-special-tlc", "Red Light Special", "Writer"),
     ("exhale-shoop-wh", "Exhale (Shoop Shoop)", "Writer"),
     ("end-of-the-road-b2m", "End of the Road", "Writer"),
     ("ill-make-love-to-you-b2m", "I'll Make Love to You", "Writer"),
     ("on-bended-knee-b2m", "On Bended Knee", "Writer"),
     ("a-song-for-mama-b2m", "A Song for Mama", "Writer")]
))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 15 — DESTINY'S CHILD
# ═══════════════════════════════════════════════════════════════════════════════
write(ARTISTS / "destinys-child.md", artist_md(
    "destinys-child", "Destiny's Child", "Group", ["R&B"], "R&B", 1990,
    [("beyonce-person", "Vocals"), ("kelly-rowland", "Vocals"),
     ("michelle-williams-dc", "Vocals")],
    ["the-writings-on-the-wall-dc", "survivor-dc"],
    disbanded=2006
))
write(ALBUMS / "the-writings-on-the-wall-dc.md", album_md(
    "the-writings-on-the-wall-dc", "The Writing's on the Wall",
    "destinys-child", 1999,
    [("bills-bills-bills-dc", "Bills, Bills, Bills"),
     ("say-my-name-dc", "Say My Name")],
    producer="kevin-briggs-prod"
))
write(ALBUMS / "survivor-dc.md", album_md(
    "survivor-dc", "Survivor", "destinys-child", 2001,
    [("survivor-dc-song", "Survivor"), ("bootylicious-dc", "Bootylicious"),
     ("independent-women-dc", "Independent Women Part I")]
))
write(SONGS / "bills-bills-bills-dc.md", song_md(
    "bills-bills-bills-dc", "Bills, Bills, Bills", "destinys-child",
    "the-writings-on-the-wall-dc", 1999,
    [("beyonce-person", "Vocals"), ("kevin-briggs-prod", "Writer")]
))
write(SONGS / "say-my-name-dc.md", song_md(
    "say-my-name-dc", "Say My Name", "destinys-child",
    "the-writings-on-the-wall-dc", 1999,
    [("beyonce-person", "Vocals"), ("rodney-jerkins", "Producer")]
))
write(SONGS / "survivor-dc-song.md", song_md(
    "survivor-dc-song", "Survivor", "destinys-child", "survivor-dc", 2001,
    [("beyonce-person", "Vocals"), ("beyonce-person", "Writer")]
))
write(SONGS / "bootylicious-dc.md", song_md(
    "bootylicious-dc", "Bootylicious", "destinys-child", "survivor-dc", 2001,
    [("beyonce-person", "Vocals"), ("beyonce-person", "Writer")]
))
write(SONGS / "independent-women-dc.md", song_md(
    "independent-women-dc", "Independent Women Part I", "destinys-child",
    "survivor-dc", 2000,
    [("beyonce-person", "Vocals"), ("beyonce-person", "Writer")]
))
write(PEOPLE / "kelly-rowland.md", person_md(
    "kelly-rowland", "Kelly Rowland", [("destinys-child", "Vocals")], []
))
write(PEOPLE / "michelle-williams-dc.md", person_md(
    "michelle-williams-dc", "Michelle Williams", [("destinys-child", "Vocals")], []
))
# KEVIN BRIGGS — consolidated across sections 11 and 15
write(PEOPLE / "kevin-briggs-prod.md", person_md(
    "kevin-briggs-prod", "Kevin 'She'kspere' Briggs", [],
    [("no-scrubs-tlc", "No Scrubs", "Writer"),
     ("bills-bills-bills-dc", "Bills, Bills, Bills", "Writer")]
))
write(PEOPLE / "rodney-jerkins.md", person_md(
    "rodney-jerkins", "Rodney Jerkins", [],
    [("say-my-name-dc", "Say My Name", "Producer"),
     ("holler-sg", "Holler", "Producer")]
))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 16 — BACKSTREET BOYS
# ═══════════════════════════════════════════════════════════════════════════════
write(ARTISTS / "backstreet-boys.md", artist_md(
    "backstreet-boys", "Backstreet Boys", "Group", ["Pop"], "Pop", 1993,
    [("aj-mclean", "Vocals"), ("howie-dorough", "Vocals"),
     ("nick-carter-bsb", "Vocals"), ("kevin-richardson", "Vocals"),
     ("brian-littrell", "Vocals")],
    ["backstreet-boys-album", "millennium-bsb"]
))
write(ALBUMS / "backstreet-boys-album.md", album_md(
    "backstreet-boys-album", "Backstreet Boys", "backstreet-boys", 1996,
    [("quit-playing-games-bsb", "Quit Playin' Games (With My Heart)"),
     ("as-long-as-you-love-me-bsb", "As Long as You Love Me"),
     ("everybody-bsb", "Everybody (Backstreet's Back)")],
    producer="denniz-pop"
))
write(ALBUMS / "millennium-bsb.md", album_md(
    "millennium-bsb", "Millennium", "backstreet-boys", 1999,
    [("i-want-it-that-way-bsb", "I Want It That Way"),
     ("larger-than-life-bsb", "Larger Than Life")],
    producer="max-martin"
))
write(SONGS / "quit-playing-games-bsb.md", song_md(
    "quit-playing-games-bsb", "Quit Playin' Games (With My Heart)",
    "backstreet-boys", "backstreet-boys-album", 1996,
    [("aj-mclean", "Vocals"), ("max-martin", "Writer"), ("denniz-pop", "Producer")]
))
write(SONGS / "as-long-as-you-love-me-bsb.md", song_md(
    "as-long-as-you-love-me-bsb", "As Long as You Love Me",
    "backstreet-boys", "backstreet-boys-album", 1996,
    [("aj-mclean", "Vocals"), ("max-martin", "Writer"), ("denniz-pop", "Producer")]
))
write(SONGS / "everybody-bsb.md", song_md(
    "everybody-bsb", "Everybody (Backstreet's Back)",
    "backstreet-boys", "backstreet-boys-album", 1997,
    [("aj-mclean", "Vocals"), ("max-martin", "Writer"), ("denniz-pop", "Producer")]
))
write(SONGS / "i-want-it-that-way-bsb.md", song_md(
    "i-want-it-that-way-bsb", "I Want It That Way",
    "backstreet-boys", "millennium-bsb", 1999,
    [("aj-mclean", "Vocals"), ("max-martin", "Writer")]
))
write(SONGS / "larger-than-life-bsb.md", song_md(
    "larger-than-life-bsb", "Larger Than Life",
    "backstreet-boys", "millennium-bsb", 1999,
    [("aj-mclean", "Vocals"), ("max-martin", "Writer")]
))
write(PEOPLE / "aj-mclean.md", person_md(
    "aj-mclean", "AJ McLean", [("backstreet-boys", "Vocals")],
    [("quit-playing-games-bsb", "Quit Playin' Games (With My Heart)", "Vocals"),
     ("as-long-as-you-love-me-bsb", "As Long as You Love Me", "Vocals"),
     ("everybody-bsb", "Everybody (Backstreet's Back)", "Vocals"),
     ("i-want-it-that-way-bsb", "I Want It That Way", "Vocals"),
     ("larger-than-life-bsb", "Larger Than Life", "Vocals")]
))
write(PEOPLE / "howie-dorough.md", person_md(
    "howie-dorough", "Howie Dorough", [("backstreet-boys", "Vocals")], []
))
write(PEOPLE / "nick-carter-bsb.md", person_md(
    "nick-carter-bsb", "Nick Carter", [("backstreet-boys", "Vocals")], []
))
write(PEOPLE / "kevin-richardson.md", person_md(
    "kevin-richardson", "Kevin Richardson", [("backstreet-boys", "Vocals")], []
))
write(PEOPLE / "brian-littrell.md", person_md(
    "brian-littrell", "Brian Littrell", [("backstreet-boys", "Vocals")], []
))
# DENNIZ POP — consolidated across sections 16 and 17
write(PEOPLE / "denniz-pop.md", person_md(
    "denniz-pop", "Denniz Pop", [],
    [("quit-playing-games-bsb", "Quit Playin' Games (With My Heart)", "Producer"),
     ("as-long-as-you-love-me-bsb", "As Long as You Love Me", "Producer"),
     ("everybody-bsb", "Everybody (Backstreet's Back)", "Producer"),
     ("i-want-you-back-nsync", "I Want You Back", "Producer"),
     ("tearin-up-my-heart-nsync", "Tearing Up My Heart", "Producer")]
))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 17 — NSYNC
# ═══════════════════════════════════════════════════════════════════════════════
write(ARTISTS / "nsync.md", artist_md(
    "nsync", "NSYNC", "Group", ["Pop"], "Pop", 1995,
    [("justin-timberlake", "Vocals"), ("jc-chasez", "Vocals"),
     ("chris-kirkpatrick", "Vocals"), ("joey-fatone", "Vocals"),
     ("lance-bass", "Vocals")],
    ["nsync-album", "no-strings-attached-nsync"],
    disbanded=2002
))
write(ALBUMS / "nsync-album.md", album_md(
    "nsync-album", "NSYNC", "nsync", 1997,
    [("i-want-you-back-nsync", "I Want You Back"),
     ("tearin-up-my-heart-nsync", "Tearing Up My Heart")],
    producer="denniz-pop"
))
write(ALBUMS / "no-strings-attached-nsync.md", album_md(
    "no-strings-attached-nsync", "No Strings Attached", "nsync", 2000,
    [("bye-bye-bye-nsync", "Bye Bye Bye"),
     ("it-s-gonna-be-me-nsync", "It's Gonna Be Me")],
    producer="max-martin"
))
write(SONGS / "i-want-you-back-nsync.md", song_md(
    "i-want-you-back-nsync", "I Want You Back", "nsync", "nsync-album", 1996,
    [("justin-timberlake", "Vocals"), ("max-martin", "Writer"),
     ("denniz-pop", "Producer")]
))
write(SONGS / "tearin-up-my-heart-nsync.md", song_md(
    "tearin-up-my-heart-nsync", "Tearing Up My Heart", "nsync", "nsync-album", 1997,
    [("justin-timberlake", "Vocals"), ("max-martin", "Writer"),
     ("denniz-pop", "Producer")]
))
write(SONGS / "bye-bye-bye-nsync.md", song_md(
    "bye-bye-bye-nsync", "Bye Bye Bye", "nsync", "no-strings-attached-nsync", 2000,
    [("justin-timberlake", "Vocals"), ("max-martin", "Writer")]
))
write(SONGS / "it-s-gonna-be-me-nsync.md", song_md(
    "it-s-gonna-be-me-nsync", "It's Gonna Be Me", "nsync",
    "no-strings-attached-nsync", 2000,
    [("justin-timberlake", "Vocals"), ("max-martin", "Writer")]
))
write(PEOPLE / "justin-timberlake.md", person_md(
    "justin-timberlake", "Justin Timberlake", [("nsync", "Vocals")],
    [("i-want-you-back-nsync", "I Want You Back", "Vocals"),
     ("tearin-up-my-heart-nsync", "Tearing Up My Heart", "Vocals"),
     ("bye-bye-bye-nsync", "Bye Bye Bye", "Vocals"),
     ("it-s-gonna-be-me-nsync", "It's Gonna Be Me", "Vocals")]
))
write(PEOPLE / "jc-chasez.md", person_md(
    "jc-chasez", "JC Chasez", [("nsync", "Vocals")], []
))
write(PEOPLE / "chris-kirkpatrick.md", person_md(
    "chris-kirkpatrick", "Chris Kirkpatrick", [("nsync", "Vocals")], []
))
write(PEOPLE / "joey-fatone.md", person_md(
    "joey-fatone", "Joey Fatone", [("nsync", "Vocals")], []
))
write(PEOPLE / "lance-bass.md", person_md(
    "lance-bass", "Lance Bass", [("nsync", "Vocals")], []
))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 18 — SPICE GIRLS
# ═══════════════════════════════════════════════════════════════════════════════
write(ARTISTS / "spice-girls.md", artist_md(
    "spice-girls", "Spice Girls", "Group", ["Pop"], "Pop", 1994,
    [("victoria-beckham", "Vocals"), ("melanie-brown", "Vocals"),
     ("emma-bunton", "Vocals"), ("melanie-chisholm", "Vocals"),
     ("geri-halliwell", "Vocals")],
    ["spice-sg", "spiceworld-sg", "forever-sg"],
    disbanded=2000
))
write(ALBUMS / "spice-sg.md", album_md(
    "spice-sg", "Spice", "spice-girls", 1996,
    [("wannabe-sg", "Wannabe"), ("say-youll-be-there-sg", "Say You'll Be There"),
     ("2-become-1-sg", "2 Become 1"), ("too-much-sg", "Too Much")],
    producer="richard-stannard"
))
write(ALBUMS / "spiceworld-sg.md", album_md(
    "spiceworld-sg", "Spiceworld", "spice-girls", 1997,
    [("spice-up-your-life-sg", "Spice Up Your Life")],
    producer="richard-stannard"
))
write(ALBUMS / "forever-sg.md", album_md(
    "forever-sg", "Forever", "spice-girls", 2000,
    [("holler-sg", "Holler")],
    producer="rodney-jerkins"
))
write(SONGS / "wannabe-sg.md", song_md(
    "wannabe-sg", "Wannabe", "spice-girls", "spice-sg", 1996,
    [("victoria-beckham", "Vocals"), ("richard-stannard", "Writer"),
     ("matt-rowe", "Writer")]
))
write(SONGS / "say-youll-be-there-sg.md", song_md(
    "say-youll-be-there-sg", "Say You'll Be There", "spice-girls", "spice-sg", 1996,
    [("victoria-beckham", "Vocals"), ("richard-stannard", "Writer")]
))
write(SONGS / "2-become-1-sg.md", song_md(
    "2-become-1-sg", "2 Become 1", "spice-girls", "spice-sg", 1996,
    [("victoria-beckham", "Vocals"), ("richard-stannard", "Writer"),
     ("matt-rowe", "Writer")]
))
write(SONGS / "too-much-sg.md", song_md(
    "too-much-sg", "Too Much", "spice-girls", "spice-sg", 1996,
    [("victoria-beckham", "Vocals"), ("richard-stannard", "Writer"),
     ("matt-rowe", "Writer")]
))
write(SONGS / "spice-up-your-life-sg.md", song_md(
    "spice-up-your-life-sg", "Spice Up Your Life", "spice-girls",
    "spiceworld-sg", 1997,
    [("victoria-beckham", "Vocals"), ("richard-stannard", "Writer"),
     ("matt-rowe", "Writer")]
))
write(SONGS / "holler-sg.md", song_md(
    "holler-sg", "Holler", "spice-girls", "forever-sg", 2000,
    [("victoria-beckham", "Vocals"), ("rodney-jerkins", "Writer")]
))
write(PEOPLE / "victoria-beckham.md", person_md(
    "victoria-beckham", "Victoria Beckham", [("spice-girls", "Vocals")],
    [("wannabe-sg", "Wannabe", "Vocals"),
     ("say-youll-be-there-sg", "Say You'll Be There", "Vocals"),
     ("2-become-1-sg", "2 Become 1", "Vocals"),
     ("too-much-sg", "Too Much", "Vocals"),
     ("spice-up-your-life-sg", "Spice Up Your Life", "Vocals"),
     ("holler-sg", "Holler", "Vocals")]
))
write(PEOPLE / "melanie-brown.md", person_md(
    "melanie-brown", "Melanie Brown", [("spice-girls", "Vocals")], []
))
write(PEOPLE / "emma-bunton.md", person_md(
    "emma-bunton", "Emma Bunton", [("spice-girls", "Vocals")], []
))
write(PEOPLE / "melanie-chisholm.md", person_md(
    "melanie-chisholm", "Melanie Chisholm", [("spice-girls", "Vocals")], []
))
write(PEOPLE / "geri-halliwell.md", person_md(
    "geri-halliwell", "Geri Halliwell", [("spice-girls", "Vocals")], []
))
write(PEOPLE / "richard-stannard.md", person_md(
    "richard-stannard", "Richard Stannard", [],
    [("wannabe-sg", "Wannabe", "Writer"),
     ("say-youll-be-there-sg", "Say You'll Be There", "Writer"),
     ("2-become-1-sg", "2 Become 1", "Writer"),
     ("too-much-sg", "Too Much", "Writer"),
     ("spice-up-your-life-sg", "Spice Up Your Life", "Writer")]
))
write(PEOPLE / "matt-rowe.md", person_md(
    "matt-rowe", "Matt Rowe", [],
    [("wannabe-sg", "Wannabe", "Writer"),
     ("2-become-1-sg", "2 Become 1", "Writer"),
     ("too-much-sg", "Too Much", "Writer"),
     ("spice-up-your-life-sg", "Spice Up Your Life", "Writer")]
))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 19 — FIONA APPLE
# ═══════════════════════════════════════════════════════════════════════════════
write(ARTISTS / "fiona-apple.md", artist_md(
    "fiona-apple", "Fiona Apple", "Solo", ["Alternative Rock"], "Alternative Rock",
    1994,
    [("fiona-apple-person", "Vocals")],
    ["tidal-fa", "when-the-pawn-fa", "extraordinary-machine-fa"]
))
write(ALBUMS / "tidal-fa.md", album_md(
    "tidal-fa", "Tidal", "fiona-apple", 1996,
    [("criminal-fa", "Criminal"), ("shadowboxer-fa", "Shadowboxer")],
    producer="jon-brion"
))
write(ALBUMS / "when-the-pawn-fa.md", album_md(
    "when-the-pawn-fa", "When the Pawn...", "fiona-apple", 1999,
    [("fast-as-you-can-fa", "Fast As You Can"), ("paper-bag-fa", "Paper Bag")],
    producer="jon-brion"
))
write(ALBUMS / "extraordinary-machine-fa.md", album_md(
    "extraordinary-machine-fa", "Extraordinary Machine", "fiona-apple", 2005,
    [("not-about-love-fa", "Not About Love")],
    producer="mike-elizondo"
))
write(SONGS / "criminal-fa.md", song_md(
    "criminal-fa", "Criminal", "fiona-apple", "tidal-fa", 1996,
    [("fiona-apple-person", "Vocals"), ("jon-brion", "Producer")]
))
write(SONGS / "shadowboxer-fa.md", song_md(
    "shadowboxer-fa", "Shadowboxer", "fiona-apple", "tidal-fa", 1996,
    [("fiona-apple-person", "Vocals"), ("jon-brion", "Producer")]
))
write(SONGS / "fast-as-you-can-fa.md", song_md(
    "fast-as-you-can-fa", "Fast As You Can", "fiona-apple",
    "when-the-pawn-fa", 1999,
    [("fiona-apple-person", "Vocals"), ("jon-brion", "Producer")]
))
write(SONGS / "paper-bag-fa.md", song_md(
    "paper-bag-fa", "Paper Bag", "fiona-apple", "when-the-pawn-fa", 1999,
    [("fiona-apple-person", "Vocals"), ("jon-brion", "Producer")]
))
write(SONGS / "not-about-love-fa.md", song_md(
    "not-about-love-fa", "Not About Love", "fiona-apple",
    "extraordinary-machine-fa", 2005,
    [("fiona-apple-person", "Vocals"), ("mike-elizondo", "Producer")]
))
write(PEOPLE / "fiona-apple-person.md", person_md(
    "fiona-apple-person", "Fiona Apple", [("fiona-apple", "Vocals")],
    [("criminal-fa", "Criminal", "Vocals"),
     ("shadowboxer-fa", "Shadowboxer", "Vocals"),
     ("fast-as-you-can-fa", "Fast As You Can", "Vocals"),
     ("paper-bag-fa", "Paper Bag", "Vocals"),
     ("not-about-love-fa", "Not About Love", "Vocals")]
))
write(PEOPLE / "jon-brion.md", person_md(
    "jon-brion", "Jon Brion", [],
    [("criminal-fa", "Criminal", "Producer"),
     ("shadowboxer-fa", "Shadowboxer", "Producer"),
     ("fast-as-you-can-fa", "Fast As You Can", "Producer"),
     ("paper-bag-fa", "Paper Bag", "Producer")]
))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 20 — MATCHBOX TWENTY
# ═══════════════════════════════════════════════════════════════════════════════
write(ARTISTS / "matchbox-twenty.md", artist_md(
    "matchbox-twenty", "Matchbox Twenty", "Group", ["Alternative Rock"],
    "Alternative Rock", 1995,
    [("rob-thomas", "Vocals"), ("kyle-cook", "Guitar"),
     ("paul-doucette", "Drums"), ("brian-yale", "Bass"),
     ("adam-gaynor", "Guitar")],
    ["yourself-or-someone-like-you-mb20", "mad-season-mb20",
     "more-than-you-think-you-are-mb20"]
))
write(ALBUMS / "yourself-or-someone-like-you-mb20.md", album_md(
    "yourself-or-someone-like-you-mb20", "Yourself or Someone Like You",
    "matchbox-twenty", 1996,
    [("3-am-mb20", "3 A.M."), ("push-mb20", "Push"), ("real-world-mb20", "Real World")],
    producer="matt-serletic"
))
write(ALBUMS / "mad-season-mb20.md", album_md(
    "mad-season-mb20", "Mad Season", "matchbox-twenty", 2000,
    [("bent-mb20", "Bent")],
    producer="matt-serletic"
))
write(ALBUMS / "more-than-you-think-you-are-mb20.md", album_md(
    "more-than-you-think-you-are-mb20", "More Than You Think You Are",
    "matchbox-twenty", 2002,
    [("unwell-mb20", "Unwell")],
    producer="matt-serletic"
))
write(SONGS / "3-am-mb20.md", song_md(
    "3-am-mb20", "3 A.M.", "matchbox-twenty",
    "yourself-or-someone-like-you-mb20", 1996,
    [("rob-thomas", "Vocals"), ("matt-serletic", "Producer")]
))
write(SONGS / "push-mb20.md", song_md(
    "push-mb20", "Push", "matchbox-twenty",
    "yourself-or-someone-like-you-mb20", 1996,
    [("rob-thomas", "Vocals"), ("matt-serletic", "Producer")]
))
write(SONGS / "real-world-mb20.md", song_md(
    "real-world-mb20", "Real World", "matchbox-twenty",
    "yourself-or-someone-like-you-mb20", 1997,
    [("rob-thomas", "Vocals"), ("matt-serletic", "Producer")]
))
write(SONGS / "bent-mb20.md", song_md(
    "bent-mb20", "Bent", "matchbox-twenty", "mad-season-mb20", 2000,
    [("rob-thomas", "Vocals"), ("matt-serletic", "Producer")]
))
write(SONGS / "unwell-mb20.md", song_md(
    "unwell-mb20", "Unwell", "matchbox-twenty",
    "more-than-you-think-you-are-mb20", 2002,
    [("rob-thomas", "Vocals"), ("matt-serletic", "Producer")]
))
write(PEOPLE / "rob-thomas.md", person_md(
    "rob-thomas", "Rob Thomas", [("matchbox-twenty", "Vocals")],
    [("3-am-mb20", "3 A.M.", "Vocals"),
     ("push-mb20", "Push", "Vocals"),
     ("real-world-mb20", "Real World", "Vocals"),
     ("bent-mb20", "Bent", "Vocals"),
     ("unwell-mb20", "Unwell", "Vocals")]
))
write(PEOPLE / "kyle-cook.md", person_md(
    "kyle-cook", "Kyle Cook", [("matchbox-twenty", "Guitar")], []
))
write(PEOPLE / "paul-doucette.md", person_md(
    "paul-doucette", "Paul Doucette", [("matchbox-twenty", "Drums")], []
))
write(PEOPLE / "brian-yale.md", person_md(
    "brian-yale", "Brian Yale", [("matchbox-twenty", "Bass")], []
))
write(PEOPLE / "adam-gaynor.md", person_md(
    "adam-gaynor", "Adam Gaynor", [("matchbox-twenty", "Guitar")], []
))
write(PEOPLE / "matt-serletic.md", person_md(
    "matt-serletic", "Matt Serletic", [],
    [("3-am-mb20", "3 A.M.", "Producer"),
     ("push-mb20", "Push", "Producer"),
     ("real-world-mb20", "Real World", "Producer"),
     ("bent-mb20", "Bent", "Producer"),
     ("unwell-mb20", "Unwell", "Producer")]
))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 21 — THIRD EYE BLIND
# ═══════════════════════════════════════════════════════════════════════════════
write(ARTISTS / "third-eye-blind.md", artist_md(
    "third-eye-blind", "Third Eye Blind", "Group", ["Alternative Rock"],
    "San Francisco", 1993,
    [("stephan-jenkins", "Vocals"), ("kevin-cadogan", "Guitar"),
     ("arion-salazar", "Bass"), ("brad-hargreaves", "Drums")],
    ["third-eye-blind-album", "blue-teb"]
))
write(ALBUMS / "third-eye-blind-album.md", album_md(
    "third-eye-blind-album", "Third Eye Blind", "third-eye-blind", 1997,
    [("semi-charmed-life-teb", "Semi-Charmed Life"),
     ("jumper-teb", "Jumper"),
     ("how-s-it-going-to-be-teb", "How's It Going to Be")],
    producer="eric-valentine"
))
write(ALBUMS / "blue-teb.md", album_md(
    "blue-teb", "Blue", "third-eye-blind", 1999,
    [("narcolepsy-teb", "Narcolepsy"),
     ("deep-inside-of-you-teb", "Deep Inside of You")],
    producer="eric-valentine"
))
write(SONGS / "semi-charmed-life-teb.md", song_md(
    "semi-charmed-life-teb", "Semi-Charmed Life", "third-eye-blind",
    "third-eye-blind-album", 1997,
    [("stephan-jenkins", "Vocals"), ("eric-valentine", "Producer")]
))
write(SONGS / "jumper-teb.md", song_md(
    "jumper-teb", "Jumper", "third-eye-blind", "third-eye-blind-album", 1997,
    [("stephan-jenkins", "Vocals"), ("eric-valentine", "Producer")]
))
write(SONGS / "how-s-it-going-to-be-teb.md", song_md(
    "how-s-it-going-to-be-teb", "How's It Going to Be", "third-eye-blind",
    "third-eye-blind-album", 1997,
    [("stephan-jenkins", "Vocals"), ("eric-valentine", "Producer")]
))
write(SONGS / "narcolepsy-teb.md", song_md(
    "narcolepsy-teb", "Narcolepsy", "third-eye-blind", "blue-teb", 1999,
    [("stephan-jenkins", "Vocals"), ("eric-valentine", "Producer")]
))
write(SONGS / "deep-inside-of-you-teb.md", song_md(
    "deep-inside-of-you-teb", "Deep Inside of You", "third-eye-blind",
    "blue-teb", 1999,
    [("stephan-jenkins", "Vocals"), ("eric-valentine", "Producer")]
))
write(PEOPLE / "stephan-jenkins.md", person_md(
    "stephan-jenkins", "Stephan Jenkins", [("third-eye-blind", "Vocals")],
    [("semi-charmed-life-teb", "Semi-Charmed Life", "Vocals"),
     ("jumper-teb", "Jumper", "Vocals"),
     ("how-s-it-going-to-be-teb", "How's It Going to Be", "Vocals"),
     ("narcolepsy-teb", "Narcolepsy", "Vocals"),
     ("deep-inside-of-you-teb", "Deep Inside of You", "Vocals")]
))
write(PEOPLE / "kevin-cadogan.md", person_md(
    "kevin-cadogan", "Kevin Cadogan", [("third-eye-blind", "Guitar")], []
))
write(PEOPLE / "arion-salazar.md", person_md(
    "arion-salazar", "Arion Salazar", [("third-eye-blind", "Bass")], []
))
write(PEOPLE / "brad-hargreaves.md", person_md(
    "brad-hargreaves", "Brad Hargreaves", [("third-eye-blind", "Drums")], []
))
write(PEOPLE / "eric-valentine.md", person_md(
    "eric-valentine", "Eric Valentine", [],
    [("semi-charmed-life-teb", "Semi-Charmed Life", "Producer"),
     ("jumper-teb", "Jumper", "Producer"),
     ("how-s-it-going-to-be-teb", "How's It Going to Be", "Producer"),
     ("narcolepsy-teb", "Narcolepsy", "Producer"),
     ("deep-inside-of-you-teb", "Deep Inside of You", "Producer")]
))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 22 — GIN BLOSSOMS
# ═══════════════════════════════════════════════════════════════════════════════
write(ARTISTS / "gin-blossoms.md", artist_md(
    "gin-blossoms", "Gin Blossoms", "Group", ["Alternative Rock"],
    "Alternative Rock", 1987,
    [("robin-wilson-gb", "Vocals"), ("jesse-valenzuela", "Guitar"),
     ("bill-leen", "Bass"), ("phillip-rhodes", "Drums"),
     ("scott-johnson-gb", "Guitar")],
    ["new-miserable-experience-gb", "congratulations-i-m-sorry-gb"],
    disbanded=1997
))
write(ALBUMS / "new-miserable-experience-gb.md", album_md(
    "new-miserable-experience-gb", "New Miserable Experience",
    "gin-blossoms", 1992,
    [("hey-jealousy-gb", "Hey Jealousy"),
     ("found-out-about-you-gb", "Found Out About You")]
))
write(ALBUMS / "congratulations-i-m-sorry-gb.md", album_md(
    "congratulations-i-m-sorry-gb", "Congratulations I'm Sorry",
    "gin-blossoms", 1996,
    [("follow-you-down-gb", "Follow You Down"),
     ("til-i-hear-it-from-you-gb", "Til I Hear It from You"),
     ("as-long-as-it-matters-gb", "As Long as It Matters")]
))
write(SONGS / "hey-jealousy-gb.md", song_md(
    "hey-jealousy-gb", "Hey Jealousy", "gin-blossoms",
    "new-miserable-experience-gb", 1992,
    [("robin-wilson-gb", "Vocals"), ("jesse-valenzuela", "Writer")]
))
write(SONGS / "found-out-about-you-gb.md", song_md(
    "found-out-about-you-gb", "Found Out About You", "gin-blossoms",
    "new-miserable-experience-gb", 1993,
    [("robin-wilson-gb", "Vocals"), ("jesse-valenzuela", "Writer")]
))
write(SONGS / "follow-you-down-gb.md", song_md(
    "follow-you-down-gb", "Follow You Down", "gin-blossoms",
    "congratulations-i-m-sorry-gb", 1996,
    [("robin-wilson-gb", "Vocals"), ("jesse-valenzuela", "Writer")]
))
write(SONGS / "til-i-hear-it-from-you-gb.md", song_md(
    "til-i-hear-it-from-you-gb", "Til I Hear It from You", "gin-blossoms",
    "congratulations-i-m-sorry-gb", 1995,
    [("robin-wilson-gb", "Vocals"), ("jesse-valenzuela", "Writer")]
))
write(SONGS / "as-long-as-it-matters-gb.md", song_md(
    "as-long-as-it-matters-gb", "As Long as It Matters", "gin-blossoms",
    "congratulations-i-m-sorry-gb", 1996,
    [("robin-wilson-gb", "Vocals"), ("jesse-valenzuela", "Writer")]
))
write(PEOPLE / "robin-wilson-gb.md", person_md(
    "robin-wilson-gb", "Robin Wilson", [("gin-blossoms", "Vocals")],
    [("hey-jealousy-gb", "Hey Jealousy", "Vocals"),
     ("found-out-about-you-gb", "Found Out About You", "Vocals"),
     ("follow-you-down-gb", "Follow You Down", "Vocals"),
     ("til-i-hear-it-from-you-gb", "Til I Hear It from You", "Vocals"),
     ("as-long-as-it-matters-gb", "As Long as It Matters", "Vocals")]
))
write(PEOPLE / "jesse-valenzuela.md", person_md(
    "jesse-valenzuela", "Jesse Valenzuela", [("gin-blossoms", "Guitar")],
    [("hey-jealousy-gb", "Hey Jealousy", "Writer"),
     ("found-out-about-you-gb", "Found Out About You", "Writer"),
     ("follow-you-down-gb", "Follow You Down", "Writer"),
     ("til-i-hear-it-from-you-gb", "Til I Hear It from You", "Writer"),
     ("as-long-as-it-matters-gb", "As Long as It Matters", "Writer")]
))
write(PEOPLE / "bill-leen.md", person_md(
    "bill-leen", "Bill Leen", [("gin-blossoms", "Bass")], []
))
write(PEOPLE / "phillip-rhodes.md", person_md(
    "phillip-rhodes", "Phillip Rhodes", [("gin-blossoms", "Drums")], []
))
write(PEOPLE / "scott-johnson-gb.md", person_md(
    "scott-johnson-gb", "Scott Johnson", [("gin-blossoms", "Guitar")], []
))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 23 — SEMISONIC
# ═══════════════════════════════════════════════════════════════════════════════
write(ARTISTS / "semisonic.md", artist_md(
    "semisonic", "Semisonic", "Group", ["Alternative Rock"], "Alternative Rock",
    1995,
    [("dan-wilson", "Vocals"), ("john-munson", "Bass"),
     ("jacob-slichter", "Drums")],
    ["feeling-strangely-fine-semisonic", "all-about-chemistry-semisonic"]
))
write(ALBUMS / "feeling-strangely-fine-semisonic.md", album_md(
    "feeling-strangely-fine-semisonic", "Feeling Strangely Fine",
    "semisonic", 1998,
    [("closing-time-semisonic", "Closing Time"),
     ("singing-in-my-sleep-semisonic", "Singing in My Sleep"),
     ("secret-smile-semisonic", "Secret Smile")],
    producer="nick-launay"
))
write(ALBUMS / "all-about-chemistry-semisonic.md", album_md(
    "all-about-chemistry-semisonic", "All About Chemistry", "semisonic", 2001, []
))
write(SONGS / "closing-time-semisonic.md", song_md(
    "closing-time-semisonic", "Closing Time", "semisonic",
    "feeling-strangely-fine-semisonic", 1998,
    [("dan-wilson", "Vocals"), ("nick-launay", "Producer")]
))
write(SONGS / "singing-in-my-sleep-semisonic.md", song_md(
    "singing-in-my-sleep-semisonic", "Singing in My Sleep", "semisonic",
    "feeling-strangely-fine-semisonic", 1998,
    [("dan-wilson", "Vocals"), ("nick-launay", "Producer")]
))
write(SONGS / "secret-smile-semisonic.md", song_md(
    "secret-smile-semisonic", "Secret Smile", "semisonic",
    "feeling-strangely-fine-semisonic", 1998,
    [("dan-wilson", "Vocals"), ("nick-launay", "Producer")]
))
write(PEOPLE / "dan-wilson.md", person_md(
    "dan-wilson", "Dan Wilson", [("semisonic", "Vocals")],
    [("closing-time-semisonic", "Closing Time", "Vocals"),
     ("singing-in-my-sleep-semisonic", "Singing in My Sleep", "Vocals"),
     ("secret-smile-semisonic", "Secret Smile", "Vocals")]
))
write(PEOPLE / "john-munson.md", person_md(
    "john-munson", "John Munson", [("semisonic", "Bass")], []
))
write(PEOPLE / "jacob-slichter.md", person_md(
    "jacob-slichter", "Jacob Slichter", [("semisonic", "Drums")], []
))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 24 — COLLECTIVE SOUL
# ═══════════════════════════════════════════════════════════════════════════════
write(ARTISTS / "collective-soul.md", artist_md(
    "collective-soul", "Collective Soul", "Group", ["Alternative Rock"],
    "Alternative Rock", 1992,
    [("ed-roland", "Vocals"), ("ross-childress", "Guitar"),
     ("will-turpin", "Bass"), ("shane-evans", "Drums"),
     ("dean-roland", "Guitar")],
    ["hints-allegations-collective-soul", "collective-soul-album",
     "disciplined-breakdown-cs"]
))
write(ALBUMS / "hints-allegations-collective-soul.md", album_md(
    "hints-allegations-collective-soul",
    "Hints, Allegations and Things Left Unsaid",
    "collective-soul", 1994,
    [("shine-cs", "Shine")],
    producer="ed-roland"
))
write(ALBUMS / "collective-soul-album.md", album_md(
    "collective-soul-album", "Collective Soul", "collective-soul", 1995,
    [("december-cs", "December"), ("the-world-i-know-cs", "The World I Know"),
     ("gel-cs", "Gel")],
    producer="ed-roland"
))
write(ALBUMS / "disciplined-breakdown-cs.md", album_md(
    "disciplined-breakdown-cs", "Disciplined Breakdown",
    "collective-soul", 1997,
    [("heavy-cs", "Heavy")],
    producer="ed-roland"
))
write(SONGS / "shine-cs.md", song_md(
    "shine-cs", "Shine", "collective-soul",
    "hints-allegations-collective-soul", 1993,
    [("ed-roland", "Vocals")]
))
write(SONGS / "december-cs.md", song_md(
    "december-cs", "December", "collective-soul", "collective-soul-album", 1995,
    [("ed-roland", "Vocals")]
))
write(SONGS / "the-world-i-know-cs.md", song_md(
    "the-world-i-know-cs", "The World I Know", "collective-soul",
    "collective-soul-album", 1995,
    [("ed-roland", "Vocals")]
))
write(SONGS / "gel-cs.md", song_md(
    "gel-cs", "Gel", "collective-soul", "collective-soul-album", 1995,
    [("ed-roland", "Vocals")]
))
write(SONGS / "heavy-cs.md", song_md(
    "heavy-cs", "Heavy", "collective-soul", "disciplined-breakdown-cs", 1997,
    [("ed-roland", "Vocals")]
))
write(PEOPLE / "ed-roland.md", person_md(
    "ed-roland", "Ed Roland", [("collective-soul", "Vocals")],
    [("shine-cs", "Shine", "Vocals"),
     ("december-cs", "December", "Vocals"),
     ("the-world-i-know-cs", "The World I Know", "Vocals"),
     ("gel-cs", "Gel", "Vocals"),
     ("heavy-cs", "Heavy", "Vocals")]
))
write(PEOPLE / "ross-childress.md", person_md(
    "ross-childress", "Ross Childress", [("collective-soul", "Guitar")], []
))
write(PEOPLE / "will-turpin.md", person_md(
    "will-turpin", "Will Turpin", [("collective-soul", "Bass")], []
))
write(PEOPLE / "shane-evans.md", person_md(
    "shane-evans", "Shane Evans", [("collective-soul", "Drums")], []
))
write(PEOPLE / "dean-roland.md", person_md(
    "dean-roland", "Dean Roland", [("collective-soul", "Guitar")], []
))

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 25 — MASSIVE ATTACK
# ═══════════════════════════════════════════════════════════════════════════════
write(ARTISTS / "massive-attack.md", artist_md(
    "massive-attack", "Massive Attack", "Group", ["Alternative Rock"],
    "Alternative Rock", 1988,
    [("robert-del-naja", "Vocals"), ("grant-marshall", "Vocals"),
     ("andrew-vowles", "Vocals")],
    ["blue-lines-ma", "protection-ma", "mezzanine-ma"]
))
write(ALBUMS / "blue-lines-ma.md", album_md(
    "blue-lines-ma", "Blue Lines", "massive-attack", 1991,
    [("unfinished-sympathy-ma", "Unfinished Sympathy"),
     ("safe-from-harm-ma", "Safe from Harm")]
))
write(ALBUMS / "protection-ma.md", album_md(
    "protection-ma", "Protection", "massive-attack", 1994,
    [("protection-song-ma", "Protection")]
))
write(ALBUMS / "mezzanine-ma.md", album_md(
    "mezzanine-ma", "Mezzanine", "massive-attack", 1998,
    [("teardrop-ma", "Teardrop"), ("angel-ma", "Angel")]
))
write(SONGS / "unfinished-sympathy-ma.md", song_md(
    "unfinished-sympathy-ma", "Unfinished Sympathy", "massive-attack",
    "blue-lines-ma", 1991,
    [("robert-del-naja", "Writer"), ("shara-nelson", "Vocals")]
))
write(SONGS / "safe-from-harm-ma.md", song_md(
    "safe-from-harm-ma", "Safe from Harm", "massive-attack",
    "blue-lines-ma", 1991,
    [("robert-del-naja", "Writer"), ("shara-nelson", "Vocals")]
))
write(SONGS / "protection-song-ma.md", song_md(
    "protection-song-ma", "Protection", "massive-attack", "protection-ma", 1994,
    [("robert-del-naja", "Writer"), ("tracey-thorn", "Vocals")]
))
write(SONGS / "teardrop-ma.md", song_md(
    "teardrop-ma", "Teardrop", "massive-attack", "mezzanine-ma", 1998,
    [("robert-del-naja", "Writer"), ("elizabeth-fraser", "Vocals")]
))
write(SONGS / "angel-ma.md", song_md(
    "angel-ma", "Angel", "massive-attack", "mezzanine-ma", 1998,
    [("robert-del-naja", "Writer"), ("grant-marshall", "Vocals")]
))
write(PEOPLE / "robert-del-naja.md", person_md(
    "robert-del-naja", "Robert Del Naja", [("massive-attack", "Vocals")],
    [("unfinished-sympathy-ma", "Unfinished Sympathy", "Writer"),
     ("safe-from-harm-ma", "Safe from Harm", "Writer"),
     ("protection-song-ma", "Protection", "Writer"),
     ("teardrop-ma", "Teardrop", "Writer"),
     ("angel-ma", "Angel", "Writer")]
))
write(PEOPLE / "grant-marshall.md", person_md(
    "grant-marshall", "Grant Marshall", [("massive-attack", "Vocals")],
    [("angel-ma", "Angel", "Vocals")]
))
write(PEOPLE / "andrew-vowles.md", person_md(
    "andrew-vowles", "Andrew Vowles", [("massive-attack", "Vocals")], []
))
write(PEOPLE / "shara-nelson.md", person_md(
    "shara-nelson", "Shara Nelson", [],
    [("unfinished-sympathy-ma", "Unfinished Sympathy", "Vocals"),
     ("safe-from-harm-ma", "Safe from Harm", "Vocals")]
))
write(PEOPLE / "elizabeth-fraser.md", person_md(
    "elizabeth-fraser", "Elizabeth Fraser", [],
    [("teardrop-ma", "Teardrop", "Vocals")]
))
write(PEOPLE / "tracey-thorn.md", person_md(
    "tracey-thorn", "Tracey Thorn", [],
    [("protection-song-ma", "Protection", "Vocals")]
))

print("\nDone.")
