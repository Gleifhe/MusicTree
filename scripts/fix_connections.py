from pathlib import Path
import re

BASE = Path("c:/repo/MusicTree")

# 1. Create The National artist
national = """---
scene: "Indie Rock"
title: "The National"
country: "US"
formed: 1999
band_type: "Group"
genres: ["indie rock", "art rock", "chamber pop"]
members:
  - slug: "aaron-dessner"
    name: "Aaron Dessner"
    role: "Guitar"
  - slug: "bryce-dessner"
    name: "Bryce Dessner"
    role: "Guitar"
  - slug: "matt-berninger"
    name: "Matt Berninger"
    role: "Vocals"
  - slug: "scott-devendorf"
    name: "Scott Devendorf"
    role: "Bass"
  - slug: "bryan-devendorf"
    name: "Bryan Devendorf"
    role: "Drums"
albums:
  - slug: "alligator-national"
    title: "Alligator"
    year: 2005
  - slug: "boxer"
    title: "Boxer"
    year: 2007
  - slug: "high-violet"
    title: "High Violet"
    year: 2010
  - slug: "trouble-will-find-me"
    title: "Trouble Will Find Me"
    year: 2013
draft: false
---
The National are an American indie rock band formed in Brooklyn, New York in 1999.
Guitarist Aaron Dessner became one of the most sought-after producers in modern music,
collaborating with Taylor Swift, Gracie Abrams, and many others, creating a key
bridge between indie rock and contemporary pop.
"""
(BASE / "content/artists/the-national.md").write_text(national, encoding="utf-8")
print("Created the-national")

# 2. Create Bleachers artist (Jack Antonoff's band)
bleachers = """---
scene: "Indie Pop"
title: "Bleachers"
country: "US"
formed: 2013
band_type: "Group"
genres: ["indie pop", "synth-pop", "new wave"]
members:
  - slug: "jack-antonoff"
    name: "Jack Antonoff"
    role: "Vocals, Guitar (2013-present)"
albums:
  - slug: "strange-desire"
    title: "Strange Desire"
    year: 2014
  - slug: "gone-now"
    title: "Gone Now"
    year: 2017
  - slug: "bleachers-self-titled"
    title: "Bleachers"
    year: 2021
draft: false
---
Bleachers is an indie pop project led by Jack Antonoff, one of the most prolific
producers and songwriters of his generation. Antonoff produced albums for Taylor Swift,
Lana Del Rey, Sabrina Carpenter, Lorde, and many others, making Bleachers a central
node connecting indie rock and mainstream pop.
"""
(BASE / "content/artists/bleachers.md").write_text(bleachers, encoding="utf-8")
print("Created bleachers")

# 3. Update aaron-dessner to include The National band
aaron_path = BASE / "content/people/aaron-dessner.md"
if aaron_path.exists():
    text = aaron_path.read_text(encoding="utf-8-sig")
    if "the-national" not in text:
        if "bands:" in text:
            text = text.replace("bands:", """bands:
  - slug: "the-national"
    name: "The National"
    years: "1999-present"
  - slug: "bleachers"
    name: "Bleachers"
    years: "collaboration" """, 1)
        else:
            text = text.replace("roles:", """bands:
  - slug: "the-national"
    name: "The National"
    years: "1999-present"
roles:""", 1)
        aaron_path.write_text(text, encoding="utf-8")
        print("Updated aaron-dessner")
else:
    # Create it
    aaron = """---
title: "Aaron Dessner"
born: 1976
nationality: "American"
roles: ["Guitar", "Producer", "Songwriter"]
bands:
  - slug: "the-national"
    name: "The National"
    years: "1999-present"
song_credits:
  - slug: "cardigan"
    title: "cardigan"
    credit: "Producer"
  - slug: "august"
    title: "august"
    credit: "Producer"
  - slug: "seven"
    title: "seven"
    credit: "Producer"
draft: false
---
Aaron Dessner is a guitarist, producer, and songwriter best known as a member of
The National and as a producer for Taylor Swift's folklore and evermore albums.
"""
    aaron_path.write_text(aaron, encoding="utf-8")
    print("Created aaron-dessner")

# 4. Update jack-antonoff to include Bleachers
jack_path = BASE / "content/people/jack-antonoff.md"
if jack_path.exists():
    text = jack_path.read_text(encoding="utf-8-sig")
    if "bleachers" not in text:
        if "bands:" in text:
            text = text.replace("bands:", """bands:
  - slug: "bleachers"
    name: "Bleachers"
    years: "2013-present"
  - slug: "fun-band"
    name: "fun."
    years: "2008-2015" """, 1)
        else:
            text = text.replace("roles:", """bands:
  - slug: "bleachers"
    name: "Bleachers"
    years: "2013-present"
roles:""", 1)
        jack_path.write_text(text, encoding="utf-8")
        print("Updated jack-antonoff")

# 5. Create Rick Rubin with real production credits connecting rock + hip-hop
rick_path = BASE / "content/people/rick-rubin.md"
rick = """---
title: "Rick Rubin"
born: 1963
nationality: "American"
roles: ["Producer"]
bands: []
song_credits:
  - slug: "sabotage"
    title: "Sabotage"
    credit: "Producer"
  - slug: "under-the-bridge"
    title: "Under the Bridge"
    credit: "Producer"
  - slug: "californication"
    title: "Californication"
    credit: "Producer"
draft: false
---
Rick Rubin is one of the most influential record producers in history.
Co-founder of Def Jam Recordings, his production credits span hip-hop (Beastie Boys,
LL Cool J, Jay-Z), metal (Metallica, Slayer), rock (Red Hot Chili Peppers, Tom Petty,
The Strokes), country (Johnny Cash), and pop (Adele, Lady Gaga).
"""
rick_path.write_text(rick, encoding="utf-8")
print("Updated rick-rubin")

# 6. Create some missing National albums so it has content in the graph
boxer_songs = ["apartment-story", "squalor-victoria", "brainy", "gospel", "slow-show", "karen", "racing-like-a-pro", "start-a-war", "guest-room", "ada", "standing-o"]
boxer_album = """---
title: "Boxer"
artist: "The National"
artist_slug: "the-national"
year: 2007
genres: ["indie rock", "art rock"]
songs:
  - slug: "brainy"
    title: "Brainy"
  - slug: "slow-show"
    title: "Slow Show"
  - slug: "apartment-story"
    title: "Apartment Story"
  - slug: "gospel"
    title: "Gospel"
  - slug: "start-a-war"
    title: "Start a War"
  - slug: "ada"
    title: "Ada"
draft: false
---
The National's breakthrough album, Boxer (2007) established them as indie rock's most
literary and emotionally resonant band.
"""
(BASE / "content/albums/boxer.md").write_text(boxer_album, encoding="utf-8")
print("Created boxer album")

# Create a few Boxer songs
boxer_tracks = [
    ("brainy", "Brainy", "Aaron Dessner wrote this introspective opener."),
    ("slow-show", "Slow Show", "One of The National's most beloved songs."),
    ("apartment-story", "Apartment Story", "A wistful indie rock track."),
]
for slug, title, desc in boxer_tracks:
    song = f"""---
title: "{title}"
artist: "The National"
artist_slug: "the-national"
album: "Boxer"
album_slug: "boxer"
year: 2007
credits:
  - person_slug: "matt-berninger"
    person: "Matt Berninger"
    role: "vocalist"
  - person_slug: "aaron-dessner"
    person: "Aaron Dessner"
    role: "guitar, producer"
  - person_slug: "bryce-dessner"
    person: "Bryce Dessner"
    role: "guitar"
draft: false
---
{desc}
"""
    (BASE / f"content/songs/{slug}.md").write_text(song, encoding="utf-8")

# Also create some people for The National
people_data = [
    ("matt-berninger", "Matt Berninger", 1971, ["Vocals", "Songwriter"], "the-national", "The National"),
    ("bryce-dessner", "Bryce Dessner", 1976, ["Guitar", "Composer"], "the-national", "The National"),
    ("scott-devendorf", "Scott Devendorf", 1976, ["Bass"], "the-national", "The National"),
    ("bryan-devendorf", "Bryan Devendorf", 1976, ["Drums"], "the-national", "The National"),
]
for slug, name, born, roles, band_slug, band_name in people_data:
    p = BASE / f"content/people/{slug}.md"
    if not p.exists():
        content = f"""---
title: "{name}"
born: {born}
nationality: "American"
roles: {roles}
bands:
  - slug: "{band_slug}"
    name: "{band_name}"
    years: "1999-present"
song_credits:
  - slug: "brainy"
    title: "Brainy"
    credit: "Performer"
draft: false
---
{name} is a member of The National.
"""
        p.write_text(content, encoding="utf-8")
        print(f"Created {slug}")

print("\nAll done!")
