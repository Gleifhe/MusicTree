#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

BASE = Path("c:/repo/MusicTree")
ARTISTS = BASE / "content/artists"
ALBUMS  = BASE / "content/albums"
SONGS   = BASE / "content/songs"
PEOPLE  = BASE / "content/people"

_c = 0; _s = 0

def w(path, content):
    global _c, _s
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists():
        _s += 1; return
    p.write_text(content, encoding="utf-8")
    _c += 1

def g(genres):
    return ", ".join(f'"{x}"' for x in genres)

def artist_md(slug, scene, title, formed, btype, genres, members, albums, bio):
    L = ["---", f'scene: "{scene}"', f'title: "{title}"', 'country: "US"',
         f'formed: {formed}', f'band_type: "{btype}"', f'genres: [{g(genres)}]', 'members:']
    for ms,mn,mr in members:
        L += [f'  - slug: "{ms}"', f'    name: "{mn}"', f'    role: "{mr}"']
    L.append('albums:')
    for asl,atn,ayr in albums:
        L += [f'  - slug: "{asl}"', f'    title: "{atn}"', f'    year: {ayr}']
    L += ['draft: false', '---', bio]
    return "\n".join(L)

def album_md(title, aname, aslug, year, genres, songs, desc):
    L = ["---", f'title: "{title}"', f'artist: "{aname}"',
         f'artist_slug: "{aslug}"', f'year: {year}', f'genres: [{g(genres)}]', 'songs:']
    for ss,st in songs:
        L += [f'  - slug: "{ss}"', f'    title: "{st}"']
    L += ['draft: false', '---', desc]
    return "\n".join(L)

def song_md(title, aname, aslug, alslug, credits, year=0, desc=""):
    L = ["---", f'title: "{title}"', f'artist: "{aname}"',
         f'artist_slug: "{aslug}"',
         f'album_slug: "{alslug}"']
    if year: L.append(f'year: {year}')
    L.append('credits:')
    for ps,pn,role in credits:
        L += [f'  - person_slug: "{ps}"', f'    person: "{pn}"', f'    role: "{role}"']
    L += ['draft: false', '---', desc]
    return "\n".join(L)

def person_md(slug, title, born, nat, roles, bands, credits, bio, died=None):
    r = ", ".join(f'"{x}"' for x in roles)
    L = ["---", f'title: "{title}"', f'born: {born}']
    if died is not None: L.append(f'died: {died}')
    L += [f'nationality: "{nat}"', f'roles: [{r}]']
    if bands:
        L.append('bands:')
        for bs,bn,br in bands:
            L += [f'  - slug: "{bs}"', f'    name: "{bn}"', f'    role: "{br}"']
    if credits:
        L.append('credits:')
        for c in credits:
            k = "song_slug" if c[0]=="song" else "album_slug"
            L += [f'  - {k}: "{c[1]}"', f'    title: "{c[2]}"',
                  f'    role: "{c[3]}"', f'    artist: "{c[4]}"']
    L += ['draft: false', '---', bio]
    return "\n".join(L)

print("Helpers loaded OK")

# ═══════════════════════════════════════════════════════════════ ARTISTS ═══

# SOUNDGARDEN
w(ARTISTS/"soundgarden.md", artist_md("soundgarden","Seattle","Soundgarden",1984,"Group",
  ["grunge","alternative rock","hard rock"],
  [("chris-cornell","Chris Cornell","Vocals, Guitar (1984-2017)"),
   ("kim-thayil","Kim Thayil","Lead Guitar"),
   ("ben-shepherd","Ben Shepherd","Bass (1990-2017)"),
   ("matt-cameron","Matt Cameron","Drums (1986-2017)")],
  [("ultramega-ok","Ultramega OK",1988),("louder-than-love","Louder Than Love",1989),
   ("badmotorfinger","Badmotorfinger",1991),("superunknown","Superunknown",1994),
   ("down-on-the-upside","Down on the Upside",1996)],
  "Soundgarden was an American rock band from Seattle, Washington, formed in 1984. Featuring the powerful vocals of Chris Cornell and Kim Thayil's innovative guitar, they were pioneers of grunge. Their 1994 album Superunknown is one of the greatest rock albums of the decade."))

# ALICE IN CHAINS
w(ARTISTS/"alice-in-chains.md", artist_md("alice-in-chains","Seattle","Alice in Chains",1987,"Group",
  ["grunge","heavy metal","alternative metal"],
  [("layne-staley","Layne Staley","Vocals (1987-2002)"),
   ("jerry-cantrell","Jerry Cantrell","Guitar, Vocals"),
   ("mike-inez","Mike Inez","Bass (1993-present)"),
   ("sean-kinney","Sean Kinney","Drums"),
   ("mike-starr","Mike Starr","Bass (1987-1993)")],
  [("facelift","Facelift",1990),("dirt","Dirt",1992),
   ("alice-in-chains-1995","Alice in Chains",1995),
   ("black-gives-way-to-blue","Black Gives Way to Blue",2009)],
  "Alice in Chains formed in Seattle in 1987. Their dark, heavy grunge blended metal with haunting vocal harmonies between Layne Staley and Jerry Cantrell. Albums like Dirt explored addiction with unflinching honesty."))

# MUDHONEY
w(ARTISTS/"mudhoney.md", artist_md("mudhoney","Seattle","Mudhoney",1988,"Group",
  ["grunge","garage rock","alternative rock"],
  [("mark-arm","Mark Arm","Vocals, Guitar"),
   ("steve-turner","Steve Turner","Guitar"),
   ("matt-lukin","Matt Lukin","Bass"),
   ("dan-peters","Dan Peters","Drums")],
  [("mudhoney-debut","Mudhoney",1989),
   ("every-good-boy-deserves-fudge","Every Good Boy Deserves Fudge",1991)],
  "Mudhoney formed in Seattle in 1988 and were central to the early grunge movement. Their fuzz-drenched debut single Touch Me I'm Sick became an anthem of the Sub Pop era."))

# MOTHER LOVE BONE
w(ARTISTS/"mother-love-bone.md", artist_md("mother-love-bone","Seattle","Mother Love Bone",1987,"Group",
  ["glam metal","grunge","alternative rock"],
  [("andrew-wood","Andrew Wood","Vocals (1987-1990)"),
   ("stone-gossard","Stone Gossard","Guitar"),
   ("jeff-ament","Jeff Ament","Bass"),
   ("greg-gilmore","Greg Gilmore","Drums"),
   ("bruce-fairweather","Bruce Fairweather","Guitar")],
  [("apple","Apple",1990)],
  "Mother Love Bone bridged glam rock and grunge in Seattle. Vocalist Andrew Wood died days before their debut album Apple was released. Stone Gossard and Jeff Ament went on to form Pearl Jam."))

# TEMPLE OF THE DOG
w(ARTISTS/"temple-of-the-dog.md", artist_md("temple-of-the-dog","Seattle","Temple of the Dog",1990,"Group",
  ["grunge","alternative rock","hard rock"],
  [("chris-cornell","Chris Cornell","Vocals"),
   ("eddie-vedder","Eddie Vedder","Vocals"),
   ("stone-gossard","Stone Gossard","Guitar"),
   ("jeff-ament","Jeff Ament","Bass"),
   ("mike-mccready","Mike McCready","Guitar"),
   ("matt-cameron","Matt Cameron","Drums")],
  [("temple-of-the-dog","Temple of the Dog",1991)],
  "Temple of the Dog was a Seattle supergroup formed as a tribute to Andrew Wood of Mother Love Bone. Chris Cornell wrote the album with future Pearl Jam members. The classic Hunger Strike remains one of grunge's defining songs."))

# SCREAMING TREES
w(ARTISTS/"screaming-trees.md", artist_md("screaming-trees","Seattle","Screaming Trees",1985,"Group",
  ["grunge","alternative rock","psychedelic rock"],
  [("mark-lanegan","Mark Lanegan","Vocals"),
   ("gary-lee-conner","Gary Lee Conner","Guitar"),
   ("van-conner","Van Conner","Bass"),
   ("barrett-martin","Barrett Martin","Drums (1991-1996)")],
  [("buzz-factory","Buzz Factory",1989),
   ("sweet-oblivion","Sweet Oblivion",1992),
   ("dust-st","Dust",1996)],
  "Screaming Trees from Ellensburg, Washington were early grunge pioneers fronted by Mark Lanegan's deep, gravelly voice. Their 1992 album Sweet Oblivion remains their most celebrated work."))

# MELVINS
w(ARTISTS/"melvins.md", artist_md("melvins","Seattle","Melvins",1983,"Group",
  ["sludge metal","noise rock","grunge"],
  [("buzz-osborne","Buzz Osborne","Vocals, Guitar"),
   ("dale-crover","Dale Crover","Drums"),
   ("matt-lukin","Matt Lukin","Bass (early)"),
   ("lori-black","Lori Black","Bass (early)")],
  [("gluey-porch-treatments","Gluey Porch Treatments",1987),
   ("houdini","Houdini",1993)],
  "Melvins from Aberdeen, Washington pioneered sludge metal and were a foundational influence on grunge. Their 1993 album Houdini was co-produced by Kurt Cobain."))

# MODEST MOUSE
w(ARTISTS/"modest-mouse.md", artist_md("modest-mouse","Seattle","Modest Mouse",1992,"Group",
  ["indie rock","alternative rock","post-punk"],
  [("isaac-brock","Isaac Brock","Vocals, Guitar"),
   ("jeremiah-green","Jeremiah Green","Drums"),
   ("eric-judy","Eric Judy","Bass")],
  [("this-is-a-long-drive","This Is a Long Drive for Someone with Nothing to Think About",1996),
   ("lonesome-crowded-west","The Lonesome Crowded West",1997),
   ("moon-and-antarctica","The Moon and Antarctica",2000),
   ("good-news-for-people-who-love-bad-news","Good News for People Who Love Bad News",2004)],
  "Modest Mouse from Issaquah, Washington blend indie rock, country, and post-punk with Isaac Brock's philosophical lyrics. Float On (2004) brought them mainstream success."))

# DEATH CAB FOR CUTIE
w(ARTISTS/"death-cab-for-cutie.md", artist_md("death-cab-for-cutie","Seattle","Death Cab for Cutie",1997,"Group",
  ["indie rock","indie pop","alternative rock"],
  [("ben-gibbard","Ben Gibbard","Vocals, Guitar"),
   ("chris-walla","Chris Walla","Guitar, Producer"),
   ("nick-harmer","Nick Harmer","Bass"),
   ("jason-mcgerr","Jason McGerr","Drums (2003-present)")],
  [("something-about-airplanes","Something About Airplanes",1998),
   ("we-have-the-facts","We Have the Facts and We're Voting Yes",2000),
   ("transatlanticism","Transatlanticism",2003),
   ("plans","Plans",2005)],
  "Death Cab for Cutie from Bellingham, Washington became a defining indie rock band of the 2000s. Ben Gibbard's emotionally resonant songwriting and melodic approach made Transatlanticism a touchstone for a generation."))

# FLEET FOXES
w(ARTISTS/"fleet-foxes.md", artist_md("fleet-foxes","Seattle","Fleet Foxes",2006,"Group",
  ["indie folk","baroque pop","folk rock"],
  [("robin-pecknold","Robin Pecknold","Vocals, Guitar"),
   ("skyler-skjelset","Skyler Skjelset","Guitar"),
   ("casey-musgraves-ff","Casey Musgraves","Guitar"),
   ("morgan-henderson","Morgan Henderson","Bass, Multi-instrumentalist"),
   ("christian-wargo","Christian Wargo","Bass, Vocals")],
  [("fleet-foxes-debut","Fleet Foxes",2008),
   ("helplessness-blues","Helplessness Blues",2011)],
  "Fleet Foxes from Seattle blend lush harmonies, baroque arrangements, and nature-inspired lyrics. Their self-titled 2008 debut was widely acclaimed as one of the best albums of the decade."))

# SLEATER-KINNEY
w(ARTISTS/"sleater-kinney.md", artist_md("sleater-kinney","Seattle","Sleater-Kinney",1994,"Group",
  ["riot grrrl","indie rock","punk rock"],
  [("corin-tucker","Corin Tucker","Vocals, Guitar"),
   ("carrie-brownstein","Carrie Brownstein","Guitar, Vocals"),
   ("janet-weiss","Janet Weiss","Drums (1996-2019)")],
  [("call-the-doctor","Call the Doctor",1996),
   ("dig-me-out","Dig Me Out",1997),
   ("all-hands-on-the-bad-one","All Hands on the Bad One",2000)],
  "Sleater-Kinney from Olympia, Washington are icons of riot grrrl and indie rock. Their powerful guitar interplay and politically charged lyrics made them one of the most celebrated feminist punk bands in history."))

# BIKINI KILL
w(ARTISTS/"bikini-kill.md", artist_md("bikini-kill","Seattle","Bikini Kill",1990,"Group",
  ["riot grrrl","punk rock","feminist punk"],
  [("kathleen-hanna","Kathleen Hanna","Vocals"),
   ("tobi-vail","Tobi Vail","Drums"),
   ("kathi-wilcox","Kathi Wilcox","Bass"),
   ("billy-karren","Billy Karren","Guitar")],
  [("pussy-whipped","Pussy Whipped",1993),
   ("reject-all-american","Reject All American",1996)],
  "Bikini Kill from Olympia, Washington founded the riot grrrl movement. Led by Kathleen Hanna, their anthem Rebel Girl became a defining song of 1990s feminist punk."))

# HEART
w(ARTISTS/"heart.md", artist_md("heart","Seattle","Heart",1973,"Group",
  ["hard rock","classic rock","arena rock"],
  [("ann-wilson","Ann Wilson","Vocals"),
   ("nancy-wilson","Nancy Wilson","Guitar, Vocals"),
   ("roger-fisher","Roger Fisher","Guitar (1973-1980)"),
   ("steve-fossen","Steve Fossen","Bass (1972-1982)"),
   ("howard-leese","Howard Leese","Guitar, Keys (1975-1998)"),
   ("mike-derosier","Mike Derosier","Drums (1975-1982)")],
  [("dreamboat-annie","Dreamboat Annie",1975),
   ("little-queen","Little Queen",1977),
   ("bad-animals","Bad Animals",1987)],
  "Heart from Seattle were one of the first successful rock bands led by women. Sisters Ann and Nancy Wilson fronted a group that produced classic rock staples Magic Man, Crazy on You, and Barracuda."))

# JIMI HENDRIX
w(ARTISTS/"jimi-hendrix.md", artist_md("jimi-hendrix","Seattle","Jimi Hendrix",1966,"Solo",
  ["psychedelic rock","blues rock","hard rock"],
  [("jimi-hendrix-person","Jimi Hendrix","Vocals, Guitar")],
  [("are-you-experienced","Are You Experienced",1967),
   ("axis-bold-as-love","Axis: Bold as Love",1967),
   ("electric-ladyland","Electric Ladyland",1968)],
  "Jimi Hendrix (1942-1970) was born in Seattle and became the most celebrated electric guitarist in history. His innovative use of feedback and distortion redefined rock guitar. He released three landmark albums before his death at age 27."))

# SMASHING PUMPKINS
w(ARTISTS/"smashing-pumpkins.md", artist_md("smashing-pumpkins","Chicago","Smashing Pumpkins",1988,"Group",
  ["alternative rock","grunge","shoegaze"],
  [("billy-corgan","Billy Corgan","Vocals, Guitar"),
   ("james-iha","James Iha","Guitar"),
   ("darcy-wretzky","D'arcy Wretzky","Bass (1988-1999)"),
   ("jimmy-chamberlin","Jimmy Chamberlin","Drums (1988-1996, 1999-2009)")],
  [("gish","Gish",1991),("siamese-dream","Siamese Dream",1993),
   ("mellon-collie","Mellon Collie and the Infinite Sadness",1995),
   ("adore","Adore",1998)],
  "Smashing Pumpkins from Chicago became one of the most successful bands of the 1990s. Siamese Dream (1993) produced by Butch Vig and the double album Mellon Collie and the Infinite Sadness (1995) defined alternative rock."))

# LIZ PHAIR
w(ARTISTS/"liz-phair.md", artist_md("liz-phair","Chicago","Liz Phair",1991,"Solo",
  ["indie rock","lo-fi","alternative rock"],
  [("liz-phair-person","Liz Phair","Vocals, Guitar")],
  [("exile-in-guyville","Exile in Guyville",1993),
   ("whip-smart","Whip-Smart",1994)],
  "Liz Phair from Chicago released Exile in Guyville (1993), a track-by-track response to the Rolling Stones' Exile on Main St. One of the most important indie rock albums of the decade."))

# WILCO
w(ARTISTS/"wilco.md", artist_md("wilco","Chicago","Wilco",1994,"Group",
  ["alternative country","indie rock","art rock"],
  [("jeff-tweedy","Jeff Tweedy","Vocals, Guitar"),
   ("john-stirratt","John Stirratt","Bass"),
   ("glenn-kotche","Glenn Kotche","Drums (2001-present)"),
   ("nels-cline","Nels Cline","Guitar (2004-present)"),
   ("jay-bennett","Jay Bennett","Guitar, Keys (1994-2001)")],
  [("am-wilco","AM",1995),("being-there","Being There",1996),
   ("yankee-hotel-foxtrot","Yankee Hotel Foxtrot",2002),
   ("a-ghost-is-born","A Ghost Is Born",2004)],
  "Wilco from Chicago evolved from alt-country to experimental indie rock. Yankee Hotel Foxtrot (2002), initially rejected by their label, became one of the most acclaimed American albums of the decade."))

# CHEAP TRICK
w(ARTISTS/"cheap-trick.md", artist_md("cheap-trick","Chicago","Cheap Trick",1973,"Group",
  ["hard rock","power pop","arena rock"],
  [("robin-zander","Robin Zander","Vocals"),
   ("rick-nielsen","Rick Nielsen","Guitar"),
   ("tom-petersson","Tom Petersson","Bass"),
   ("bun-e-carlos","Bun E. Carlos","Drums")],
  [("cheap-trick-debut","Cheap Trick",1977),
   ("in-color","In Color",1977),
   ("at-budokan","At Budokan",1978)],
  "Cheap Trick from Rockford, Illinois pioneered power pop and hard rock. Their 1978 live album At Budokan captured the hysteria of their Japanese fanbase and became one of the best-selling live albums of all time."))

# THE JESUS LIZARD
w(ARTISTS/"the-jesus-lizard.md", artist_md("the-jesus-lizard","Chicago","The Jesus Lizard",1988,"Group",
  ["noise rock","post-hardcore","alternative rock"],
  [("david-yow","David Yow","Vocals"),
   ("duane-denison","Duane Denison","Guitar"),
   ("david-sims","David Wm. Sims","Bass"),
   ("mac-mcneilly","Mac McNeilly","Drums")],
  [("goat","Goat",1991),("liar","Liar",1992)],
  "The Jesus Lizard from Chicago were one of the most visceral live acts of the 1990s underground. Produced by Steve Albini, their noise rock albums Goat and Liar are landmarks of the genre."))

# URGE OVERKILL
w(ARTISTS/"urge-overkill.md", artist_md("urge-overkill","Chicago","Urge Overkill",1986,"Group",
  ["alternative rock","indie rock","hard rock"],
  [("nash-kato","Nash Kato","Vocals, Guitar"),
   ("eddie-roeser","Eddie Roeser","Guitar, Vocals"),
   ("blackie-onassis","Blackie Onassis","Drums")],
  [("saturation","Saturation",1993)],
  "Urge Overkill from Chicago were known for their debonair image and big-riff sound. Their Butch Vig-produced album Saturation (1993) was their commercial peak."))

# TORTOISE
w(ARTISTS/"tortoise.md", artist_md("tortoise","Chicago","Tortoise",1990,"Group",
  ["post-rock","experimental","krautrock"],
  [("john-mcentire","John McEntire","Drums, Producer"),
   ("bundy-k-brown","Bundy K. Brown","Bass, Guitar"),
   ("doug-mccombs","Doug McCombs","Bass"),
   ("dan-bitney","Dan Bitney","Percussion"),
   ("john-herndon","John Herndon","Drums")],
  [("millions-now-living-will-never-die","Millions Now Living Will Never Die",1996),
   ("tnt-tortoise","TNT",1998)],
  "Tortoise from Chicago are central figures in post-rock, blending jazz, krautrock, and minimalism. Their 1996 album Millions Now Living Will Never Die is anchored by the epic 20-minute track Djed."))

# MUDDY WATERS
w(ARTISTS/"muddy-waters.md", artist_md("muddy-waters","Chicago","Muddy Waters",1943,"Solo",
  ["Chicago blues","electric blues","delta blues"],
  [("muddy-waters-person","Muddy Waters","Vocals, Guitar")],
  [("folk-singer","Folk Singer",1964),
   ("electric-mud","Electric Mud",1968)],
  "Muddy Waters (1913-1983) was the most important figure in Chicago blues. Moving from the Mississippi Delta, he electrified the blues and influenced virtually every rock musician who followed, including the Rolling Stones and Led Zeppelin."))

# BUDDY GUY
w(ARTISTS/"buddy-guy.md", artist_md("buddy-guy","Chicago","Buddy Guy",1957,"Solo",
  ["Chicago blues","electric blues","blues rock"],
  [("buddy-guy-person","Buddy Guy","Vocals, Guitar")],
  [("damn-right-ive-got-the-blues","Damn Right, I've Got the Blues",1991)],
  "Buddy Guy (born 1936) is a central figure in Chicago blues. His aggressive guitar style influenced Jimi Hendrix, Eric Clapton, and Stevie Ray Vaughan."))

# HOWLIN WOLF
w(ARTISTS/"howlin-wolf.md", artist_md("howlin-wolf","Chicago","Howlin' Wolf",1948,"Solo",
  ["Chicago blues","electric blues","delta blues"],
  [("howlin-wolf-person","Howlin' Wolf","Vocals, Guitar")],
  [("moanin-in-the-moonshine","Moanin' in the Moonshine",1959),
   ("the-real-folk-blues","The Real Folk Blues",1966)],
  "Howlin' Wolf (1910-1976) was one of the most powerful figures in Chicago blues. Songs like Smokestack Lightning, Back Door Man, and Killing Floor have been covered by countless rock artists."))

# BIG BLACK
w(ARTISTS/"big-black.md", artist_md("big-black","Chicago","Big Black",1982,"Group",
  ["noise rock","post-punk","hardcore punk"],
  [("steve-albini","Steve Albini","Vocals, Guitar"),
   ("santiago-durango","Santiago Durango","Guitar"),
   ("dave-riley","Dave Riley","Bass")],
  [("atomizer","Atomizer",1986),
   ("songs-about-fucking","Songs About Fucking",1987)],
  "Big Black formed by Steve Albini in Chicago in 1982. Using drum machines alongside guitars and bass, they created an abrasive sound that influenced countless underground bands."))

# SHELLAC
w(ARTISTS/"shellac.md", artist_md("shellac","Chicago","Shellac",1992,"Group",
  ["noise rock","post-hardcore","math rock"],
  [("steve-albini","Steve Albini","Guitar, Vocals"),
   ("bob-weston","Bob Weston","Bass"),
   ("todd-trainer","Todd Trainer","Drums")],
  [("at-action-park","At Action Park",1994),
   ("terraform","Terraform",1998)],
  "Shellac formed by Steve Albini in Chicago in 1992. Known for their sparse, precise noise rock, they are one of the most consistent and respected acts in underground rock."))

print(f"After artists: {_c} created, {_s} skipped")

# ══════════════════════════════════════════════════════════════ ALBUMS ═══

# SOUNDGARDEN albums
w(ALBUMS/"ultramega-ok.md", album_md("Ultramega OK","Soundgarden","soundgarden",1988,
  ["grunge","alternative rock"],
  [("flower-sg","Flower"),("all-your-lies","All Your Lies"),("six-six-seven","667"),
   ("beyond-the-wheel","Beyond the Wheel"),("fourth-of-july-1988","4th of July"),
   ("mood-for-trouble","Mood for Trouble"),("circle-of-power","Circle of Power"),
   ("he-didnt","He Didn't")],
  "Soundgarden's debut album, produced by Jack Endino and released on SST Records in 1988. Raw and experimental, it introduced their heavy psychedelic sound."))

w(ALBUMS/"louder-than-love.md", album_md("Louder Than Love","Soundgarden","soundgarden",1989,
  ["grunge","hard rock","alternative rock"],
  [("ugly-truth","Ugly Truth"),("hands-all-over","Hands All Over"),
   ("get-on-the-snake","Get on the Snake"),("big-dumb-sex","Big Dumb Sex"),
   ("full-on-kevins-mom","Full on Kevin's Mom"),("no-wrong-no-right","No Wrong No Right"),
   ("loud-love","Loud Love")],
  "Soundgarden's second album, their first on a major label (A&M Records). Produced by Terry Date and Jack Endino, it expanded their heavy sound."))

w(ALBUMS/"badmotorfinger.md", album_md("Badmotorfinger","Soundgarden","soundgarden",1991,
  ["grunge","alternative metal","hard rock"],
  [("rusty-cage","Rusty Cage"),("outshined","Outshined"),
   ("slaves-and-bulldozers","Slaves and Bulldozers"),("jesus-christ-pose","Jesus Christ Pose"),
   ("face-pollution","Face Pollution"),("somewhere-sg","Somewhere"),
   ("searching-with-my-good-eye-closed","Searching with My Good Eye Closed"),
   ("room-a-thousand-years-wide","Room a Thousand Years Wide")],
  "Soundgarden's breakthrough album, widely considered one of the finest grunge albums. Rusty Cage and Outshined became radio staples."))

w(ALBUMS/"superunknown.md", album_md("Superunknown","Soundgarden","soundgarden",1994,
  ["grunge","alternative rock","psychedelic rock"],
  [("let-me-drown","Let Me Drown"),("my-wave","My Wave"),
   ("the-day-i-tried-to-live","The Day I Tried to Live"),("black-hole-sun","Black Hole Sun"),
   ("spoonman","Spoonman"),("fell-on-black-days","Fell on Black Days"),
   ("fresh-tendrils","Fresh Tendrils"),("fourth-of-july-1994","4th of July"),
   ("like-suicide","Like Suicide")],
  "Soundgarden's masterpiece, produced by Michael Beinhorn. Debuted at number one on the Billboard 200 and won two Grammy Awards. Black Hole Sun and Spoonman are among rock's most iconic songs."))

w(ALBUMS/"down-on-the-upside.md", album_md("Down on the Upside","Soundgarden","soundgarden",1996,
  ["grunge","alternative rock","hard rock"],
  [("pretty-noose","Pretty Noose"),("rhinosaur","Rhinosaur"),("zero-chance","Zero Chance"),
   ("dusty-sg","Dusty"),("blow-up-the-outside-world","Blow Up the Outside World"),
   ("burden-in-my-hand","Burden in My Hand"),("never-the-machine-forever","Never the Machine Forever")],
  "Soundgarden's fifth and final studio album before their 1997 breakup. Produced by Adam Kasper."))

# ALICE IN CHAINS albums
w(ALBUMS/"facelift.md", album_md("Facelift","Alice in Chains","alice-in-chains",1990,
  ["grunge","heavy metal","alternative metal"],
  [("we-die-young","We Die Young"),("man-in-the-box","Man in the Box"),
   ("sea-of-sorrow","Sea of Sorrow"),("bleed-the-freak","Bleed the Freak"),
   ("i-cant-remember-aic","I Can't Remember"),("love-hate-love","Love Hate Love"),
   ("it-aint-like-that","It Ain't Like That"),("sunshine-aic","Sunshine")],
  "Alice in Chains' debut album, produced by Dave Jerden. Man in the Box became their breakthrough single."))

w(ALBUMS/"dirt.md", album_md("Dirt","Alice in Chains","alice-in-chains",1992,
  ["grunge","heavy metal","alternative metal"],
  [("them-bones","Them Bones"),("dam-that-river","Dam That River"),
   ("rain-when-i-die","Rain When I Die"),("down-in-a-hole","Down in a Hole"),
   ("sickman","Sickman"),("rooster","Rooster"),("junkhead","Junkhead"),
   ("dirt-aic","Dirt"),("would","Would?")],
  "Alice in Chains' second album and their darkest, most personal work. Exploring addiction, depression, and mortality, it is widely considered one of the greatest albums of the grunge era."))

w(ALBUMS/"alice-in-chains-1995.md", album_md("Alice in Chains","Alice in Chains","alice-in-chains",1995,
  ["grunge","alternative metal","heavy metal"],
  [("grind-aic","Grind"),("brush-away","Brush Away"),("sludge-factory","Sludge Factory"),
   ("heaven-beside-you","Heaven Beside You"),("head-creeps","Head Creeps"),
   ("again-aic","Again"),("shame-in-you","Shame in You"),
   ("god-am","God Am"),("nothin-song","Nothin' Song")],
  "Alice in Chains' self-titled third album, produced by Toby Wright. Recorded amid Layne Staley's worsening addiction."))

w(ALBUMS/"black-gives-way-to-blue.md", album_md("Black Gives Way to Blue","Alice in Chains","alice-in-chains",2009,
  ["grunge","heavy metal","alternative metal"],
  [("all-secrets-known","All Secrets Known"),("check-my-brain","Check My Brain"),
   ("last-of-my-kind","Last of My Kind"),("your-decision","Your Decision"),
   ("a-looking-in-view","A Looking in View"),("when-the-sun-rose-again","When the Sun Rose Again")],
  "Alice in Chains' reunion album with new vocalist William DuVall. A heartfelt tribute to Layne Staley."))

# MUDHONEY albums
w(ALBUMS/"mudhoney-debut.md", album_md("Mudhoney","Mudhoney","mudhoney",1989,
  ["grunge","garage rock"],
  [("touch-me-im-sick","Touch Me I'm Sick"),("sweet-young-thing","Sweet Young Thing Ain't Sweet No More"),
   ("need-mudhoney","Need"),("chain-that-door","Chain That Door"),
   ("mudride","Mudride"),("here-comes-sickness","Here Comes Sickness"),
   ("running-loaded","Running Loaded"),("the-further-i-fall","The Further I Fall")],
  "Mudhoney's debut, produced by Jack Endino. Touch Me I'm Sick became one of grunge's first anthems."))

w(ALBUMS/"every-good-boy-deserves-fudge.md", album_md("Every Good Boy Deserves Fudge","Mudhoney","mudhoney",1991,
  ["grunge","garage rock","alternative rock"],
  [("generation-spokesmodel","Generation Spokesmodel"),("let-it-slide","Let It Slide"),
   ("good-enough-mudhoney","Good Enough"),("something-so-clear","Something So Clear"),
   ("thorn-mudhoney","Thorn"),("into-the-drink","Into the Drink"),
   ("move-out","Move Out"),("shoot-the-moon","Shoot the Moon")],
  "Mudhoney's second album, produced by Conrad Uno at Egg Studios in Seattle."))

# MOTHER LOVE BONE album
w(ALBUMS/"apple.md", album_md("Apple","Mother Love Bone","mother-love-bone",1990,
  ["glam metal","grunge","alternative rock"],
  [("this-is-shangrila","This Is Shangrila"),("stardog-champion","Stardog Champion"),
   ("holy-roller-mlb","Holy Roller"),("bone-china","Bone China"),
   ("come-bite-the-apple","Come Bite the Apple"),("stargazer-mlb","Stargazer"),
   ("heartshine","Heartshine"),("captain-hi-top","Captain Hi-Top"),
   ("man-of-golden-words","Man of Golden Words"),("crown-of-thorns","Crown of Thorns")],
  "Mother Love Bone's debut and only studio album, produced by Terry Date. Released posthumously after vocalist Andrew Wood's death from a heroin overdose."))

# TEMPLE OF THE DOG album
w(ALBUMS/"temple-of-the-dog.md", album_md("Temple of the Dog","Temple of the Dog","temple-of-the-dog",1991,
  ["grunge","alternative rock","hard rock"],
  [("say-hello-2-heaven","Say Hello 2 Heaven"),("reach-down","Reach Down"),
   ("hunger-strike","Hunger Strike"),("pushin-forward-back","Pushin Forward Back"),
   ("call-me-a-dog","Call Me a Dog"),("times-of-trouble","Times of Trouble"),
   ("wooden-jesus","Wooden Jesus"),("your-saviour","Your Saviour"),
   ("four-walled-world","Four Walled World"),("all-night-thing","All Night Thing")],
  "The sole album by Temple of the Dog, produced by Rick Parashar. A tribute to Andrew Wood featuring Chris Cornell and future Pearl Jam members."))

# SCREAMING TREES albums
w(ALBUMS/"buzz-factory.md", album_md("Buzz Factory","Screaming Trees","screaming-trees",1989,
  ["grunge","psychedelic rock","alternative rock"],
  [("where-the-twain-shall-meet","Where the Twain Shall Meet"),
   ("too-far-away-st","Too Far Away"),("subtle-poison","Subtle Poison"),
   ("ivy-st","Ivy"),("yard-trip","Yard Trip"),("ive-seen-you-before","I've Seen You Before"),
   ("the-looking-glass-cracked","The Looking Glass Cracked"),
   ("end-of-the-universe","End of the Universe")],
  "Screaming Trees' fourth studio album, released on SST Records in 1989."))

w(ALBUMS/"sweet-oblivion.md", album_md("Sweet Oblivion","Screaming Trees","screaming-trees",1992,
  ["grunge","alternative rock","psychedelic rock"],
  [("shadow-of-the-season","Shadow of the Season"),("nearly-lost-you","Nearly Lost You"),
   ("dollar-bill","Dollar Bill"),("more-or-less","More or Less"),
   ("butterfly-st","Butterfly"),("for-celebrations-past","For Celebrations Past"),
   ("the-secret-kind","The Secret Kind")],
  "Screaming Trees' breakthrough album, produced by Don Fleming. Nearly Lost You became their biggest hit after appearing in the Singles soundtrack."))

w(ALBUMS/"dust-st.md", album_md("Dust","Screaming Trees","screaming-trees",1996,
  ["grunge","alternative rock","psychedelic rock"],
  [("halo-of-ashes","Halo of Ashes"),("all-i-know-st","All I Know"),
   ("sworn-and-broken","Sworn and Broken"),("dying-days","Dying Days"),
   ("make-my-mind","Make My Mind"),("witness-st","Witness"),
   ("come-see-what-love-has-done","Come See What Love Has Done")],
  "Screaming Trees' final studio album, produced by George Drakoulias. A mature and powerful swan song."))

# MELVINS albums
w(ALBUMS/"gluey-porch-treatments.md", album_md("Gluey Porch Treatments","Melvins","melvins",1987,
  ["sludge metal","noise rock","punk rock"],
  [("leetle-lulu","Leetle Lulu"),("now-a-limo","Now a Limo"),
   ("grinding-process","Grinding Process"),("as-it-was","As It Was"),
   ("disinvite-from-the-formal","Disinvite from the Formal"),
   ("snake-appeal","Snake Appeal"),("if-i-had-an-exorcism","If I Had an Exorcism"),
   ("show-off-your-red-hands","Show Off Your Red Hands")],
  "Melvins' debut album, produced by Jack Endino. A foundational work of sludge metal."))

w(ALBUMS/"houdini.md", album_md("Houdini","Melvins","melvins",1993,
  ["sludge metal","alternative rock","noise rock"],
  [("hooch","Hooch"),("night-goat","Night Goat"),("lizzy","Lizzy"),
   ("going-blind","Going Blind"),("honey-bucket","Honey Bucket"),
   ("hag-me","Hag Me"),("set-me-straight","Set Me Straight"),("sky-pup","Sky Pup")],
  "Melvins' fifth album, co-produced by Kurt Cobain and Buzz Osborne on Atlantic Records."))

# MODEST MOUSE albums
w(ALBUMS/"this-is-a-long-drive.md", album_md("This Is a Long Drive for Someone with Nothing to Think About",
  "Modest Mouse","modest-mouse",1996,
  ["indie rock","alternative rock","post-punk"],
  [("dramamine","Dramamine"),("bankrupt-on-selling","Bankrupt on Selling"),
   ("heart-cooks-brain","Heart Cooks Brain"),("convenient-parking","Convenient Parking"),
   ("lounge-mm","Lounge"),("pieces-as-big-as-my-piano","Pieces as Big as My Piano")],
  "Modest Mouse's debut album, produced by John Goodmanson. A lo-fi indie rock classic recorded in Seattle."))

w(ALBUMS/"lonesome-crowded-west.md", album_md("The Lonesome Crowded West","Modest Mouse","modest-mouse",1997,
  ["indie rock","alternative rock"],
  [("teeth-like-gods-shoeshine","Teeth Like God's Shoeshine"),("trailer-trash","Trailer Trash"),
   ("out-of-gas","Out of Gas"),("jesus-was-a-cross-maker","Jesus Was a Cross Maker"),
   ("styrofoam-boots","Styrofoam Boots"),("cowboy-dan","Cowboy Dan")],
  "Modest Mouse's second album. Rawer and more aggressive than their debut."))

w(ALBUMS/"moon-and-antarctica.md", album_md("The Moon and Antarctica","Modest Mouse","modest-mouse",2000,
  ["indie rock","alternative rock","art rock"],
  [("3rd-planet","3rd Planet"),("dark-center-of-the-universe","Dark Center of the Universe"),
   ("lives-mm","Lives"),("gravity-rides-everything","Gravity Rides Everything"),
   ("tiny-cities-made-of-ashes","Tiny Cities Made of Ashes"),
   ("oh-what-a-world-mm","Oh What a World")],
  "Widely considered Modest Mouse's masterpiece. A sprawling concept album exploring cosmic themes."))

w(ALBUMS/"good-news-for-people-who-love-bad-news.md", album_md("Good News for People Who Love Bad News",
  "Modest Mouse","modest-mouse",2004,
  ["indie rock","alternative rock","indie pop"],
  [("float-on","Float On"),("ocean-breathes-salty","Ocean Breathes Salty"),
   ("the-view-mm","The View"),("satin-in-a-coffin","Satin in a Coffin"),
   ("world-at-large","World at Large"),("dashboard-mm","Dashboard")],
  "Modest Mouse's breakthrough album. Float On became a top-40 hit and introduced them to a mainstream audience."))

# DEATH CAB albums
w(ALBUMS/"something-about-airplanes.md", album_md("Something About Airplanes",
  "Death Cab for Cutie","death-cab-for-cutie",1998,
  ["indie rock","indie pop"],
  [("bend-to-squares","Bend to Squares"),("president-of-what","President of What?"),
   ("champagne-from-a-paper-cup","Champagne from a Paper Cup"),
   ("your-bruise","Your Bruise"),("pictures-in-an-exhibition","Pictures in an Exhibition")],
  "Death Cab for Cutie's debut album, produced by Chris Walla and released on Barsuk Records."))

w(ALBUMS/"we-have-the-facts.md", album_md("We Have the Facts and We're Voting Yes",
  "Death Cab for Cutie","death-cab-for-cutie",2000,
  ["indie rock","indie pop"],
  [("title-track-dcfc","Title Track"),("the-employment-pages","The Employment Pages"),
   ("for-what-reason","For What Reason"),("lowell-ma","Lowell, MA"),
   ("company-calls","Company Calls")],
  "Death Cab for Cutie's second album, produced by Chris Walla."))

w(ALBUMS/"transatlanticism.md", album_md("Transatlanticism","Death Cab for Cutie","death-cab-for-cutie",2003,
  ["indie rock","indie pop","alternative rock"],
  [("the-new-year","The New Year"),("lightness-dcfc","Lightness"),
   ("title-and-registration","Title and Registration"),("expo-86","Expo '86"),
   ("the-sound-of-settling","The Sound of Settling"),("tiny-vessels","Tiny Vessels"),
   ("transatlanticism-song","Transatlanticism"),
   ("death-of-an-interior-decorator","Death of an Interior Decorator")],
  "Death Cab for Cutie's breakthrough album, produced by Chris Walla. The title track became their signature song."))

w(ALBUMS/"plans.md", album_md("Plans","Death Cab for Cutie","death-cab-for-cutie",2005,
  ["indie rock","indie pop","alternative rock"],
  [("marching-bands-of-manhattan","Marching Bands of Manhattan"),
   ("soul-meets-body","Soul Meets Body"),("summer-skin","Summer Skin"),
   ("what-sarah-said","What Sarah Said"),
   ("i-will-follow-you-into-the-dark","I Will Follow You into the Dark"),
   ("brothers-on-a-hotel-bed","Brothers on a Hotel Bed")],
  "Death Cab for Cutie's major label debut on Atlantic Records. I Will Follow You into the Dark became their most beloved song."))

# FLEET FOXES albums
w(ALBUMS/"fleet-foxes-debut.md", album_md("Fleet Foxes","Fleet Foxes","fleet-foxes",2008,
  ["indie folk","baroque pop","folk rock"],
  [("white-winter-hymnal","White Winter Hymnal"),("ragged-wood","Ragged Wood"),
   ("tiger-mountain-peasant-song","Tiger Mountain Peasant Song"),("meadowlarks","Meadowlarks"),
   ("blue-ridge-mountains","Blue Ridge Mountains"),
   ("he-doesnt-know-why","He Doesn't Know Why"),("heard-them-stirring","Heard Them Stirring")],
  "Fleet Foxes' self-titled debut, produced by Phil Ek. Widely acclaimed as one of the best albums of 2008."))

w(ALBUMS/"helplessness-blues.md", album_md("Helplessness Blues","Fleet Foxes","fleet-foxes",2011,
  ["indie folk","baroque pop","folk rock"],
  [("montezuma","Montezuma"),("bedouin-dress","Bedouin Dress"),("sim-sala-bim","Sim Sala Bim"),
   ("battery-kinzie","Battery Kinzie"),("the-plains-bitter-dancer","The Plains / Bitter Dancer"),
   ("helplessness-blues-song","Helplessness Blues"),
   ("the-shrine-an-argument","The Shrine / An Argument")],
  "Fleet Foxes' second album, self-produced by Robin Pecknold and Skyler Skjelset. A more ambitious and contemplative work."))

# SLEATER-KINNEY albums
w(ALBUMS/"call-the-doctor.md", album_md("Call the Doctor","Sleater-Kinney","sleater-kinney",1996,
  ["riot grrrl","indie rock","punk rock"],
  [("call-the-doctor-song","Call the Doctor"),("stay-where-you-are","Stay Where You Are"),
   ("i-wanna-be-your-joey-ramone","I Wanna Be Your Joey Ramone"),
   ("good-things-sk","Good Things"),("the-day-i-went-away","The Day I Went Away")],
  "Sleater-Kinney's second album and first with drummer Janet Weiss. Produced by John Goodmanson."))

w(ALBUMS/"dig-me-out.md", album_md("Dig Me Out","Sleater-Kinney","sleater-kinney",1997,
  ["riot grrrl","indie rock","punk rock"],
  [("dig-me-out-song","Dig Me Out"),("one-more-hour","One More Hour"),
   ("turn-it-on-sk","Turn It On"),("heart-attack-sk","Heart Attack"),
   ("words-and-guitar","Words and Guitar"),("its-enough","It's Enough"),
   ("little-babies","Little Babies")],
  "Widely considered Sleater-Kinney's breakthrough album. Produced by John Goodmanson."))

w(ALBUMS/"all-hands-on-the-bad-one.md", album_md("All Hands on the Bad One","Sleater-Kinney","sleater-kinney",2000,
  ["riot grrrl","indie rock","punk rock"],
  [("ballad-of-a-ladyman","Ballad of a Ladyman"),
   ("youre-no-rock-n-roll-fun","You're No Rock N Roll Fun"),
   ("ironclad","Ironclad"),("one-must-have","#1 Must Have"),
   ("leave-you-behind","Leave You Behind")],
  "Sleater-Kinney's fifth album, a critique of the music industry and gender politics."))

# BIKINI KILL albums
w(ALBUMS/"pussy-whipped.md", album_md("Pussy Whipped","Bikini Kill","bikini-kill",1993,
  ["riot grrrl","punk rock","feminist punk"],
  [("rebel-girl","Rebel Girl"),("liar-bk","Liar"),("star-bellied-boy","Star Bellied Boy"),
   ("carnival-bk","Carnival"),("magnet-bk","Magnet"),("feels-blind","Feels Blind"),
   ("alien-she","Alien She")],
  "Bikini Kill's debut full-length album. Rebel Girl, featuring Joan Jett, became the anthem of riot grrrl."))

w(ALBUMS/"reject-all-american.md", album_md("Reject All American","Bikini Kill","bikini-kill",1996,
  ["riot grrrl","punk rock"],
  [("statement-of-vindication","Statement of Vindication"),("rip-bk","R.I.P."),
   ("false-start","False Start"),("reject-all-american-song","Reject All American")],
  "Bikini Kill's second and final studio album."))

# HEART albums
w(ALBUMS/"dreamboat-annie.md", album_md("Dreamboat Annie","Heart","heart",1975,
  ["hard rock","classic rock","folk rock"],
  [("magic-man","Magic Man"),("crazy-on-you","Crazy on You"),
   ("dreamboat-annie-song","Dreamboat Annie"),("sing-child","Sing Child"),
   ("how-deep-it-goes","How Deep It Goes"),("lighthearted-flower","Lighthearted Flower")],
  "Heart's debut album, produced by Mike Flicker. Magic Man and Crazy on You are classic rock standards."))

w(ALBUMS/"little-queen.md", album_md("Little Queen","Heart","heart",1977,
  ["hard rock","classic rock","arena rock"],
  [("barracuda","Barracuda"),("love-alive","Love Alive"),("sylvan-song","Sylvan Song"),
   ("dream-of-the-archer","Dream of the Archer"),("kick-it-out","Kick It Out"),
   ("little-queen-song","Little Queen"),("treat-me-well","Treat Me Well")],
  "Heart's second album. Barracuda, written after a music industry deception, became one of rock's most iconic riffs."))

w(ALBUMS/"bad-animals.md", album_md("Bad Animals","Heart","heart",1987,
  ["hard rock","pop rock","arena rock"],
  [("who-will-you-run-to","Who Will You Run To"),("alone-heart","Alone"),
   ("theres-the-girl","There's the Girl"),("i-want-you-so-bad","I Want You So Bad"),
   ("wait-for-an-answer","Wait for an Answer"),("bad-animals-song","Bad Animals")],
  "Heart's commercial comeback album, produced by Ron Nevison. Alone reached number one on the Billboard Hot 100."))

# JIMI HENDRIX albums
w(ALBUMS/"are-you-experienced.md", album_md("Are You Experienced","Jimi Hendrix","jimi-hendrix",1967,
  ["psychedelic rock","blues rock","hard rock"],
  [("purple-haze","Purple Haze"),("manic-depression","Manic Depression"),
   ("hey-joe","Hey Joe"),("love-or-confusion","Love or Confusion"),
   ("may-this-be-love","May This Be Love"),("the-wind-cries-mary","The Wind Cries Mary"),
   ("fire-jh","Fire"),("foxy-lady","Foxy Lady"),("are-you-experienced-song","Are You Experienced?")],
  "Jimi Hendrix's debut album, produced by Chas Chandler. One of the most important rock albums ever recorded."))

w(ALBUMS/"axis-bold-as-love.md", album_md("Axis: Bold as Love","Jimi Hendrix","jimi-hendrix",1967,
  ["psychedelic rock","blues rock","hard rock"],
  [("exp-jh","EXP"),("up-from-the-skies","Up from the Skies"),
   ("spanish-castle-magic","Spanish Castle Magic"),("little-wing","Little Wing"),
   ("if-6-was-9","If 6 Was 9"),("castles-made-of-sand","Castles Made of Sand"),
   ("bold-as-love","Bold as Love")],
  "The second Jimi Hendrix Experience album. Little Wing is one of the most covered guitar pieces in rock history."))

w(ALBUMS/"electric-ladyland.md", album_md("Electric Ladyland","Jimi Hendrix","jimi-hendrix",1968,
  ["psychedelic rock","blues rock","hard rock"],
  [("crosstown-traffic","Crosstown Traffic"),("voodoo-chile","Voodoo Chile"),
   ("gypsy-eyes","Gypsy Eyes"),("burning-of-the-midnight-lamp","Burning of the Midnight Lamp"),
   ("all-along-the-watchtower","All Along the Watchtower"),
   ("voodoo-child-slight-return","Voodoo Child (Slight Return)"),
   ("have-you-ever-been","Have You Ever Been (to Electric Ladyland)")],
  "Hendrix's third and final studio album, self-produced. All Along the Watchtower and Voodoo Child (Slight Return) are among his greatest achievements."))

# SMASHING PUMPKINS albums
w(ALBUMS/"gish.md", album_md("Gish","Smashing Pumpkins","smashing-pumpkins",1991,
  ["alternative rock","shoegaze","grunge"],
  [("i-am-one-sp","I Am One"),("siva","Siva"),("rhinoceros","Rhinoceros"),
   ("bury-me","Bury Me"),("crush-sp","Crush"),("suffer","Suffer"),
   ("snail-sp","Snail"),("tristessa","Tristessa")],
  "Smashing Pumpkins' debut album, produced by Butch Vig and Bjorn Thorsrud. A dense, layered rock record."))

w(ALBUMS/"siamese-dream.md", album_md("Siamese Dream","Smashing Pumpkins","smashing-pumpkins",1993,
  ["alternative rock","grunge","shoegaze"],
  [("cherub-rock","Cherub Rock"),("quiet-sp","Quiet"),("today-sp","Today"),
   ("hummer","Hummer"),("rocket-sp","Rocket"),("disarm","Disarm"),
   ("soma","Soma"),("geek-usa","Geek U.S.A."),("mayonaise","Mayonaise"),
   ("spaceboy-sp","Spaceboy"),("silverfuck","Silverfuck"),("luna-sp","Luna")],
  "Produced by Butch Vig, Siamese Dream is one of the defining alternative rock albums. Billy Corgan played almost all instruments due to band tensions."))

w(ALBUMS/"mellon-collie.md", album_md("Mellon Collie and the Infinite Sadness",
  "Smashing Pumpkins","smashing-pumpkins",1995,
  ["alternative rock","art rock","dream pop"],
  [("tonight-tonight","Tonight Tonight"),("jellybelly","Jellybelly"),
   ("zero-sp","Zero"),("bullet-with-butterfly-wings","Bullet with Butterfly Wings"),
   ("to-forgive","To Forgive"),("nineteen-seventy-nine","1979"),
   ("tales-of-a-scorched-earth","Tales of a Scorched Earth"),
   ("bodies-sp","Bodies"),("thirty-three","Thirty-Three")],
  "Smashing Pumpkins' ambitious double album, produced by Flood and Alan Moulder. Bullet with Butterfly Wings and 1979 became their biggest hits."))

w(ALBUMS/"adore.md", album_md("Adore","Smashing Pumpkins","smashing-pumpkins",1998,
  ["alternative rock","dream pop","electronic"],
  [("to-sheila","To Sheila"),("ava-adore","Ava Adore"),("perfect-sp","Perfect"),
   ("daphne-descends","Daphne Descends"),("once-upon-a-time-sp","Once Upon a Time"),
   ("crestfallen","Crestfallen"),("appels-oranjes","Appels + Oranjes"),
   ("tale-of-dusty-and-demon-king","The Tale of Dusty and Demon King")],
  "Smashing Pumpkins' fourth album, self-produced by Billy Corgan. A more electronic and introspective direction."))

# LIZ PHAIR albums
w(ALBUMS/"exile-in-guyville.md", album_md("Exile in Guyville","Liz Phair","liz-phair",1993,
  ["indie rock","lo-fi","alternative rock"],
  [("six-foot-one","6'1\""),("help-me-mary","Help Me Mary"),
   ("glory-lp","Glory"),("dance-of-the-seven-veils","Dance of the Seven Veils"),
   ("never-said","Never Said"),("soap-star-joe","Soap Star Joe"),
   ("explain-it-to-me","Explain It to Me"),("fuck-and-run","Fuck and Run"),
   ("divorce-song","Divorce Song"),("stratford-on-guy","Stratford-on-Guy"),
   ("girls-girls-girls-lp","Girls! Girls! Girls!"),("canary-lp","Canary")],
  "Liz Phair's debut, produced by Brad Wood. A track-by-track response to the Rolling Stones' Exile on Main St., it is one of the most important indie rock albums of the 1990s."))

w(ALBUMS/"whip-smart.md", album_md("Whip-Smart","Liz Phair","liz-phair",1994,
  ["indie rock","alternative rock"],
  [("chopsticks-lp","Chopsticks"),("supernova","Supernova"),
   ("support-system","Support System"),("cinco-de-mayo","Cinco de Mayo"),
   ("x-ray-man","X-Ray Man"),("jealousy-lp","Jealousy"),
   ("main-street-saloon","Main Street Saloon"),("headache-lp","Headache"),
   ("alice-springs","Alice Springs")],
  "Liz Phair's second album, produced by Brad Wood. A more polished but still witty follow-up."))

# WILCO albums
w(ALBUMS/"am-wilco.md", album_md("AM","Wilco","wilco",1995,
  ["alternative country","alt-country","indie rock"],
  [("i-must-be-high","I Must Be High"),("casino-queen","Casino Queen"),
   ("box-full-of-letters","Box Full of Letters"),("shouldnt-be-ashamed","Shouldn't Be Ashamed"),
   ("pick-up-the-change","Pick Up the Change"),("passenger-side","Passenger Side"),
   ("dash-7","Dash 7"),("blue-eyed-soul","Blue Eyed Soul")],
  "Wilco's debut album. An alt-country record showcasing Jeff Tweedy's post-Uncle Tupelo songwriting."))

w(ALBUMS/"being-there.md", album_md("Being There","Wilco","wilco",1996,
  ["alternative country","indie rock","art rock"],
  [("misunderstood-wilco","Misunderstood"),("far-far-away","Far Far Away"),
   ("monday-wilco","Monday"),("forget-the-flowers","Forget the Flowers"),
   ("red-eyed-and-blue","Red-Eyed and Blue"),("hotel-arizona","Hotel Arizona"),
   ("sunken-treasure","Sunken Treasure"),("outtasite","Outtasite (Outtamind)")],
  "Wilco's ambitious double album. A transition from alt-country toward their experimental rock future."))

w(ALBUMS/"yankee-hotel-foxtrot.md", album_md("Yankee Hotel Foxtrot","Wilco","wilco",2002,
  ["indie rock","art rock","alternative rock"],
  [("i-am-trying-to-break-your-heart","I Am Trying to Break Your Heart"),
   ("kamera","Kamera"),("radio-cure","Radio Cure"),("war-on-war","War on War"),
   ("jesus-etc","Jesus, etc."),("ashes-of-american-flags","Ashes of American Flags"),
   ("heavy-metal-drummer","Heavy Metal Drummer"),("im-the-man-who-loves-you","I'm the Man Who Loves You"),
   ("pot-kettle-black","Pot Kettle Black"),("poor-places","Poor Places"),
   ("reservations-wilco","Reservations")],
  "Wilco's masterpiece, co-produced by Jim O'Rourke. Initially rejected by Reprise Records, it became one of the most acclaimed albums of the decade."))

w(ALBUMS/"a-ghost-is-born.md", album_md("A Ghost Is Born","Wilco","wilco",2004,
  ["indie rock","art rock","noise rock"],
  [("at-least-thats-what-you-said","At Least That's What You Said"),
   ("hell-is-chrome","Hell Is Chrome"),("spiders-kidsmoke","Spiders (Kidsmoke)"),
   ("muzzle-of-bees","Muzzle of Bees"),("hummingbird-wilco","Hummingbird"),
   ("handshake-drugs","Handshake Drugs"),("the-late-greats","The Late Greats")],
  "Wilco's fifth album, featuring the 10-minute noise epic Spiders (Kidsmoke)."))

# CHEAP TRICK albums
w(ALBUMS/"cheap-trick-debut.md", album_md("Cheap Trick","Cheap Trick","cheap-trick",1977,
  ["hard rock","power pop"],
  [("elo-kiddies","ELO Kiddies"),("daddy-should-have-stayed","Daddy Should Have Stayed in High School"),
   ("taxman-mr-thief","Taxman, Mr. Thief"),("cry-cry","Cry Cry"),
   ("oh-candy","Oh Candy"),("hes-a-whore","He's a Whore"),
   ("mandocello","Mandocello"),("ballad-of-tv-violence","The Ballad of TV Violence"),
   ("lovin-money","Lovin' Money")],
  "Cheap Trick's self-titled debut, produced by Tom Werman. A raw power pop/hard rock statement."))

w(ALBUMS/"in-color.md", album_md("In Color","Cheap Trick","cheap-trick",1977,
  ["hard rock","power pop","arena rock"],
  [("hello-there","Hello There"),("big-eyes","Big Eyes"),("downed","Downed"),
   ("i-want-you-to-want-me","I Want You to Want Me"),("youre-all-talk","You're All Talk"),
   ("oh-caroline","Oh Caroline"),("clock-strikes-ten","Clock Strikes Ten"),
   ("southern-girls","Southern Girls"),("come-on-come-on","Come On, Come On, Come On")],
  "Cheap Trick's second album, produced by Tom Werman. I Want You to Want Me became one of their signature songs."))

w(ALBUMS/"at-budokan.md", album_md("At Budokan","Cheap Trick","cheap-trick",1978,
  ["hard rock","power pop","live"],
  [("hello-there-live","Hello There (Live)"),("i-want-you-to-want-me-live","I Want You to Want Me (Live)"),
   ("surrender-ct","Surrender"),("aint-that-a-shame","Ain't That a Shame"),
   ("goodnight-now","Goodnight Now")],
  "Cheap Trick's breakthrough live album, recorded in Tokyo. Captured the hysteria of their Japanese fanbase and became one of the best-selling live albums of all time."))

# THE JESUS LIZARD albums
w(ALBUMS/"goat.md", album_md("Goat","The Jesus Lizard","the-jesus-lizard",1991,
  ["noise rock","post-hardcore","alternative rock"],
  [("then-comes-dudley","Then Comes Dudley"),("mouth-breather","Mouth Breather"),
   ("nub","Nub"),("seasick-jl","Seasick"),("monkey-trick","Monkey Trick"),
   ("karpis","Karpis"),("south-mouth","South Mouth"),
   ("lady-shoes","Lady Shoes"),("rodeo-in-joliet","Rodeo in Joliet")],
  "The Jesus Lizard's second album, produced by Steve Albini. A landmark of noise rock."))

w(ALBUMS/"liar.md", album_md("Liar","The Jesus Lizard","the-jesus-lizard",1992,
  ["noise rock","post-hardcore","alternative rock"],
  [("boilermaker","Boilermaker"),("gladiator-jl","Gladiator"),
   ("the-art-of-self-defense","The Art of Self-Defense"),("slave-ship","Slave Ship"),
   ("puss","Puss"),("whirl","Whirl"),("rope-jl","Rope"),("perk","Perk")],
  "The Jesus Lizard's third album, also produced by Steve Albini. Puss was released as a split single with Nirvana."))

# URGE OVERKILL album
w(ALBUMS/"saturation.md", album_md("Saturation","Urge Overkill","urge-overkill",1993,
  ["alternative rock","indie rock","hard rock"],
  [("sister-havana","Sister Havana"),("tequila-sundae","Tequila Sundae"),
   ("positive-bleeding","Positive Bleeding"),("back-on-me","Back on Me"),
   ("woman-2-woman","Woman 2 Woman"),("cracker-uo","Cracker"),
   ("dropout","Dropout"),("the-stalker","The Stalker")],
  "Urge Overkill's Geffen debut, produced by Butch Vig. Their most commercially successful album."))

# TORTOISE albums
w(ALBUMS/"millions-now-living-will-never-die.md", album_md("Millions Now Living Will Never Die",
  "Tortoise","tortoise",1996,
  ["post-rock","experimental","krautrock"],
  [("djed","Djed"),("glass-museum","Glass Museum"),("a-survey","A Survey"),
   ("the-taut-and-tame","The Taut and Tame"),
   ("dear-grandma-and-grandpa","Dear Grandma and Grandpa"),
   ("along-the-banks-of-rivers","Along the Banks of Rivers")],
  "Tortoise's second album. The opening track Djed runs 20 minutes and is a defining work of post-rock."))

w(ALBUMS/"tnt-tortoise.md", album_md("TNT","Tortoise","tortoise",1998,
  ["post-rock","experimental","jazz fusion"],
  [("tnt-song","TNT"),("in-sarah-mencins","In Sarah, Mencin's..."),
   ("the-equator","The Equator"),("a-simple-way-to-go-faster","A Simple Way to Go Faster Than Light That Does Not Work"),
   ("the-science-of-what","The Science of What"),
   ("swung-from-the-gutters","Swung from the Gutters"),("ten-day-interval","Ten-Day Interval")],
  "Tortoise's third album. A more jazz-influenced post-rock exploration."))

# MUDDY WATERS albums
w(ALBUMS/"folk-singer.md", album_md("Folk Singer","Muddy Waters","muddy-waters",1964,
  ["Chicago blues","acoustic blues","delta blues"],
  [("my-home-is-in-the-delta","My Home Is in the Delta"),("long-distance-mw","Long Distance"),
   ("my-captain","My Captain"),("good-morning-little-schoolgirl","Good Morning Little Schoolgirl"),
   ("ive-got-my-mojo-working","I've Got My Mojo Working"),
   ("feel-like-going-home","Feel Like Going Home"),
   ("the-same-thing-mw","The Same Thing"),("walking-blues","Walking Blues")],
  "Muddy Waters' intimate acoustic album, produced by Sam Charters. A stripped-down return to his Delta roots."))

w(ALBUMS/"electric-mud.md", album_md("Electric Mud","Muddy Waters","muddy-waters",1968,
  ["Chicago blues","psychedelic blues","electric blues"],
  [("i-just-want-to-make-love-to-you","I Just Want to Make Love to You"),
   ("hoochie-coochie-man","Hoochie Coochie Man"),
   ("lets-spend-the-night-together-mw","Let's Spend the Night Together"),
   ("shes-all-right","She's All Right"),("im-a-man-mw","I'm a Man"),
   ("tom-cat","Tom Cat"),("herbert-harpers-free-press-news","Herbert Harper's Free Press News")],
  "Muddy Waters' psychedelic blues experiment, produced by Marshall Chess. A controversial but influential record."))

# BUDDY GUY album
w(ALBUMS/"damn-right-ive-got-the-blues.md", album_md("Damn Right, I've Got the Blues",
  "Buddy Guy","buddy-guy",1991,
  ["Chicago blues","blues rock","electric blues"],
  [("damn-right-ive-got-the-blues-song","Damn Right, I've Got the Blues"),
   ("where-is-the-next-one-coming-from","Where Is the Next One Coming From"),
   ("five-long-years","Five Long Years"),("pretty-baby-bg","Pretty Baby"),
   ("let-me-love-you-baby","Let Me Love You Baby"),
   ("too-broke-to-spend-the-night","Too Broke to Spend the Night"),
   ("early-in-the-morning","Early in the Morning")],
  "Buddy Guy's comeback album, produced by John Porter. Won a Grammy for Best Traditional Blues Album."))

# HOWLIN WOLF albums
w(ALBUMS/"moanin-in-the-moonshine.md", album_md("Moanin' in the Moonshine",
  "Howlin' Wolf","howlin-wolf",1959,
  ["Chicago blues","electric blues","delta blues"],
  [("moanin-at-midnight","Moanin' at Midnight"),("how-many-more-years","How Many More Years"),
   ("smokestack-lightning","Smokestack Lightning"),("baby-how-long","Baby How Long"),
   ("no-place-to-go-hw","No Place to Go"),("all-night-boogie","All Night Boogie"),
   ("evil-hw","Evil"),("im-the-wolf","I'm the Wolf")],
  "Howlin' Wolf's debut Chess Records album, compiled from early singles. Smokestack Lightning became one of the most recognizable blues songs ever recorded."))

w(ALBUMS/"the-real-folk-blues.md", album_md("The Real Folk Blues","Howlin' Wolf","howlin-wolf",1966,
  ["Chicago blues","electric blues"],
  [("smokestack-lightning-ii","Smokestack Lightning (Alt. Version)"),
   ("back-door-man","Back Door Man"),("wang-dang-doodle","Wang Dang Doodle"),
   ("the-red-rooster","The Red Rooster"),("shake-for-me","Shake for Me"),
   ("howlin-for-my-darling","Howlin' for My Darling"),
   ("hidden-charms","Hidden Charms"),("killing-floor","Killing Floor")],
  "A compilation of Howlin' Wolf's Chess Records recordings, produced by Willie Dixon. Back Door Man and Killing Floor influenced countless rock bands."))

# BIG BLACK albums
w(ALBUMS/"atomizer.md", album_md("Atomizer","Big Black","big-black",1986,
  ["noise rock","post-punk","hardcore punk"],
  [("jordan-minnesota","Jordan, Minnesota"),("passing-complexion","Passing Complexion"),
   ("big-money-bb","Big Money"),("kerosene","Kerosene"),("bad-houses","Bad Houses"),
   ("fists-of-love","Fists of Love"),("stinking-drunk","Stinking Drunk"),
   ("cables-bb","Cables"),("strange-things-bb","Strange Things")],
  "Big Black's debut full-length album, self-produced by Steve Albini. Kerosene became their signature song."))

w(ALBUMS/"songs-about-fucking.md", album_md("Songs About Fucking","Big Black","big-black",1987,
  ["noise rock","post-punk","hardcore punk"],
  [("power-of-independent-trucking","The Power of Independent Trucking"),
   ("the-ugly-american","The Ugly American"),("bad-penny","Bad Penny"),
   ("pavement-saw","Pavement Saw"),("tiny-bb","Tiny"),
   ("kasimir-s-pulaski-day","Kasimir S. Pulaski Day"),("ergot","Ergot"),
   ("precious-thing-bb","Precious Thing"),("colombian-necktie","Colombian Necktie"),
   ("kitty-empire","Kitty Empire")],
  "Big Black's final album. Their most confrontational and influential record."))

# SHELLAC albums
w(ALBUMS/"at-action-park.md", album_md("At Action Park","Shellac","shellac",1994,
  ["noise rock","post-hardcore","math rock"],
  [("my-black-ass","My Black Ass"),("pull-the-cup","Pull the Cup"),
   ("the-admiral","The Admiral"),("crow-shellac","Crow"),("trem-two","Trem Two"),
   ("dog-and-pony-show","Dog and Pony Show"),("boches-dick","Boche's Dick"),
   ("a-minute-shellac","A Minute")],
  "Shellac's debut album, self-produced by Steve Albini. A spare, precise noise rock statement."))

w(ALBUMS/"terraform.md", album_md("Terraform","Shellac","shellac",1998,
  ["noise rock","post-hardcore","math rock"],
  [("didnt-we-deserve-a-look","Didn't We Deserve a Look at You the Way You Really Are"),
   ("this-is-a-picture-shellac","This Is a Picture"),("disgrace-shellac","Disgrace"),
   ("watch-song","Watch Song"),("canada-shellac","Canada"),
   ("rush-job","Rush Job"),("copper-shellac","Copper")],
  "Shellac's second album. More melodic and varied than their debut, but no less intense."))

print(f"After albums: {_c} created, {_s} skipped")

# ══════════════════════════════════════════════════════════════ SONGS ════

# ── SOUNDGARDEN ──────────────────────────────────────────────────────────
sg_members = [
  ("chris-cornell","Chris Cornell","vocals/guitar"),
  ("kim-thayil","Kim Thayil","lead guitar"),
  ("hiro-yamamoto","Hiro Yamamoto","bass"),
  ("matt-cameron","Matt Cameron","drums"),
]
sg_members2 = [
  ("chris-cornell","Chris Cornell","vocals/guitar"),
  ("kim-thayil","Kim Thayil","lead guitar"),
  ("ben-shepherd","Ben Shepherd","bass"),
  ("matt-cameron","Matt Cameron","drums"),
]

def sgsong(slug, title, album_slug, credits_extra=None):
  cr = [c for c in sg_members] + (credits_extra or [])
  w(SONGS/f"{slug}.md", song_md(title, "Soundgarden", "soundgarden", album_slug, cr))

def sgsong2(slug, title, album_slug, credits_extra=None):
  cr = [c for c in sg_members2] + (credits_extra or [])
  w(SONGS/f"{slug}.md", song_md(title, "Soundgarden", "soundgarden", album_slug, cr))

jack_prod = [("jack-endino","Jack Endino","producer")]
terry_jack = [("terry-date","Terry Date","producer"),("jack-endino","Jack Endino","producer")]
beinhorn_prod = [("michael-beinhorn","Michael Beinhorn","producer")]
adam_prod = [("adam-kasper","Adam Kasper","producer")]

# Ultramega OK
sgsong("flower-sg","Flower","ultramega-ok", jack_prod)
sgsong("all-your-lies","All Your Lies","ultramega-ok", jack_prod)
sgsong("six-six-seven","667","ultramega-ok", jack_prod)
sgsong("beyond-the-wheel","Beyond the Wheel","ultramega-ok", jack_prod)
sgsong("fourth-of-july-1988","4th of July","ultramega-ok", jack_prod)
sgsong("mood-for-trouble","Mood for Trouble","ultramega-ok", jack_prod)
sgsong("circle-of-power","Circle of Power","ultramega-ok", jack_prod)
sgsong("he-didnt","He Didn't","ultramega-ok", jack_prod)
# Louder Than Love
sgsong("ugly-truth","Ugly Truth","louder-than-love", terry_jack)
sgsong("hands-all-over","Hands All Over","louder-than-love", terry_jack)
sgsong("get-on-the-snake","Get on the Snake","louder-than-love", terry_jack)
sgsong("big-dumb-sex","Big Dumb Sex","louder-than-love", terry_jack)
sgsong("full-on-kevins-mom","Full on Kevin's Mom","louder-than-love", terry_jack)
sgsong("no-wrong-no-right","No Wrong No Right","louder-than-love", terry_jack)
sgsong("loud-love","Loud Love","louder-than-love", terry_jack)
# Badmotorfinger (Ben Shepherd replaces Hiro Yamamoto)
sgsong2("rusty-cage","Rusty Cage","badmotorfinger", terry_jack)
sgsong2("outshined","Outshined","badmotorfinger", terry_jack)
sgsong2("slaves-and-bulldozers","Slaves and Bulldozers","badmotorfinger", terry_jack)
sgsong2("jesus-christ-pose","Jesus Christ Pose","badmotorfinger", terry_jack)
sgsong2("face-pollution","Face Pollution","badmotorfinger", terry_jack)
sgsong2("somewhere-sg","Somewhere","badmotorfinger", terry_jack)
sgsong2("searching-with-my-good-eye-closed","Searching with My Good Eye Closed","badmotorfinger", terry_jack)
sgsong2("room-a-thousand-years-wide","Room a Thousand Years Wide","badmotorfinger", terry_jack)
# Superunknown
sgsong2("let-me-drown","Let Me Drown","superunknown", beinhorn_prod)
sgsong2("my-wave","My Wave","superunknown", beinhorn_prod)
sgsong2("the-day-i-tried-to-live","The Day I Tried to Live","superunknown", beinhorn_prod)
sgsong2("black-hole-sun","Black Hole Sun","superunknown", beinhorn_prod)
sgsong2("spoonman","Spoonman","superunknown", beinhorn_prod)
sgsong2("fell-on-black-days","Fell on Black Days","superunknown", beinhorn_prod)
sgsong2("fresh-tendrils","Fresh Tendrils","superunknown", beinhorn_prod)
sgsong2("fourth-of-july-1994","4th of July","superunknown", beinhorn_prod)
sgsong2("like-suicide","Like Suicide","superunknown", beinhorn_prod)
# Down on the Upside
sgsong2("pretty-noose","Pretty Noose","down-on-the-upside", adam_prod)
sgsong2("rhinosaur","Rhinosaur","down-on-the-upside", adam_prod)
sgsong2("zero-chance","Zero Chance","down-on-the-upside", adam_prod)
sgsong2("dusty-sg","Dusty","down-on-the-upside", adam_prod)
sgsong2("blow-up-the-outside-world","Blow Up the Outside World","down-on-the-upside", adam_prod)
sgsong2("burden-in-my-hand","Burden in My Hand","down-on-the-upside", adam_prod)
sgsong2("never-the-machine-forever","Never the Machine Forever","down-on-the-upside", adam_prod)

# ── ALICE IN CHAINS ───────────────────────────────────────────────────────
aic_credits = [
  ("layne-staley","Layne Staley","vocals"),
  ("jerry-cantrell","Jerry Cantrell","guitar/vocals"),
  ("mike-starr","Mike Starr","bass"),
  ("sean-kinney","Sean Kinney","drums"),
]
aic_credits2 = [
  ("layne-staley","Layne Staley","vocals"),
  ("jerry-cantrell","Jerry Cantrell","guitar/vocals"),
  ("mike-inez","Mike Inez","bass"),
  ("sean-kinney","Sean Kinney","drums"),
]
dave_jerden = [("dave-jerden","Dave Jerden","producer")]
toby_wright = [("toby-wright","Toby Wright","producer")]

def aicsong(slug, title, album_slug, line=1):
  cr = (aic_credits if line==1 else aic_credits2) + dave_jerden
  w(SONGS/f"{slug}.md", song_md(title,"Alice in Chains","alice-in-chains",album_slug,cr))

def aicsong2(slug, title, album_slug):
  cr = aic_credits2 + toby_wright
  w(SONGS/f"{slug}.md", song_md(title,"Alice in Chains","alice-in-chains",album_slug,cr))

for s,t in [("we-die-young","We Die Young"),("man-in-the-box","Man in the Box"),
            ("sea-of-sorrow","Sea of Sorrow"),("bleed-the-freak","Bleed the Freak"),
            ("i-cant-remember-aic","I Can't Remember"),("love-hate-love","Love Hate Love"),
            ("it-aint-like-that","It Ain't Like That"),("sunshine-aic","Sunshine")]:
  aicsong(s,t,"facelift",1)
for s,t in [("them-bones","Them Bones"),("dam-that-river","Dam That River"),
            ("rain-when-i-die","Rain When I Die"),("down-in-a-hole","Down in a Hole"),
            ("sickman","Sickman"),("rooster","Rooster"),("junkhead","Junkhead"),
            ("dirt-aic","Dirt"),("would","Would?")]:
  aicsong(s,t,"dirt",2)
for s,t in [("grind-aic","Grind"),("brush-away","Brush Away"),("sludge-factory","Sludge Factory"),
            ("heaven-beside-you","Heaven Beside You"),("head-creeps","Head Creeps"),
            ("again-aic","Again"),("shame-in-you","Shame in You"),
            ("god-am","God Am"),("nothin-song","Nothin' Song")]:
  aicsong2(s,t,"alice-in-chains-1995")

# Black Gives Way to Blue - William DuVall lineup
bgwtb_cr = [("william-duvall","William DuVall","vocals"),
            ("jerry-cantrell","Jerry Cantrell","guitar/vocals"),
            ("mike-inez","Mike Inez","bass"),
            ("sean-kinney","Sean Kinney","drums"),
            ("nick-raskulinecz","Nick Raskulinecz","producer")]
for s,t in [("all-secrets-known","All Secrets Known"),("check-my-brain","Check My Brain"),
            ("last-of-my-kind","Last of My Kind"),("your-decision","Your Decision"),
            ("a-looking-in-view","A Looking in View"),("when-the-sun-rose-again","When the Sun Rose Again")]:
  w(SONGS/f"{s}.md", song_md(t,"Alice in Chains","alice-in-chains","black-gives-way-to-blue",bgwtb_cr))

# ── MUDHONEY ──────────────────────────────────────────────────────────────
mud_cr = [("mark-arm","Mark Arm","vocals/guitar"),
          ("steve-turner","Steve Turner","guitar"),
          ("matt-lukin","Matt Lukin","bass"),
          ("dan-peters","Dan Peters","drums")]
for s,t,alb,ex in [
    ("touch-me-im-sick","Touch Me I'm Sick","mudhoney-debut",[]),
    ("sweet-young-thing","Sweet Young Thing Ain't Sweet No More","mudhoney-debut",[]),
    ("need-mudhoney","Need","mudhoney-debut",[]),
    ("chain-that-door","Chain That Door","mudhoney-debut",[]),
    ("mudride","Mudride","mudhoney-debut",[]),
    ("here-comes-sickness","Here Comes Sickness","mudhoney-debut",[]),
    ("running-loaded","Running Loaded","mudhoney-debut",[]),
    ("the-further-i-fall","The Further I Fall","mudhoney-debut",[]),
    ("generation-spokesmodel","Generation Spokesmodel","every-good-boy-deserves-fudge",[]),
    ("let-it-slide","Let It Slide","every-good-boy-deserves-fudge",[]),
    ("good-enough-mudhoney","Good Enough","every-good-boy-deserves-fudge",[]),
    ("something-so-clear","Something So Clear","every-good-boy-deserves-fudge",[]),
    ("thorn-mudhoney","Thorn","every-good-boy-deserves-fudge",[]),
    ("into-the-drink","Into the Drink","every-good-boy-deserves-fudge",[]),
    ("move-out","Move Out","every-good-boy-deserves-fudge",[]),
    ("shoot-the-moon","Shoot the Moon","every-good-boy-deserves-fudge",[]),
  ]:
  prod = jack_prod if "mudhoney-debut" in alb else [("conrad-uno","Conrad Uno","producer")]
  w(SONGS/f"{s}.md", song_md(t,"Mudhoney","mudhoney",alb,mud_cr+prod))

# ── MOTHER LOVE BONE ──────────────────────────────────────────────────────
mlb_cr = [("andrew-wood","Andrew Wood","vocals"),
          ("stone-gossard","Stone Gossard","guitar"),
          ("bruce-fairweather","Bruce Fairweather","guitar"),
          ("jeff-ament","Jeff Ament","bass"),
          ("greg-gilmore","Greg Gilmore","drums"),
          ("terry-date","Terry Date","producer")]
for s,t in [("this-is-shangrila","This Is Shangrila"),("stardog-champion","Stardog Champion"),
            ("holy-roller-mlb","Holy Roller"),("bone-china","Bone China"),
            ("come-bite-the-apple","Come Bite the Apple"),("stargazer-mlb","Stargazer"),
            ("heartshine","Heartshine"),("captain-hi-top","Captain Hi-Top"),
            ("man-of-golden-words","Man of Golden Words"),("crown-of-thorns","Crown of Thorns")]:
  w(SONGS/f"{s}.md", song_md(t,"Mother Love Bone","mother-love-bone","apple",mlb_cr))

# ── TEMPLE OF THE DOG ─────────────────────────────────────────────────────
totd_cr = [("chris-cornell","Chris Cornell","vocals/guitar"),
           ("eddie-vedder","Eddie Vedder","vocals"),
           ("stone-gossard","Stone Gossard","guitar"),
           ("mike-mccready","Mike McCready","lead guitar"),
           ("jeff-ament","Jeff Ament","bass"),
           ("matt-cameron","Matt Cameron","drums"),
           ("rick-parashar","Rick Parashar","producer")]
for s,t in [("say-hello-2-heaven","Say Hello 2 Heaven"),("reach-down","Reach Down"),
            ("hunger-strike","Hunger Strike"),("pushin-forward-back","Pushin Forward Back"),
            ("call-me-a-dog","Call Me a Dog"),("times-of-trouble","Times of Trouble"),
            ("wooden-jesus","Wooden Jesus"),("your-saviour","Your Saviour"),
            ("four-walled-world","Four Walled World"),("all-night-thing","All Night Thing")]:
  w(SONGS/f"{s}.md", song_md(t,"Temple of the Dog","temple-of-the-dog","temple-of-the-dog",totd_cr))

# ── SCREAMING TREES ───────────────────────────────────────────────────────
st_cr = [("mark-lanegan","Mark Lanegan","vocals"),
         ("gary-lee-conner","Gary Lee Conner","guitar"),
         ("van-conner","Van Conner","bass"),
         ("barrett-martin","Barrett Martin","drums")]
st_cr_early = [("mark-lanegan","Mark Lanegan","vocals"),
               ("gary-lee-conner","Gary Lee Conner","guitar"),
               ("van-conner","Van Conner","bass"),
               ("mark-pickerel","Mark Pickerel","drums")]
don_prod = [("don-fleming","Don Fleming","producer")]
george_prod = [("george-drakoulias","George Drakoulias","producer")]
for s,t in [("where-the-twain-shall-meet","Where the Twain Shall Meet"),
            ("too-far-away-st","Too Far Away"),("subtle-poison","Subtle Poison"),
            ("ivy-st","Ivy"),("yard-trip","Yard Trip"),
            ("ive-seen-you-before","I've Seen You Before"),
            ("the-looking-glass-cracked","The Looking Glass Cracked"),
            ("end-of-the-universe","End of the Universe")]:
  w(SONGS/f"{s}.md", song_md(t,"Screaming Trees","screaming-trees","buzz-factory",
                              st_cr_early+jack_prod))
for s,t in [("shadow-of-the-season","Shadow of the Season"),("nearly-lost-you","Nearly Lost You"),
            ("dollar-bill","Dollar Bill"),("more-or-less","More or Less"),
            ("butterfly-st","Butterfly"),("for-celebrations-past","For Celebrations Past"),
            ("the-secret-kind","The Secret Kind")]:
  w(SONGS/f"{s}.md", song_md(t,"Screaming Trees","screaming-trees","sweet-oblivion",
                              st_cr+don_prod))
for s,t in [("halo-of-ashes","Halo of Ashes"),("all-i-know-st","All I Know"),
            ("sworn-and-broken","Sworn and Broken"),("dying-days","Dying Days"),
            ("make-my-mind","Make My Mind"),("witness-st","Witness"),
            ("come-see-what-love-has-done","Come See What Love Has Done")]:
  w(SONGS/f"{s}.md", song_md(t,"Screaming Trees","screaming-trees","dust-st",
                              st_cr+george_prod))

# ── MELVINS ───────────────────────────────────────────────────────────────
mel_cr = [("buzz-osborne","Buzz Osborne","vocals/guitar"),
          ("dale-crover","Dale Crover","drums")]
mel_cr_early = mel_cr + [("lori-black","Lori Black","bass")]
kc_prod = [("kurt-cobain","Kurt Cobain","producer"),("buzz-osborne","Buzz Osborne","producer")]
for s,t in [("leetle-lulu","Leetle Lulu"),("now-a-limo","Now a Limo"),
            ("grinding-process","Grinding Process"),("as-it-was","As It Was"),
            ("disinvite-from-the-formal","Disinvite from the Formal"),
            ("snake-appeal","Snake Appeal"),("if-i-had-an-exorcism","If I Had an Exorcism"),
            ("show-off-your-red-hands","Show Off Your Red Hands")]:
  w(SONGS/f"{s}.md", song_md(t,"Melvins","melvins","gluey-porch-treatments",
                              mel_cr_early+jack_prod))
for s,t in [("hooch","Hooch"),("night-goat","Night Goat"),("lizzy","Lizzy"),
            ("going-blind","Going Blind"),("honey-bucket","Honey Bucket"),
            ("hag-me","Hag Me"),("set-me-straight","Set Me Straight"),("sky-pup","Sky Pup")]:
  w(SONGS/f"{s}.md", song_md(t,"Melvins","melvins","houdini",
                              mel_cr+kc_prod))

# ── MODEST MOUSE ──────────────────────────────────────────────────────────
mm_cr = [("isaac-brock","Isaac Brock","vocals/guitar"),
         ("jeremiah-green","Jeremiah Green","drums"),
         ("eric-judy","Eric Judy","bass")]
jg_prod = [("john-goodmanson","John Goodmanson","producer")]
for s,t,alb in [
    ("dramamine","Dramamine","this-is-a-long-drive"),
    ("bankrupt-on-selling","Bankrupt on Selling","this-is-a-long-drive"),
    ("heart-cooks-brain","Heart Cooks Brain","this-is-a-long-drive"),
    ("convenient-parking","Convenient Parking","this-is-a-long-drive"),
    ("lounge-mm","Lounge","this-is-a-long-drive"),
    ("pieces-as-big-as-my-piano","Pieces as Big as My Piano","this-is-a-long-drive"),
    ("teeth-like-gods-shoeshine","Teeth Like God's Shoeshine","lonesome-crowded-west"),
    ("trailer-trash","Trailer Trash","lonesome-crowded-west"),
    ("out-of-gas","Out of Gas","lonesome-crowded-west"),
    ("jesus-was-a-cross-maker","Jesus Was a Cross Maker","lonesome-crowded-west"),
    ("styrofoam-boots","Styrofoam Boots","lonesome-crowded-west"),
    ("cowboy-dan","Cowboy Dan","lonesome-crowded-west"),
    ("3rd-planet","3rd Planet","moon-and-antarctica"),
    ("dark-center-of-the-universe","Dark Center of the Universe","moon-and-antarctica"),
    ("lives-mm","Lives","moon-and-antarctica"),
    ("gravity-rides-everything","Gravity Rides Everything","moon-and-antarctica"),
    ("tiny-cities-made-of-ashes","Tiny Cities Made of Ashes","moon-and-antarctica"),
    ("oh-what-a-world-mm","Oh What a World","moon-and-antarctica"),
    ("float-on","Float On","good-news-for-people-who-love-bad-news"),
    ("ocean-breathes-salty","Ocean Breathes Salty","good-news-for-people-who-love-bad-news"),
    ("the-view-mm","The View","good-news-for-people-who-love-bad-news"),
    ("satin-in-a-coffin","Satin in a Coffin","good-news-for-people-who-love-bad-news"),
    ("world-at-large","World at Large","good-news-for-people-who-love-bad-news"),
    ("dashboard-mm","Dashboard","good-news-for-people-who-love-bad-news"),
  ]:
  w(SONGS/f"{s}.md", song_md(t,"Modest Mouse","modest-mouse",alb,mm_cr+jg_prod))

# ── DEATH CAB ─────────────────────────────────────────────────────────────
dcfc_cr = [("ben-gibbard","Ben Gibbard","vocals/guitar"),
           ("chris-walla","Chris Walla","guitar/producer"),
           ("nick-harmer","Nick Harmer","bass"),
           ("jason-mcgerr","Jason McGerr","drums")]
dcfc_early = [("ben-gibbard","Ben Gibbard","vocals/guitar"),
              ("chris-walla","Chris Walla","guitar/producer"),
              ("nick-harmer","Nick Harmer","bass"),
              ("nathaniel-floyd","Nathaniel Floyd","drums")]
for s,t,alb,line in [
    ("bend-to-squares","Bend to Squares","something-about-airplanes","early"),
    ("president-of-what","President of What?","something-about-airplanes","early"),
    ("champagne-from-a-paper-cup","Champagne from a Paper Cup","something-about-airplanes","early"),
    ("your-bruise","Your Bruise","something-about-airplanes","early"),
    ("pictures-in-an-exhibition","Pictures in an Exhibition","something-about-airplanes","early"),
    ("title-track-dcfc","Title Track","we-have-the-facts","early"),
    ("the-employment-pages","The Employment Pages","we-have-the-facts","early"),
    ("for-what-reason","For What Reason","we-have-the-facts","early"),
    ("lowell-ma","Lowell, MA","we-have-the-facts","early"),
    ("company-calls","Company Calls","we-have-the-facts","early"),
    ("the-new-year","The New Year","transatlanticism","late"),
    ("lightness-dcfc","Lightness","transatlanticism","late"),
    ("title-and-registration","Title and Registration","transatlanticism","late"),
    ("expo-86","Expo '86","transatlanticism","late"),
    ("the-sound-of-settling","The Sound of Settling","transatlanticism","late"),
    ("tiny-vessels","Tiny Vessels","transatlanticism","late"),
    ("transatlanticism-song","Transatlanticism","transatlanticism","late"),
    ("death-of-an-interior-decorator","Death of an Interior Decorator","transatlanticism","late"),
    ("marching-bands-of-manhattan","Marching Bands of Manhattan","plans","late"),
    ("soul-meets-body","Soul Meets Body","plans","late"),
    ("summer-skin","Summer Skin","plans","late"),
    ("what-sarah-said","What Sarah Said","plans","late"),
    ("i-will-follow-you-into-the-dark","I Will Follow You into the Dark","plans","late"),
    ("brothers-on-a-hotel-bed","Brothers on a Hotel Bed","plans","late"),
  ]:
  cr = (dcfc_early if line=="early" else dcfc_cr)
  w(SONGS/f"{s}.md", song_md(t,"Death Cab for Cutie","death-cab-for-cutie",alb,cr))

# ── FLEET FOXES ───────────────────────────────────────────────────────────
ff_cr = [("robin-pecknold","Robin Pecknold","vocals/guitar"),
         ("skyler-skjelset","Skyler Skjelset","guitar"),
         ("casey-musgraves-ff","Casey Musgraves","keyboards"),
         ("christian-wargo","Christian Wargo","bass/vocals"),
         ("morgan-henderson","Morgan Henderson","multi-instrumentalist"),
         ("phil-ek","Phil Ek","producer")]
ff_cr2 = [("robin-pecknold","Robin Pecknold","vocals/guitar/producer"),
          ("skyler-skjelset","Skyler Skjelset","guitar"),
          ("casey-musgraves-ff","Casey Musgraves","keyboards"),
          ("christian-wargo","Christian Wargo","bass/vocals"),
          ("morgan-henderson","Morgan Henderson","multi-instrumentalist")]
for s,t,alb,line in [
    ("white-winter-hymnal","White Winter Hymnal","fleet-foxes-debut",1),
    ("ragged-wood","Ragged Wood","fleet-foxes-debut",1),
    ("tiger-mountain-peasant-song","Tiger Mountain Peasant Song","fleet-foxes-debut",1),
    ("meadowlarks","Meadowlarks","fleet-foxes-debut",1),
    ("blue-ridge-mountains","Blue Ridge Mountains","fleet-foxes-debut",1),
    ("he-doesnt-know-why","He Doesn't Know Why","fleet-foxes-debut",1),
    ("heard-them-stirring","Heard Them Stirring","fleet-foxes-debut",1),
    ("montezuma","Montezuma","helplessness-blues",2),
    ("bedouin-dress","Bedouin Dress","helplessness-blues",2),
    ("sim-sala-bim","Sim Sala Bim","helplessness-blues",2),
    ("battery-kinzie","Battery Kinzie","helplessness-blues",2),
    ("the-plains-bitter-dancer","The Plains / Bitter Dancer","helplessness-blues",2),
    ("helplessness-blues-song","Helplessness Blues","helplessness-blues",2),
    ("the-shrine-an-argument","The Shrine / An Argument","helplessness-blues",2),
  ]:
  w(SONGS/f"{s}.md", song_md(t,"Fleet Foxes","fleet-foxes",alb,(ff_cr if line==1 else ff_cr2)))

# ── SLEATER-KINNEY ────────────────────────────────────────────────────────
sk_cr = [("corin-tucker","Corin Tucker","vocals/guitar"),
         ("carrie-brownstein","Carrie Brownstein","guitar/vocals"),
         ("janet-weiss","Janet Weiss","drums"),
         ("john-goodmanson","John Goodmanson","producer")]
for s,t,alb in [
    ("call-the-doctor-song","Call the Doctor","call-the-doctor"),
    ("stay-where-you-are","Stay Where You Are","call-the-doctor"),
    ("i-wanna-be-your-joey-ramone","I Wanna Be Your Joey Ramone","call-the-doctor"),
    ("good-things-sk","Good Things","call-the-doctor"),
    ("the-day-i-went-away","The Day I Went Away","call-the-doctor"),
    ("dig-me-out-song","Dig Me Out","dig-me-out"),
    ("one-more-hour","One More Hour","dig-me-out"),
    ("turn-it-on-sk","Turn It On","dig-me-out"),
    ("heart-attack-sk","Heart Attack","dig-me-out"),
    ("words-and-guitar","Words and Guitar","dig-me-out"),
    ("its-enough","It's Enough","dig-me-out"),
    ("little-babies","Little Babies","dig-me-out"),
    ("ballad-of-a-ladyman","Ballad of a Ladyman","all-hands-on-the-bad-one"),
    ("youre-no-rock-n-roll-fun","You're No Rock N Roll Fun","all-hands-on-the-bad-one"),
    ("ironclad","Ironclad","all-hands-on-the-bad-one"),
    ("one-must-have","#1 Must Have","all-hands-on-the-bad-one"),
    ("leave-you-behind","Leave You Behind","all-hands-on-the-bad-one"),
  ]:
  w(SONGS/f"{s}.md", song_md(t,"Sleater-Kinney","sleater-kinney",alb,sk_cr))

# ── BIKINI KILL ───────────────────────────────────────────────────────────
bk_cr = [("kathleen-hanna","Kathleen Hanna","vocals"),
         ("tobi-vail","Tobi Vail","drums"),
         ("kathi-wilcox","Kathi Wilcox","bass"),
         ("billy-karren","Billy Karren","guitar")]
for s,t,alb in [
    ("rebel-girl","Rebel Girl","pussy-whipped"),
    ("liar-bk","Liar","pussy-whipped"),
    ("star-bellied-boy","Star Bellied Boy","pussy-whipped"),
    ("carnival-bk","Carnival","pussy-whipped"),
    ("magnet-bk","Magnet","pussy-whipped"),
    ("feels-blind","Feels Blind","pussy-whipped"),
    ("alien-she","Alien She","pussy-whipped"),
    ("statement-of-vindication","Statement of Vindication","reject-all-american"),
    ("rip-bk","R.I.P.","reject-all-american"),
    ("false-start","False Start","reject-all-american"),
    ("reject-all-american-song","Reject All American","reject-all-american"),
  ]:
  w(SONGS/f"{s}.md", song_md(t,"Bikini Kill","bikini-kill",alb,bk_cr))

# ── HEART ─────────────────────────────────────────────────────────────────
heart_cr_early = [("ann-wilson","Ann Wilson","vocals"),
                  ("nancy-wilson","Nancy Wilson","guitar/vocals"),
                  ("roger-fisher","Roger Fisher","guitar"),
                  ("steve-fossen","Steve Fossen","bass"),
                  ("michael-derosier","Michael DeRosier","drums"),
                  ("mike-flicker","Mike Flicker","producer")]
heart_cr_da = [("ann-wilson","Ann Wilson","vocals"),
               ("nancy-wilson","Nancy Wilson","guitar/vocals"),
               ("howard-leese","Howard Leese","guitar/keyboards"),
               ("mark-andes","Mark Andes","bass"),
               ("denny-carmassi","Denny Carmassi","drums"),
               ("ron-nevison","Ron Nevison","producer")]
for s,t in [("magic-man","Magic Man"),("crazy-on-you","Crazy on You"),
            ("dreamboat-annie-song","Dreamboat Annie"),("sing-child","Sing Child"),
            ("how-deep-it-goes","How Deep It Goes"),("lighthearted-flower","Lighthearted Flower")]:
  w(SONGS/f"{s}.md", song_md(t,"Heart","heart","dreamboat-annie",heart_cr_early))
for s,t in [("barracuda","Barracuda"),("love-alive","Love Alive"),
            ("sylvan-song","Sylvan Song"),("dream-of-the-archer","Dream of the Archer"),
            ("kick-it-out","Kick It Out"),("little-queen-song","Little Queen"),
            ("treat-me-well","Treat Me Well")]:
  w(SONGS/f"{s}.md", song_md(t,"Heart","heart","little-queen",heart_cr_early))
for s,t in [("who-will-you-run-to","Who Will You Run To"),("alone-heart","Alone"),
            ("theres-the-girl","There's the Girl"),("i-want-you-so-bad","I Want You So Bad"),
            ("wait-for-an-answer","Wait for an Answer"),("bad-animals-song","Bad Animals")]:
  w(SONGS/f"{s}.md", song_md(t,"Heart","heart","bad-animals",heart_cr_da))

# ── JIMI HENDRIX ──────────────────────────────────────────────────────────
jh_cr = [("jimi-hendrix-person","Jimi Hendrix","vocals/guitar"),
         ("noel-redding","Noel Redding","bass"),
         ("mitch-mitchell","Mitch Mitchell","drums"),
         ("chas-chandler","Chas Chandler","producer")]
jh_cr2 = [("jimi-hendrix-person","Jimi Hendrix","vocals/guitar"),
           ("noel-redding","Noel Redding","bass"),
           ("mitch-mitchell","Mitch Mitchell","drums")]
for s,t,alb,prod in [
    ("purple-haze","Purple Haze","are-you-experienced","with_prod"),
    ("manic-depression","Manic Depression","are-you-experienced","with_prod"),
    ("hey-joe","Hey Joe","are-you-experienced","with_prod"),
    ("love-or-confusion","Love or Confusion","are-you-experienced","with_prod"),
    ("may-this-be-love","May This Be Love","are-you-experienced","with_prod"),
    ("the-wind-cries-mary","The Wind Cries Mary","are-you-experienced","with_prod"),
    ("fire-jh","Fire","are-you-experienced","with_prod"),
    ("foxy-lady","Foxy Lady","are-you-experienced","with_prod"),
    ("are-you-experienced-song","Are You Experienced?","are-you-experienced","with_prod"),
    ("exp-jh","EXP","axis-bold-as-love","with_prod"),
    ("up-from-the-skies","Up from the Skies","axis-bold-as-love","with_prod"),
    ("spanish-castle-magic","Spanish Castle Magic","axis-bold-as-love","with_prod"),
    ("little-wing","Little Wing","axis-bold-as-love","with_prod"),
    ("if-6-was-9","If 6 Was 9","axis-bold-as-love","with_prod"),
    ("castles-made-of-sand","Castles Made of Sand","axis-bold-as-love","with_prod"),
    ("bold-as-love","Bold as Love","axis-bold-as-love","with_prod"),
    ("crosstown-traffic","Crosstown Traffic","electric-ladyland","no_prod"),
    ("voodoo-chile","Voodoo Chile","electric-ladyland","no_prod"),
    ("gypsy-eyes","Gypsy Eyes","electric-ladyland","no_prod"),
    ("burning-of-the-midnight-lamp","Burning of the Midnight Lamp","electric-ladyland","no_prod"),
    ("all-along-the-watchtower","All Along the Watchtower","electric-ladyland","no_prod"),
    ("voodoo-child-slight-return","Voodoo Child (Slight Return)","electric-ladyland","no_prod"),
    ("have-you-ever-been","Have You Ever Been (to Electric Ladyland)","electric-ladyland","no_prod"),
  ]:
  cr = jh_cr if prod=="with_prod" else jh_cr2
  w(SONGS/f"{s}.md", song_md(t,"Jimi Hendrix","jimi-hendrix",alb,cr))

# ── SMASHING PUMPKINS ─────────────────────────────────────────────────────
bv_prod = [("butch-vig","Butch Vig","producer")]
flood_prod = [("flood-producer","Flood","producer")]
sp_cr_gish = [("billy-corgan","Billy Corgan","vocals/guitar"),
              ("james-iha","James Iha","guitar"),
              ("darcy-wretzky","D'arcy Wretzky","bass"),
              ("jimmy-chamberlin","Jimmy Chamberlin","drums")]
for s,t,alb,prod in [
    ("i-am-one-sp","I Am One","gish","bv"),
    ("siva","Siva","gish","bv"),
    ("rhinoceros","Rhinoceros","gish","bv"),
    ("bury-me","Bury Me","gish","bv"),
    ("crush-sp","Crush","gish","bv"),
    ("suffer","Suffer","gish","bv"),
    ("snail-sp","Snail","gish","bv"),
    ("tristessa","Tristessa","gish","bv"),
    ("cherub-rock","Cherub Rock","siamese-dream","bv"),
    ("quiet-sp","Quiet","siamese-dream","bv"),
    ("today-sp","Today","siamese-dream","bv"),
    ("hummer","Hummer","siamese-dream","bv"),
    ("rocket-sp","Rocket","siamese-dream","bv"),
    ("disarm","Disarm","siamese-dream","bv"),
    ("soma","Soma","siamese-dream","bv"),
    ("geek-usa","Geek U.S.A.","siamese-dream","bv"),
    ("mayonaise","Mayonaise","siamese-dream","bv"),
    ("spaceboy-sp","Spaceboy","siamese-dream","bv"),
    ("silverfuck","Silverfuck","siamese-dream","bv"),
    ("luna-sp","Luna","siamese-dream","bv"),
    ("tonight-tonight","Tonight Tonight","mellon-collie","flood"),
    ("jellybelly","Jellybelly","mellon-collie","flood"),
    ("zero-sp","Zero","mellon-collie","flood"),
    ("bullet-with-butterfly-wings","Bullet with Butterfly Wings","mellon-collie","flood"),
    ("to-forgive","To Forgive","mellon-collie","flood"),
    ("nineteen-seventy-nine","1979","mellon-collie","flood"),
    ("tales-of-a-scorched-earth","Tales of a Scorched Earth","mellon-collie","flood"),
    ("bodies-sp","Bodies","mellon-collie","flood"),
    ("thirty-three","Thirty-Three","mellon-collie","flood"),
    ("to-sheila","To Sheila","adore","self"),
    ("ava-adore","Ava Adore","adore","self"),
    ("perfect-sp","Perfect","adore","self"),
    ("daphne-descends","Daphne Descends","adore","self"),
    ("once-upon-a-time-sp","Once Upon a Time","adore","self"),
    ("crestfallen","Crestfallen","adore","self"),
    ("appels-oranjes","Appels + Oranjes","adore","self"),
    ("tale-of-dusty-and-demon-king","The Tale of Dusty and Demon King","adore","self"),
  ]:
  prod_cr = bv_prod if prod=="bv" else (flood_prod if prod=="flood" else [("billy-corgan","Billy Corgan","producer")])
  w(SONGS/f"{s}.md", song_md(t,"Smashing Pumpkins","smashing-pumpkins",alb,sp_cr_gish+prod_cr))

# ── LIZ PHAIR ─────────────────────────────────────────────────────────────
bw_prod = [("brad-wood","Brad Wood","producer")]
lp_cr = [("liz-phair-person","Liz Phair","vocals/guitar")]
for s,t,alb in [
    ("six-foot-one","6'1\"","exile-in-guyville"),
    ("help-me-mary","Help Me Mary","exile-in-guyville"),
    ("glory-lp","Glory","exile-in-guyville"),
    ("dance-of-the-seven-veils","Dance of the Seven Veils","exile-in-guyville"),
    ("never-said","Never Said","exile-in-guyville"),
    ("soap-star-joe","Soap Star Joe","exile-in-guyville"),
    ("explain-it-to-me","Explain It to Me","exile-in-guyville"),
    ("fuck-and-run","Fuck and Run","exile-in-guyville"),
    ("divorce-song","Divorce Song","exile-in-guyville"),
    ("stratford-on-guy","Stratford-on-Guy","exile-in-guyville"),
    ("girls-girls-girls-lp","Girls! Girls! Girls!","exile-in-guyville"),
    ("canary-lp","Canary","exile-in-guyville"),
    ("chopsticks-lp","Chopsticks","whip-smart"),
    ("supernova","Supernova","whip-smart"),
    ("support-system","Support System","whip-smart"),
    ("cinco-de-mayo","Cinco de Mayo","whip-smart"),
    ("x-ray-man","X-Ray Man","whip-smart"),
    ("jealousy-lp","Jealousy","whip-smart"),
    ("main-street-saloon","Main Street Saloon","whip-smart"),
    ("headache-lp","Headache","whip-smart"),
    ("alice-springs","Alice Springs","whip-smart"),
  ]:
  w(SONGS/f"{s}.md", song_md(t,"Liz Phair","liz-phair",alb,lp_cr+bw_prod))

# ── WILCO ─────────────────────────────────────────────────────────────────
wilco_cr = [("jeff-tweedy","Jeff Tweedy","vocals/guitar"),
            ("john-stirratt","John Stirratt","bass"),
            ("ken-coomer","Ken Coomer","drums"),
            ("max-johnston","Max Johnston","multi-instrumentalist")]
wilco_bt = [("jeff-tweedy","Jeff Tweedy","vocals/guitar"),
            ("john-stirratt","John Stirratt","bass"),
            ("ken-coomer","Ken Coomer","drums"),
            ("bob-egan","Bob Egan","pedal steel/guitar")]
wilco_yhf = [("jeff-tweedy","Jeff Tweedy","vocals/guitar"),
             ("john-stirratt","John Stirratt","bass"),
             ("glenn-kotche","Glenn Kotche","drums"),
             ("leroy-bach","Leroy Bach","keyboards"),
             ("jim-orourke","Jim O'Rourke","producer")]
wilco_agib = [("jeff-tweedy","Jeff Tweedy","vocals/guitar/producer"),
              ("john-stirratt","John Stirratt","bass"),
              ("glenn-kotche","Glenn Kotche","drums"),
              ("nels-cline","Nels Cline","guitar"),
              ("mikael-jorgensen","Mikael Jorgensen","keyboards")]
for s,t,alb,line in [
    ("i-must-be-high","I Must Be High","am-wilco","am"),
    ("casino-queen","Casino Queen","am-wilco","am"),
    ("box-full-of-letters","Box Full of Letters","am-wilco","am"),
    ("shouldnt-be-ashamed","Shouldn't Be Ashamed","am-wilco","am"),
    ("pick-up-the-change","Pick Up the Change","am-wilco","am"),
    ("passenger-side","Passenger Side","am-wilco","am"),
    ("dash-7","Dash 7","am-wilco","am"),
    ("blue-eyed-soul","Blue Eyed Soul","am-wilco","am"),
    ("misunderstood-wilco","Misunderstood","being-there","bt"),
    ("far-far-away","Far Far Away","being-there","bt"),
    ("monday-wilco","Monday","being-there","bt"),
    ("forget-the-flowers","Forget the Flowers","being-there","bt"),
    ("red-eyed-and-blue","Red-Eyed and Blue","being-there","bt"),
    ("hotel-arizona","Hotel Arizona","being-there","bt"),
    ("sunken-treasure","Sunken Treasure","being-there","bt"),
    ("outtasite","Outtasite (Outtamind)","being-there","bt"),
    ("i-am-trying-to-break-your-heart","I Am Trying to Break Your Heart","yankee-hotel-foxtrot","yhf"),
    ("kamera","Kamera","yankee-hotel-foxtrot","yhf"),
    ("radio-cure","Radio Cure","yankee-hotel-foxtrot","yhf"),
    ("war-on-war","War on War","yankee-hotel-foxtrot","yhf"),
    ("jesus-etc","Jesus, etc.","yankee-hotel-foxtrot","yhf"),
    ("ashes-of-american-flags","Ashes of American Flags","yankee-hotel-foxtrot","yhf"),
    ("heavy-metal-drummer","Heavy Metal Drummer","yankee-hotel-foxtrot","yhf"),
    ("im-the-man-who-loves-you","I'm the Man Who Loves You","yankee-hotel-foxtrot","yhf"),
    ("pot-kettle-black","Pot Kettle Black","yankee-hotel-foxtrot","yhf"),
    ("poor-places","Poor Places","yankee-hotel-foxtrot","yhf"),
    ("reservations-wilco","Reservations","yankee-hotel-foxtrot","yhf"),
    ("at-least-thats-what-you-said","At Least That's What You Said","a-ghost-is-born","agib"),
    ("hell-is-chrome","Hell Is Chrome","a-ghost-is-born","agib"),
    ("spiders-kidsmoke","Spiders (Kidsmoke)","a-ghost-is-born","agib"),
    ("muzzle-of-bees","Muzzle of Bees","a-ghost-is-born","agib"),
    ("hummingbird-wilco","Hummingbird","a-ghost-is-born","agib"),
    ("handshake-drugs","Handshake Drugs","a-ghost-is-born","agib"),
    ("the-late-greats","The Late Greats","a-ghost-is-born","agib"),
  ]:
  cr = {"am":wilco_cr,"bt":wilco_bt,"yhf":wilco_yhf,"agib":wilco_agib}[line]
  w(SONGS/f"{s}.md", song_md(t,"Wilco","wilco",alb,cr))

# ── CHEAP TRICK ───────────────────────────────────────────────────────────
ct_cr = [("robin-zander","Robin Zander","vocals"),
         ("rick-nielsen","Rick Nielsen","guitar"),
         ("tom-petersson","Tom Petersson","bass"),
         ("bun-e-carlos","Bun E. Carlos","drums"),
         ("tom-werman","Tom Werman","producer")]
ct_live = [("robin-zander","Robin Zander","vocals"),
           ("rick-nielsen","Rick Nielsen","guitar"),
           ("tom-petersson","Tom Petersson","bass"),
           ("bun-e-carlos","Bun E. Carlos","drums"),
           ("jack-douglas-ct","Jack Douglas","producer")]
for s,t,alb,line in [
    ("elo-kiddies","ELO Kiddies","cheap-trick-debut","studio"),
    ("daddy-should-have-stayed","Daddy Should Have Stayed in High School","cheap-trick-debut","studio"),
    ("taxman-mr-thief","Taxman, Mr. Thief","cheap-trick-debut","studio"),
    ("cry-cry","Cry Cry","cheap-trick-debut","studio"),
    ("oh-candy","Oh Candy","cheap-trick-debut","studio"),
    ("hes-a-whore","He's a Whore","cheap-trick-debut","studio"),
    ("mandocello","Mandocello","cheap-trick-debut","studio"),
    ("ballad-of-tv-violence","The Ballad of TV Violence","cheap-trick-debut","studio"),
    ("lovin-money","Lovin' Money","cheap-trick-debut","studio"),
    ("hello-there","Hello There","in-color","studio"),
    ("big-eyes","Big Eyes","in-color","studio"),
    ("downed","Downed","in-color","studio"),
    ("i-want-you-to-want-me","I Want You to Want Me","in-color","studio"),
    ("youre-all-talk","You're All Talk","in-color","studio"),
    ("oh-caroline","Oh Caroline","in-color","studio"),
    ("clock-strikes-ten","Clock Strikes Ten","in-color","studio"),
    ("southern-girls","Southern Girls","in-color","studio"),
    ("come-on-come-on","Come On, Come On, Come On","in-color","studio"),
    ("hello-there-live","Hello There (Live)","at-budokan","live"),
    ("i-want-you-to-want-me-live","I Want You to Want Me (Live)","at-budokan","live"),
    ("surrender-ct","Surrender","at-budokan","live"),
    ("aint-that-a-shame","Ain't That a Shame","at-budokan","live"),
    ("goodnight-now","Goodnight Now","at-budokan","live"),
  ]:
  cr = ct_cr if line=="studio" else ct_live
  w(SONGS/f"{s}.md", song_md(t,"Cheap Trick","cheap-trick",alb,cr))

# ── THE JESUS LIZARD ──────────────────────────────────────────────────────
jl_cr = [("david-yow","David Yow","vocals"),
         ("duane-denison","Duane Denison","guitar"),
         ("david-wm-sims","David Wm. Sims","bass"),
         ("mac-mcneilly","Mac McNeilly","drums"),
         ("steve-albini","Steve Albini","producer")]
for s,t,alb in [
    ("then-comes-dudley","Then Comes Dudley","goat"),
    ("mouth-breather","Mouth Breather","goat"),
    ("nub","Nub","goat"),
    ("seasick-jl","Seasick","goat"),
    ("monkey-trick","Monkey Trick","goat"),
    ("karpis","Karpis","goat"),
    ("south-mouth","South Mouth","goat"),
    ("lady-shoes","Lady Shoes","goat"),
    ("rodeo-in-joliet","Rodeo in Joliet","goat"),
    ("boilermaker","Boilermaker","liar"),
    ("gladiator-jl","Gladiator","liar"),
    ("the-art-of-self-defense","The Art of Self-Defense","liar"),
    ("slave-ship","Slave Ship","liar"),
    ("puss","Puss","liar"),
    ("whirl","Whirl","liar"),
    ("rope-jl","Rope","liar"),
    ("perk","Perk","liar"),
  ]:
  w(SONGS/f"{s}.md", song_md(t,"The Jesus Lizard","the-jesus-lizard",alb,jl_cr))

# ── URGE OVERKILL ─────────────────────────────────────────────────────────
uo_cr = [("nash-kato","Nash Kato","vocals/guitar"),
         ("eddie-roeser","Eddie Roeser","guitar/vocals"),
         ("blackie-onassis","Blackie Onassis","drums"),
         ("butch-vig","Butch Vig","producer")]
for s,t in [("sister-havana","Sister Havana"),("tequila-sundae","Tequila Sundae"),
            ("positive-bleeding","Positive Bleeding"),("back-on-me","Back on Me"),
            ("woman-2-woman","Woman 2 Woman"),("cracker-uo","Cracker"),
            ("dropout","Dropout"),("the-stalker","The Stalker")]:
  w(SONGS/f"{s}.md", song_md(t,"Urge Overkill","urge-overkill","saturation",uo_cr))

# ── TORTOISE ──────────────────────────────────────────────────────────────
tort_cr = [("douglas-mccombs","Douglas McCombs","bass"),
           ("john-herndon","John Herndon","drums/percussion"),
           ("john-mcentire","John McEntire","drums/vibraphone/producer"),
           ("jeff-parker","Jeff Parker","guitar"),
           ("dan-bitney","Dan Bitney","percussion/keyboards")]
for s,t,alb in [
    ("djed","Djed","millions-now-living-will-never-die"),
    ("glass-museum","Glass Museum","millions-now-living-will-never-die"),
    ("a-survey","A Survey","millions-now-living-will-never-die"),
    ("the-taut-and-tame","The Taut and Tame","millions-now-living-will-never-die"),
    ("dear-grandma-and-grandpa","Dear Grandma and Grandpa","millions-now-living-will-never-die"),
    ("along-the-banks-of-rivers","Along the Banks of Rivers","millions-now-living-will-never-die"),
    ("tnt-song","TNT","tnt-tortoise"),
    ("in-sarah-mencins","In Sarah, Mencin's...","tnt-tortoise"),
    ("the-equator","The Equator","tnt-tortoise"),
    ("a-simple-way-to-go-faster","A Simple Way to Go Faster Than Light That Does Not Work","tnt-tortoise"),
    ("the-science-of-what","The Science of What","tnt-tortoise"),
    ("swung-from-the-gutters","Swung from the Gutters","tnt-tortoise"),
    ("ten-day-interval","Ten-Day Interval","tnt-tortoise"),
  ]:
  w(SONGS/f"{s}.md", song_md(t,"Tortoise","tortoise",alb,tort_cr))

# ── MUDDY WATERS ──────────────────────────────────────────────────────────
mw_cr_folk = [("muddy-waters-person","Muddy Waters","vocals/guitar"),
              ("buddy-guy-person","Buddy Guy","guitar"),
              ("willie-dixon","Willie Dixon","bass/producer")]
mw_cr_elec = [("muddy-waters-person","Muddy Waters","vocals/guitar"),
              ("willie-dixon","Willie Dixon","bass"),
              ("muddy-waters-person","Muddy Waters","producer")]
mw_cr_elec2 = [("muddy-waters-person","Muddy Waters","vocals/guitar"),
               ("willie-dixon","Willie Dixon","bass")]
for s,t in [("my-home-is-in-the-delta","My Home Is in the Delta"),
            ("long-distance-mw","Long Distance"),("my-captain","My Captain"),
            ("good-morning-little-schoolgirl","Good Morning Little Schoolgirl"),
            ("ive-got-my-mojo-working","I've Got My Mojo Working"),
            ("feel-like-going-home","Feel Like Going Home"),
            ("the-same-thing-mw","The Same Thing"),("walking-blues","Walking Blues")]:
  w(SONGS/f"{s}.md", song_md(t,"Muddy Waters","muddy-waters","folk-singer",mw_cr_folk))
for s,t in [("i-just-want-to-make-love-to-you","I Just Want to Make Love to You"),
            ("hoochie-coochie-man","Hoochie Coochie Man"),
            ("lets-spend-the-night-together-mw","Let's Spend the Night Together"),
            ("shes-all-right","She's All Right"),("im-a-man-mw","I'm a Man"),
            ("tom-cat","Tom Cat"),
            ("herbert-harpers-free-press-news","Herbert Harper's Free Press News")]:
  w(SONGS/f"{s}.md", song_md(t,"Muddy Waters","muddy-waters","electric-mud",mw_cr_elec2))

# ── BUDDY GUY ─────────────────────────────────────────────────────────────
bg_cr = [("buddy-guy-person","Buddy Guy","vocals/guitar"),
         ("john-porter-bg","John Porter","producer")]
for s,t in [("damn-right-ive-got-the-blues-song","Damn Right, I've Got the Blues"),
            ("where-is-the-next-one-coming-from","Where Is the Next One Coming From"),
            ("five-long-years","Five Long Years"),("pretty-baby-bg","Pretty Baby"),
            ("let-me-love-you-baby","Let Me Love You Baby"),
            ("too-broke-to-spend-the-night","Too Broke to Spend the Night"),
            ("early-in-the-morning","Early in the Morning")]:
  w(SONGS/f"{s}.md", song_md(t,"Buddy Guy","buddy-guy","damn-right-ive-got-the-blues",bg_cr))

# ── HOWLIN WOLF ───────────────────────────────────────────────────────────
hw_cr = [("howlin-wolf-person","Howlin' Wolf","vocals/guitar"),
         ("willie-dixon","Willie Dixon","bass/songwriter"),
         ("hubert-sumlin","Hubert Sumlin","guitar")]
for s,t,alb in [
    ("moanin-at-midnight","Moanin' at Midnight","moanin-in-the-moonshine"),
    ("how-many-more-years","How Many More Years","moanin-in-the-moonshine"),
    ("smokestack-lightning","Smokestack Lightning","moanin-in-the-moonshine"),
    ("baby-how-long","Baby How Long","moanin-in-the-moonshine"),
    ("no-place-to-go-hw","No Place to Go","moanin-in-the-moonshine"),
    ("all-night-boogie","All Night Boogie","moanin-in-the-moonshine"),
    ("evil-hw","Evil","moanin-in-the-moonshine"),
    ("im-the-wolf","I'm the Wolf","moanin-in-the-moonshine"),
    ("smokestack-lightning-ii","Smokestack Lightning (Alt. Version)","the-real-folk-blues"),
    ("back-door-man","Back Door Man","the-real-folk-blues"),
    ("wang-dang-doodle","Wang Dang Doodle","the-real-folk-blues"),
    ("the-red-rooster","The Red Rooster","the-real-folk-blues"),
    ("shake-for-me","Shake for Me","the-real-folk-blues"),
    ("howlin-for-my-darling","Howlin' for My Darling","the-real-folk-blues"),
    ("hidden-charms","Hidden Charms","the-real-folk-blues"),
    ("killing-floor","Killing Floor","the-real-folk-blues"),
  ]:
  w(SONGS/f"{s}.md", song_md(t,"Howlin' Wolf","howlin-wolf",alb,hw_cr))

# ── BIG BLACK ─────────────────────────────────────────────────────────────
bb_cr = [("steve-albini","Steve Albini","vocals/guitar/producer"),
         ("santiago-durango","Santiago Durango","guitar"),
         ("dave-riley","Dave Riley","bass")]
for s,t,alb in [
    ("jordan-minnesota","Jordan, Minnesota","atomizer"),
    ("passing-complexion","Passing Complexion","atomizer"),
    ("big-money-bb","Big Money","atomizer"),
    ("kerosene","Kerosene","atomizer"),
    ("bad-houses","Bad Houses","atomizer"),
    ("fists-of-love","Fists of Love","atomizer"),
    ("stinking-drunk","Stinking Drunk","atomizer"),
    ("cables-bb","Cables","atomizer"),
    ("strange-things-bb","Strange Things","atomizer"),
    ("power-of-independent-trucking","The Power of Independent Trucking","songs-about-fucking"),
    ("the-ugly-american","The Ugly American","songs-about-fucking"),
    ("bad-penny","Bad Penny","songs-about-fucking"),
    ("pavement-saw","Pavement Saw","songs-about-fucking"),
    ("tiny-bb","Tiny","songs-about-fucking"),
    ("kasimir-s-pulaski-day","Kasimir S. Pulaski Day","songs-about-fucking"),
    ("ergot","Ergot","songs-about-fucking"),
    ("precious-thing-bb","Precious Thing","songs-about-fucking"),
    ("colombian-necktie","Colombian Necktie","songs-about-fucking"),
    ("kitty-empire","Kitty Empire","songs-about-fucking"),
  ]:
  w(SONGS/f"{s}.md", song_md(t,"Big Black","big-black",alb,bb_cr))

# ── SHELLAC ───────────────────────────────────────────────────────────────
sh_cr = [("steve-albini","Steve Albini","vocals/guitar/producer"),
         ("bob-weston","Bob Weston","guitar"),
         ("todd-trainer","Todd Trainer","drums")]
for s,t,alb in [
    ("my-black-ass","My Black Ass","at-action-park"),
    ("pull-the-cup","Pull the Cup","at-action-park"),
    ("the-admiral","The Admiral","at-action-park"),
    ("crow-shellac","Crow","at-action-park"),
    ("trem-two","Trem Two","at-action-park"),
    ("dog-and-pony-show","Dog and Pony Show","at-action-park"),
    ("boches-dick","Boche's Dick","at-action-park"),
    ("a-minute-shellac","A Minute","at-action-park"),
    ("didnt-we-deserve-a-look","Didn't We Deserve a Look at You the Way You Really Are","terraform"),
    ("this-is-a-picture-shellac","This Is a Picture","terraform"),
    ("disgrace-shellac","Disgrace","terraform"),
    ("watch-song","Watch Song","terraform"),
    ("canada-shellac","Canada","terraform"),
    ("rush-job","Rush Job","terraform"),
    ("copper-shellac","Copper","terraform"),
  ]:
  w(SONGS/f"{s}.md", song_md(t,"Shellac","shellac",alb,sh_cr))

print(f"After songs: {_c} created, {_s} skipped")

# ══════════════════════════════════════════════════════════════ PEOPLE ════

def make_person(slug, title, born, nat, roles, bands, credits, bio, died=None):
    w(PEOPLE/f"{slug}.md", person_md(slug, title, born, nat, roles, bands, credits, bio, died))

# ── SOUNDGARDEN people ────────────────────────────────────────────────────
make_person("chris-cornell","Chris Cornell",1964,"American",
  ["vocalist","guitarist","songwriter"],
  [("soundgarden","Soundgarden","Vocalist, Guitarist"),
   ("temple-of-the-dog","Temple of the Dog","Vocalist, Guitarist"),
   ("audioslave","Audioslave","Vocalist")],
  [("song","black-hole-sun","Black Hole Sun","songwriter/vocalist","Soundgarden"),
   ("song","spoonman","Spoonman","songwriter/vocalist","Soundgarden"),
   ("song","outshined","Outshined","songwriter/vocalist","Soundgarden"),
   ("song","rusty-cage","Rusty Cage","songwriter/vocalist","Soundgarden"),
   ("song","say-hello-2-heaven","Say Hello 2 Heaven","songwriter/vocalist","Temple of the Dog"),
   ("song","hunger-strike","Hunger Strike","vocalist","Temple of the Dog"),
   ("album","superunknown","Superunknown","vocalist/guitarist","Soundgarden")],
  "Chris Cornell (1964–2017) was the founding vocalist and guitarist of Soundgarden, one of the most powerful voices in rock history. His four-octave tenor defined Seattle grunge. He also formed Temple of the Dog as a tribute to Andrew Wood, and later fronted Audioslave.",
  died=2017)

make_person("kim-thayil","Kim Thayil",1960,"American",
  ["guitarist","songwriter"],
  [("soundgarden","Soundgarden","Lead Guitarist")],
  [("song","black-hole-sun","Black Hole Sun","lead guitar","Soundgarden"),
   ("song","spoonman","Spoonman","lead guitar","Soundgarden"),
   ("album","superunknown","Superunknown","lead guitar","Soundgarden")],
  "Kim Thayil is the lead guitarist of Soundgarden, known for his unconventional tunings and distinctive heavy tone. Born in Park Forest, Illinois, he co-founded Soundgarden in Seattle in 1984.")

make_person("ben-shepherd","Ben Shepherd",1968,"American",
  ["bassist","vocalist","songwriter"],
  [("soundgarden","Soundgarden","Bassist (1990–2017)")],
  [("song","outshined","Outshined","bass","Soundgarden"),
   ("song","rusty-cage","Rusty Cage","bass","Soundgarden"),
   ("album","badmotorfinger","Badmotorfinger","bass","Soundgarden")],
  "Ben Shepherd joined Soundgarden as bassist in 1990, replacing Hiro Yamamoto. His melodic bass lines and occasional lead vocals added depth to the band's sound.")

make_person("hiro-yamamoto","Hiro Yamamoto",1961,"American",
  ["bassist"],
  [("soundgarden","Soundgarden","Bassist (1984–1990)")],
  [("song","flower-sg","Flower","bass","Soundgarden"),
   ("album","ultramega-ok","Ultramega OK","bass","Soundgarden")],
  "Hiro Yamamoto was a founding member and original bassist of Soundgarden, present on their early recordings including Ultramega OK and Louder Than Love before departing in 1990.")

make_person("matt-cameron","Matt Cameron",1962,"American",
  ["drummer","vocalist","songwriter"],
  [("soundgarden","Soundgarden","Drummer"),
   ("pearl-jam","Pearl Jam","Drummer (1998–present)"),
   ("temple-of-the-dog","Temple of the Dog","Drummer")],
  [("song","black-hole-sun","Black Hole Sun","drums","Soundgarden"),
   ("song","hunger-strike","Hunger Strike","drums","Temple of the Dog"),
   ("album","superunknown","Superunknown","drums","Soundgarden")],
  "Matt Cameron is one of rock's most celebrated drummers. He was the longtime drummer for Soundgarden and has been Pearl Jam's drummer since 1998. He also played on the Temple of the Dog tribute album.")

# ── ALICE IN CHAINS people ────────────────────────────────────────────────
make_person("layne-staley","Layne Staley",1967,"American",
  ["vocalist","songwriter"],
  [("alice-in-chains","Alice in Chains","Vocalist (1987–2002)")],
  [("song","man-in-the-box","Man in the Box","songwriter/vocalist","Alice in Chains"),
   ("song","rooster","Rooster","vocalist","Alice in Chains"),
   ("song","down-in-a-hole","Down in a Hole","vocalist","Alice in Chains"),
   ("album","dirt","Dirt","vocalist","Alice in Chains")],
  "Layne Staley (1967–2002) was the founding vocalist of Alice in Chains, whose haunting harmonies with Jerry Cantrell defined the Seattle grunge sound. His struggle with heroin addiction became central to the band's later work. He died of a drug overdose in 2002.",
  died=2002)

make_person("jerry-cantrell","Jerry Cantrell",1966,"American",
  ["guitarist","vocalist","songwriter"],
  [("alice-in-chains","Alice in Chains","Guitarist, Vocalist")],
  [("song","rooster","Rooster","songwriter/guitarist","Alice in Chains"),
   ("song","them-bones","Them Bones","songwriter/guitarist","Alice in Chains"),
   ("song","would","Would?","songwriter/guitarist","Alice in Chains"),
   ("album","dirt","Dirt","guitarist/vocalist","Alice in Chains")],
  "Jerry Cantrell is the co-founder, lead guitarist, and co-vocalist of Alice in Chains. His sludgy, down-tuned riffs and harmony vocals with Layne Staley are central to the band's identity. Rooster is his tribute to his Vietnam veteran father.")

make_person("sean-kinney","Sean Kinney",1966,"American",
  ["drummer"],
  [("alice-in-chains","Alice in Chains","Drummer")],
  [("album","dirt","Dirt","drums","Alice in Chains"),
   ("album","facelift","Facelift","drums","Alice in Chains")],
  "Sean Kinney is the drummer and a founding member of Alice in Chains, known for his powerful, groove-heavy style.")

make_person("mike-starr","Mike Starr",1966,"American",
  ["bassist"],
  [("alice-in-chains","Alice in Chains","Bassist (1987–1993)")],
  [("album","facelift","Facelift","bass","Alice in Chains"),
   ("album","dirt","Dirt","bass","Alice in Chains")],
  "Mike Starr (1966–2011) was the original bassist of Alice in Chains, featured on their first two major albums. He left the band in 1993 and passed away in 2011.",
  died=2011)

make_person("mike-inez","Mike Inez",1966,"American",
  ["bassist"],
  [("alice-in-chains","Alice in Chains","Bassist (1993–present)")],
  [("album","alice-in-chains-1995","Alice in Chains","bass","Alice in Chains"),
   ("album","black-gives-way-to-blue","Black Gives Way to Blue","bass","Alice in Chains")],
  "Mike Inez replaced Mike Starr as Alice in Chains' bassist in 1993, appearing on their self-titled album and all subsequent releases.")

make_person("william-duvall","William DuVall",1967,"American",
  ["vocalist","guitarist"],
  [("alice-in-chains","Alice in Chains","Vocalist (2006–present)")],
  [("song","check-my-brain","Check My Brain","vocalist","Alice in Chains"),
   ("album","black-gives-way-to-blue","Black Gives Way to Blue","vocalist","Alice in Chains")],
  "William DuVall joined Alice in Chains as co-vocalist in 2006 following the death of Layne Staley, helping to revitalize the band.")

# ── MUDHONEY people ───────────────────────────────────────────────────────
make_person("mark-arm","Mark Arm",1962,"American",
  ["vocalist","guitarist","songwriter"],
  [("mudhoney","Mudhoney","Vocalist, Guitarist"),
   ("green-river","Green River","Vocalist, Guitarist")],
  [("song","touch-me-im-sick","Touch Me I'm Sick","songwriter/vocalist","Mudhoney"),
   ("album","mudhoney-debut","Mudhoney","vocalist/guitarist","Mudhoney")],
  "Mark Arm is the co-founder and frontman of Mudhoney, one of grunge's most enduring bands. He previously sang for Green River alongside Stone Gossard and Jeff Ament.")

make_person("steve-turner","Steve Turner",1965,"American",
  ["guitarist"],
  [("mudhoney","Mudhoney","Guitarist"),
   ("green-river","Green River","Guitarist")],
  [("album","mudhoney-debut","Mudhoney","guitarist","Mudhoney")],
  "Steve Turner is Mudhoney's guitarist, known for his raw, feedback-heavy style influenced by garage rock and the Stooges.")

make_person("matt-lukin","Matt Lukin",1964,"American",
  ["bassist"],
  [("mudhoney","Mudhoney","Bassist"),
   ("melvins","Melvins","Bassist (early)")],
  [("album","mudhoney-debut","Mudhoney","bass","Mudhoney")],
  "Matt Lukin was Mudhoney's bassist throughout their peak years. He previously played bass for the Melvins.")

make_person("dan-peters","Dan Peters",1967,"American",
  ["drummer"],
  [("mudhoney","Mudhoney","Drummer")],
  [("album","mudhoney-debut","Mudhoney","drums","Mudhoney")],
  "Dan Peters is Mudhoney's drummer. He briefly filled in as Nirvana's drummer before Dave Grohl joined.")

# ── MOTHER LOVE BONE / TEMPLE OF THE DOG people ───────────────────────────
make_person("andrew-wood","Andrew Wood",1966,"American",
  ["vocalist","songwriter"],
  [("mother-love-bone","Mother Love Bone","Vocalist"),
   ("malfunkshun","Malfunkshun","Vocalist")],
  [("song","stardog-champion","Stardog Champion","songwriter/vocalist","Mother Love Bone"),
   ("song","crown-of-thorns","Crown of Thorns","songwriter/vocalist","Mother Love Bone"),
   ("album","apple","Apple","vocalist","Mother Love Bone")],
  "Andrew Wood (1966–1990) was the charismatic frontman of Mother Love Bone, whose glam-influenced vision helped shape Seattle's music scene. His death from a heroin overdose at age 24 inspired Chris Cornell to write the Temple of the Dog album.",
  died=1990)

make_person("bruce-fairweather","Bruce Fairweather",1966,"American",
  ["guitarist"],
  [("mother-love-bone","Mother Love Bone","Guitarist"),
   ("love-battery","Love Battery","Guitarist")],
  [("album","apple","Apple","guitarist","Mother Love Bone")],
  "Bruce Fairweather was a guitarist in Mother Love Bone, and later joined Love Battery.")

make_person("greg-gilmore","Greg Gilmore",1963,"American",
  ["drummer"],
  [("mother-love-bone","Mother Love Bone","Drummer"),
   ("ten-minute-warning","Ten Minute Warning","Drummer")],
  [("album","apple","Apple","drums","Mother Love Bone")],
  "Greg Gilmore was the drummer for Mother Love Bone.")

make_person("mike-mccready","Mike McCready",1966,"American",
  ["guitarist"],
  [("pearl-jam","Pearl Jam","Lead Guitarist"),
   ("temple-of-the-dog","Temple of the Dog","Lead Guitarist"),
   ("mad-season","Mad Season","Guitarist")],
  [("song","hunger-strike","Hunger Strike","lead guitar","Temple of the Dog"),
   ("album","temple-of-the-dog","Temple of the Dog","lead guitar","Temple of the Dog")],
  "Mike McCready is Pearl Jam's lead guitarist, celebrated for his blues-influenced improvisational style. He also played on the Temple of the Dog album.")

make_person("rick-parashar","Rick Parashar",1964,"Canadian",
  ["producer","engineer"],
  [("temple-of-the-dog","Temple of the Dog","Producer"),
   ("pearl-jam","Pearl Jam","Producer")],
  [("album","temple-of-the-dog","Temple of the Dog","producer","Temple of the Dog")],
  "Rick Parashar (1964–2014) was a Canadian record producer who produced the Temple of the Dog album and Pearl Jam's Ten. He was known for his warm, natural sound.",
  died=2014)

# ── SCREAMING TREES people ────────────────────────────────────────────────
make_person("gary-lee-conner","Gary Lee Conner",1962,"American",
  ["guitarist","songwriter"],
  [("screaming-trees","Screaming Trees","Lead Guitarist")],
  [("album","sweet-oblivion","Sweet Oblivion","guitarist","Screaming Trees"),
   ("album","dust-st","Dust","guitarist","Screaming Trees")],
  "Gary Lee Conner was the lead guitarist and co-founder of Screaming Trees, bringing a psychedelic, vintage rock influence to the band's sound.")

make_person("van-conner","Van Conner",1967,"American",
  ["bassist","vocalist"],
  [("screaming-trees","Screaming Trees","Bassist")],
  [("album","sweet-oblivion","Sweet Oblivion","bass","Screaming Trees"),
   ("album","dust-st","Dust","bass","Screaming Trees")],
  "Van Conner (1967–2023) was the bassist and co-founder of Screaming Trees, younger brother of guitarist Gary Lee Conner.",
  died=2023)

make_person("barrett-martin","Barrett Martin",1967,"American",
  ["drummer","multi-instrumentalist"],
  [("screaming-trees","Screaming Trees","Drummer (1991–1996)"),
   ("mad-season","Mad Season","Drummer")],
  [("album","sweet-oblivion","Sweet Oblivion","drums","Screaming Trees"),
   ("album","dust-st","Dust","drums","Screaming Trees")],
  "Barrett Martin joined Screaming Trees as drummer in 1991 after Mark Pickerel's departure. He also played with Mad Season.")

make_person("mark-pickerel","Mark Pickerel",1966,"American",
  ["drummer"],
  [("screaming-trees","Screaming Trees","Drummer (1985–1991)")],
  [("album","buzz-factory","Buzz Factory","drums","Screaming Trees")],
  "Mark Pickerel was the original drummer of Screaming Trees, present on their earliest recordings including Buzz Factory.")

make_person("don-fleming","Don Fleming",1954,"American",
  ["producer","guitarist","songwriter"],
  [],
  [("album","sweet-oblivion","Sweet Oblivion","producer","Screaming Trees")],
  "Don Fleming is an American record producer and musician who produced Screaming Trees' Sweet Oblivion.")

make_person("george-drakoulias","George Drakoulias",1961,"American",
  ["producer"],
  [],
  [("album","dust-st","Dust","producer","Screaming Trees")],
  "George Drakoulias is an American record producer known for working with Tom Petty, the Black Crowes, and Screaming Trees.")

# ── MELVINS people ────────────────────────────────────────────────────────
make_person("buzz-osborne","Buzz Osborne",1964,"American",
  ["vocalist","guitarist","songwriter"],
  [("melvins","Melvins","Vocalist, Guitarist")],
  [("song","hooch","Hooch","vocalist/guitarist/producer","Melvins"),
   ("song","night-goat","Night Goat","vocalist/guitarist/producer","Melvins"),
   ("album","houdini","Houdini","vocalist/guitarist/producer","Melvins")],
  "Buzz Osborne (King Buzzo) is the founder, vocalist, and guitarist of the Melvins. He was a key early influence on Kurt Cobain and co-produced Houdini with Kurt Cobain.")

make_person("dale-crover","Dale Crover",1972,"American",
  ["drummer","vocalist"],
  [("melvins","Melvins","Drummer"),
   ("nirvana","Nirvana","Drummer (early, live)")],
  [("album","houdini","Houdini","drums","Melvins"),
   ("album","gluey-porch-treatments","Gluey Porch Treatments","drums","Melvins")],
  "Dale Crover is the longtime drummer for the Melvins and one of the most influential drummers in alternative rock. He briefly played with Nirvana in their early days.")

make_person("lori-black","Lori Black",1961,"American",
  ["bassist"],
  [("melvins","Melvins","Bassist (1987–1989)")],
  [("album","gluey-porch-treatments","Gluey Porch Treatments","bass","Melvins")],
  "Lori Black (daughter of actress Shirley Temple) was the bassist on the Melvins' debut album Gluey Porch Treatments.")

# ── MODEST MOUSE people ───────────────────────────────────────────────────
make_person("isaac-brock","Isaac Brock",1975,"American",
  ["vocalist","guitarist","songwriter"],
  [("modest-mouse","Modest Mouse","Vocalist, Guitarist")],
  [("song","float-on","Float On","songwriter/vocalist","Modest Mouse"),
   ("song","3rd-planet","3rd Planet","songwriter/vocalist","Modest Mouse"),
   ("album","moon-and-antarctica","The Moon and Antarctica","vocalist/guitarist","Modest Mouse")],
  "Isaac Brock is the founder, vocalist, and primary songwriter of Modest Mouse. His raw, stream-of-consciousness lyrics and erratic guitar style define the band's sound.")

make_person("jeremiah-green","Jeremiah Green",1977,"American",
  ["drummer"],
  [("modest-mouse","Modest Mouse","Drummer")],
  [("album","moon-and-antarctica","The Moon and Antarctica","drums","Modest Mouse")],
  "Jeremiah Green is Modest Mouse's drummer, known for his propulsive, eclectic style. He has been with the band through most of their career.")

make_person("eric-judy","Eric Judy",1974,"American",
  ["bassist"],
  [("modest-mouse","Modest Mouse","Bassist (founding member)")],
  [("album","moon-and-antarctica","The Moon and Antarctica","bass","Modest Mouse")],
  "Eric Judy was a founding member and bassist of Modest Mouse, appearing on all their classic albums before departing in 2012.")

make_person("john-goodmanson","John Goodmanson",1968,"American",
  ["producer","engineer"],
  [],
  [("album","this-is-a-long-drive","This Is a Long Drive for Someone with Nothing to Think About","producer","Modest Mouse"),
   ("album","call-the-doctor","Call the Doctor","producer","Sleater-Kinney"),
   ("album","dig-me-out","Dig Me Out","producer","Sleater-Kinney")],
  "John Goodmanson is a Seattle-based record producer and engineer who worked extensively with Modest Mouse and Sleater-Kinney.")

# ── DEATH CAB FOR CUTIE people ────────────────────────────────────────────
make_person("ben-gibbard","Ben Gibbard",1976,"American",
  ["vocalist","guitarist","songwriter","pianist"],
  [("death-cab-for-cutie","Death Cab for Cutie","Vocalist, Guitarist"),
   ("the-postal-service","The Postal Service","Vocalist")],
  [("song","i-will-follow-you-into-the-dark","I Will Follow You into the Dark","songwriter/vocalist","Death Cab for Cutie"),
   ("song","transatlanticism-song","Transatlanticism","songwriter/vocalist","Death Cab for Cutie"),
   ("album","transatlanticism","Transatlanticism","vocalist/guitarist","Death Cab for Cutie")],
  "Ben Gibbard is the co-founder, vocalist, and primary songwriter of Death Cab for Cutie. His introspective, literary lyrics have made him one of indie rock's most beloved writers.")

make_person("chris-walla","Chris Walla",1975,"American",
  ["guitarist","producer","keyboardist"],
  [("death-cab-for-cutie","Death Cab for Cutie","Guitarist, Producer (1997–2014)")],
  [("album","transatlanticism","Transatlanticism","guitarist/producer","Death Cab for Cutie"),
   ("album","plans","Plans","guitarist/producer","Death Cab for Cutie")],
  "Chris Walla was Death Cab for Cutie's guitarist and in-house producer from their founding through 2014. His clean guitar tones and production aesthetic shaped the band's sound.")

make_person("nick-harmer","Nick Harmer",1974,"American",
  ["bassist"],
  [("death-cab-for-cutie","Death Cab for Cutie","Bassist")],
  [("album","transatlanticism","Transatlanticism","bass","Death Cab for Cutie")],
  "Nick Harmer is a founding member and bassist of Death Cab for Cutie.")

make_person("jason-mcgerr","Jason McGerr",1974,"American",
  ["drummer"],
  [("death-cab-for-cutie","Death Cab for Cutie","Drummer (2003–present)")],
  [("album","transatlanticism","Transatlanticism","drums","Death Cab for Cutie")],
  "Jason McGerr joined Death Cab for Cutie as drummer in 2003.")

make_person("nathaniel-floyd","Nathaniel Floyd",1975,"American",
  ["drummer"],
  [("death-cab-for-cutie","Death Cab for Cutie","Drummer (1997–2003)")],
  [("album","something-about-airplanes","Something About Airplanes","drums","Death Cab for Cutie")],
  "Nathaniel Floyd was Death Cab for Cutie's original drummer, present on their first two albums.")

# ── FLEET FOXES people ────────────────────────────────────────────────────
make_person("robin-pecknold","Robin Pecknold",1986,"American",
  ["vocalist","guitarist","songwriter"],
  [("fleet-foxes","Fleet Foxes","Vocalist, Guitarist")],
  [("song","white-winter-hymnal","White Winter Hymnal","songwriter/vocalist","Fleet Foxes"),
   ("song","helplessness-blues-song","Helplessness Blues","songwriter/vocalist","Fleet Foxes"),
   ("album","fleet-foxes-debut","Fleet Foxes","vocalist/guitarist","Fleet Foxes")],
  "Robin Pecknold is the founder and frontman of Fleet Foxes. His multi-part harmonies and poetic imagery have made the band one of indie folk's most celebrated acts.")

make_person("skyler-skjelset","Skyler Skjelset",1986,"American",
  ["guitarist"],
  [("fleet-foxes","Fleet Foxes","Guitarist")],
  [("album","fleet-foxes-debut","Fleet Foxes","guitarist","Fleet Foxes")],
  "Skyler Skjelset is a founding guitarist of Fleet Foxes and childhood friend of Robin Pecknold.")

make_person("casey-musgraves-ff","Casey Musgraves",1987,"American",
  ["keyboardist","multi-instrumentalist"],
  [("fleet-foxes","Fleet Foxes","Keyboardist")],
  [("album","fleet-foxes-debut","Fleet Foxes","keyboards","Fleet Foxes")],
  "Casey Musgraves is a keyboardist and multi-instrumentalist for Fleet Foxes. (Not to be confused with country singer Kacey Musgraves.)")

make_person("christian-wargo","Christian Wargo",1980,"American",
  ["bassist","vocalist","guitarist"],
  [("fleet-foxes","Fleet Foxes","Bassist, Vocalist")],
  [("album","fleet-foxes-debut","Fleet Foxes","bass/vocals","Fleet Foxes")],
  "Christian Wargo is the bassist and backing vocalist for Fleet Foxes.")

make_person("morgan-henderson","Morgan Henderson",1979,"American",
  ["multi-instrumentalist","bassist"],
  [("fleet-foxes","Fleet Foxes","Multi-instrumentalist")],
  [("album","helplessness-blues","Helplessness Blues","multi-instrumentalist","Fleet Foxes")],
  "Morgan Henderson joined Fleet Foxes as a multi-instrumentalist for their second album Helplessness Blues.")

make_person("phil-ek","Phil Ek",1968,"American",
  ["producer","engineer"],
  [],
  [("album","fleet-foxes-debut","Fleet Foxes","producer","Fleet Foxes")],
  "Phil Ek is a Seattle-based record producer known for working with Fleet Foxes, Built to Spill, and the Shins.")

# ── SLEATER-KINNEY people ─────────────────────────────────────────────────
make_person("corin-tucker","Corin Tucker",1972,"American",
  ["vocalist","guitarist","songwriter"],
  [("sleater-kinney","Sleater-Kinney","Vocalist, Guitarist")],
  [("song","dig-me-out-song","Dig Me Out","songwriter/vocalist","Sleater-Kinney"),
   ("album","dig-me-out","Dig Me Out","vocalist/guitarist","Sleater-Kinney")],
  "Corin Tucker is a co-founder of Sleater-Kinney and one of rock's most distinctive vocalists, known for her powerful vibrato and feminist lyricism.")

make_person("carrie-brownstein","Carrie Brownstein",1974,"American",
  ["guitarist","vocalist","songwriter","actress","writer"],
  [("sleater-kinney","Sleater-Kinney","Guitarist, Vocalist")],
  [("song","words-and-guitar","Words and Guitar","guitarist/vocalist","Sleater-Kinney"),
   ("album","dig-me-out","Dig Me Out","guitarist/vocalist","Sleater-Kinney")],
  "Carrie Brownstein is a co-founder of Sleater-Kinney and one of rock's most celebrated guitarists. She is also an actress and writer, best known for co-creating and starring in the TV series Portlandia.")

make_person("janet-weiss","Janet Weiss",1965,"American",
  ["drummer","vocalist"],
  [("sleater-kinney","Sleater-Kinney","Drummer"),
   ("quasi","Quasi","Drummer, Vocalist")],
  [("album","dig-me-out","Dig Me Out","drums","Sleater-Kinney"),
   ("album","call-the-doctor","Call the Doctor","drums","Sleater-Kinney")],
  "Janet Weiss is widely considered one of rock's finest drummers. She joined Sleater-Kinney in 1996 and transformed the band's sound.")

# ── BIKINI KILL people ────────────────────────────────────────────────────
make_person("kathleen-hanna","Kathleen Hanna",1968,"American",
  ["vocalist","songwriter","activist"],
  [("bikini-kill","Bikini Kill","Vocalist"),
   ("le-tigre","Le Tigre","Vocalist"),
   ("the-julie-ruin","The Julie Ruin","Vocalist")],
  [("song","rebel-girl","Rebel Girl","songwriter/vocalist","Bikini Kill"),
   ("album","pussy-whipped","Pussy Whipped","vocalist","Bikini Kill")],
  "Kathleen Hanna is the frontwoman of Bikini Kill and a central figure of the riot grrrl movement. Her confrontational performances and feminist manifestos defined punk's political wing in the 1990s.")

make_person("tobi-vail","Tobi Vail",1969,"American",
  ["drummer","vocalist","writer"],
  [("bikini-kill","Bikini Kill","Drummer"),
   ("the-casual-dots","The Casual Dots","Drummer")],
  [("album","pussy-whipped","Pussy Whipped","drums","Bikini Kill")],
  "Tobi Vail is the drummer and co-founder of Bikini Kill. She coined the term 'riot grrrl' and published the influential zine Jigsaw.")

make_person("kathi-wilcox","Kathi Wilcox",1972,"American",
  ["bassist"],
  [("bikini-kill","Bikini Kill","Bassist")],
  [("album","pussy-whipped","Pussy Whipped","bass","Bikini Kill")],
  "Kathi Wilcox is the bassist of Bikini Kill.")

make_person("billy-karren","Billy Karren",1971,"American",
  ["guitarist"],
  [("bikini-kill","Bikini Kill","Guitarist")],
  [("album","pussy-whipped","Pussy Whipped","guitar","Bikini Kill")],
  "Billy Karren is the guitarist of Bikini Kill.")

# ── HEART people ──────────────────────────────────────────────────────────
make_person("ann-wilson","Ann Wilson",1950,"American",
  ["vocalist","flautist","songwriter"],
  [("heart","Heart","Lead Vocalist")],
  [("song","barracuda","Barracuda","vocalist","Heart"),
   ("song","magic-man","Magic Man","vocalist","Heart"),
   ("song","alone-heart","Alone","vocalist","Heart"),
   ("album","little-queen","Little Queen","vocalist","Heart")],
  "Ann Wilson is the lead vocalist of Heart and one of rock's greatest singers, known for her powerful range and blues-influenced delivery.")

make_person("nancy-wilson","Nancy Wilson",1954,"American",
  ["guitarist","vocalist","songwriter"],
  [("heart","Heart","Guitarist, Vocalist")],
  [("song","barracuda","Barracuda","co-songwriter/guitarist","Heart"),
   ("song","crazy-on-you","Crazy on You","guitarist","Heart"),
   ("album","little-queen","Little Queen","guitarist","Heart")],
  "Nancy Wilson is Heart's guitarist and co-vocalist, co-writer of many of the band's classic songs including Barracuda and Crazy on You.")

make_person("mike-flicker","Mike Flicker",1948,"American",
  ["producer","engineer"],
  [],
  [("album","dreamboat-annie","Dreamboat Annie","producer","Heart"),
   ("album","little-queen","Little Queen","producer","Heart")],
  "Mike Flicker produced Heart's early albums Dreamboat Annie and Little Queen, helping establish their hard rock sound.")

make_person("ron-nevison","Ron Nevison",1946,"American",
  ["producer","engineer"],
  [],
  [("album","bad-animals","Bad Animals","producer","Heart")],
  "Ron Nevison is a veteran rock producer known for his work with Heart (Bad Animals), Led Zeppelin, and the Who.")

make_person("roger-fisher","Roger Fisher",1950,"American",
  ["guitarist"],
  [("heart","Heart","Lead Guitarist (1973–1979)")],
  [("album","dreamboat-annie","Dreamboat Annie","lead guitar","Heart"),
   ("album","little-queen","Little Queen","lead guitar","Heart")],
  "Roger Fisher was Heart's original lead guitarist, featured on Dreamboat Annie and Little Queen.")

make_person("howard-leese","Howard Leese",1951,"American",
  ["guitarist","keyboardist"],
  [("heart","Heart","Guitarist, Keyboardist (1975–1998)")],
  [("album","bad-animals","Bad Animals","guitar/keyboards","Heart")],
  "Howard Leese was Heart's guitarist and keyboardist from the mid-1970s through 1998.")

# ── JIMI HENDRIX people ───────────────────────────────────────────────────
make_person("jimi-hendrix-person","Jimi Hendrix",1942,"American",
  ["vocalist","guitarist","songwriter","bandleader"],
  [("jimi-hendrix","Jimi Hendrix","Vocalist, Guitarist")],
  [("song","purple-haze","Purple Haze","songwriter/vocalist/guitarist","Jimi Hendrix"),
   ("song","voodoo-child-slight-return","Voodoo Child (Slight Return)","songwriter/vocalist/guitarist","Jimi Hendrix"),
   ("song","little-wing","Little Wing","songwriter/guitarist","Jimi Hendrix"),
   ("album","are-you-experienced","Are You Experienced","vocalist/guitarist","Jimi Hendrix"),
   ("album","electric-ladyland","Electric Ladyland","vocalist/guitarist/producer","Jimi Hendrix")],
  "Jimi Hendrix (1942–1970) was born in Seattle and became widely regarded as the greatest electric guitarist who ever lived. His innovative use of feedback, distortion, and wah-wah pedal transformed rock guitar. He died at age 27.",
  died=1970)

make_person("noel-redding","Noel Redding",1945,"British",
  ["bassist","guitarist"],
  [("jimi-hendrix","Jimi Hendrix","Bassist (Jimi Hendrix Experience)")],
  [("album","are-you-experienced","Are You Experienced","bass","Jimi Hendrix"),
   ("album","axis-bold-as-love","Axis: Bold as Love","bass","Jimi Hendrix")],
  "Noel Redding (1945–2003) was the bassist of the Jimi Hendrix Experience.",
  died=2003)

make_person("mitch-mitchell","Mitch Mitchell",1947,"British",
  ["drummer"],
  [("jimi-hendrix","Jimi Hendrix","Drummer (Jimi Hendrix Experience)")],
  [("album","are-you-experienced","Are You Experienced","drums","Jimi Hendrix"),
   ("album","electric-ladyland","Electric Ladyland","drums","Jimi Hendrix")],
  "Mitch Mitchell (1947–2008) was the drummer of the Jimi Hendrix Experience, known for his jazz-influenced improvisational style.",
  died=2008)

make_person("chas-chandler","Chas Chandler",1938,"British",
  ["producer","bassist","manager"],
  [],
  [("album","are-you-experienced","Are You Experienced","producer","Jimi Hendrix"),
   ("album","axis-bold-as-love","Axis: Bold as Love","producer","Jimi Hendrix")],
  "Chas Chandler (1938–1996) was the former Animals bassist who discovered Jimi Hendrix in New York in 1966 and produced his first two albums.",
  died=1996)

# ── SMASHING PUMPKINS people ──────────────────────────────────────────────
make_person("billy-corgan","Billy Corgan",1967,"American",
  ["vocalist","guitarist","songwriter","producer"],
  [("smashing-pumpkins","Smashing Pumpkins","Vocalist, Guitarist")],
  [("song","tonight-tonight","Tonight Tonight","songwriter/vocalist","Smashing Pumpkins"),
   ("song","bullet-with-butterfly-wings","Bullet with Butterfly Wings","songwriter/vocalist","Smashing Pumpkins"),
   ("song","cherub-rock","Cherub Rock","songwriter/vocalist","Smashing Pumpkins"),
   ("album","siamese-dream","Siamese Dream","vocalist/guitarist","Smashing Pumpkins"),
   ("album","mellon-collie","Mellon Collie and the Infinite Sadness","vocalist/guitarist","Smashing Pumpkins")],
  "Billy Corgan is the founder, vocalist, and primary creative force behind the Smashing Pumpkins. He played nearly all instruments on Siamese Dream and wrote the band's most iconic songs.")

make_person("james-iha","James Iha",1968,"American",
  ["guitarist","vocalist","songwriter"],
  [("smashing-pumpkins","Smashing Pumpkins","Guitarist (1988–2000)")],
  [("album","siamese-dream","Siamese Dream","guitarist","Smashing Pumpkins"),
   ("album","mellon-collie","Mellon Collie and the Infinite Sadness","guitarist","Smashing Pumpkins")],
  "James Iha was the rhythm guitarist of the Smashing Pumpkins during their classic era.")

make_person("darcy-wretzky","D'arcy Wretzky",1968,"American",
  ["bassist","vocalist"],
  [("smashing-pumpkins","Smashing Pumpkins","Bassist (1988–1999)")],
  [("album","siamese-dream","Siamese Dream","bass","Smashing Pumpkins")],
  "D'arcy Wretzky was the bassist of the Smashing Pumpkins during their peak years.")

make_person("jimmy-chamberlin","Jimmy Chamberlin",1964,"American",
  ["drummer","keyboardist"],
  [("smashing-pumpkins","Smashing Pumpkins","Drummer"),
   ("jimmy-chamberlin-complex","Jimmy Chamberlin Complex","Drummer")],
  [("album","siamese-dream","Siamese Dream","drums","Smashing Pumpkins"),
   ("album","mellon-collie","Mellon Collie and the Infinite Sadness","drums","Smashing Pumpkins")],
  "Jimmy Chamberlin is widely considered one of rock's finest drummers. His jazz-influenced style on Siamese Dream and Mellon Collie was central to the Smashing Pumpkins' sound.")

make_person("michael-beinhorn","Michael Beinhorn",1958,"American",
  ["producer"],
  [],
  [("album","superunknown","Superunknown","producer","Soundgarden")],
  "Michael Beinhorn is an American record producer known for producing Soundgarden's Superunknown and albums by Red Hot Chili Peppers and Soul Asylum.")

make_person("flood-producer","Flood",1960,"British",
  ["producer","engineer"],
  [],
  [("album","mellon-collie","Mellon Collie and the Infinite Sadness","producer","Smashing Pumpkins")],
  "Flood (Mark Ellis) is a British record producer known for his work with Smashing Pumpkins, U2, Depeche Mode, and Nick Cave.")

make_person("adam-kasper","Adam Kasper",1965,"American",
  ["producer","engineer"],
  [],
  [("album","down-on-the-upside","Down on the Upside","producer","Soundgarden")],
  "Adam Kasper is a Seattle-based record producer and engineer who produced Soundgarden's Down on the Upside and has worked with Foo Fighters and Pearl Jam.")

# ── LIZ PHAIR people ─────────────────────────────────────────────────────
make_person("liz-phair-person","Liz Phair",1967,"American",
  ["vocalist","guitarist","songwriter"],
  [("liz-phair","Liz Phair","Vocalist, Guitarist")],
  [("song","fuck-and-run","Fuck and Run","songwriter/vocalist","Liz Phair"),
   ("song","divorce-song","Divorce Song","songwriter/vocalist","Liz Phair"),
   ("album","exile-in-guyville","Exile in Guyville","vocalist/guitarist","Liz Phair")],
  "Liz Phair is a Chicago-born singer-songwriter whose debut album Exile in Guyville is one of the most acclaimed indie rock albums of the 1990s. Her frank, conversational lyrics and lo-fi aesthetic were groundbreaking.")

make_person("brad-wood","Brad Wood",1963,"American",
  ["producer","drummer","engineer"],
  [],
  [("album","exile-in-guyville","Exile in Guyville","producer","Liz Phair"),
   ("album","whip-smart","Whip-Smart","producer","Liz Phair")],
  "Brad Wood is a Chicago-based record producer who collaborated with Liz Phair on her early albums.")

# ── WILCO people ──────────────────────────────────────────────────────────
make_person("jeff-tweedy","Jeff Tweedy",1967,"American",
  ["vocalist","guitarist","songwriter","producer"],
  [("wilco","Wilco","Vocalist, Guitarist"),
   ("uncle-tupelo","Uncle Tupelo","Vocalist, Guitarist"),
   ("golden-smog","Golden Smog","Vocalist")],
  [("song","jesus-etc","Jesus, etc.","songwriter/vocalist","Wilco"),
   ("song","i-am-trying-to-break-your-heart","I Am Trying to Break Your Heart","songwriter/vocalist","Wilco"),
   ("album","yankee-hotel-foxtrot","Yankee Hotel Foxtrot","vocalist/guitarist","Wilco")],
  "Jeff Tweedy is the co-founder, vocalist, and primary songwriter of Wilco. Starting from alt-country with Uncle Tupelo, he has led Wilco through one of rock's most adventurous creative evolutions.")

make_person("john-stirratt","John Stirratt",1967,"American",
  ["bassist","vocalist"],
  [("wilco","Wilco","Bassist"),
   ("the-autumn-defense","The Autumn Defense","Vocalist, Guitarist")],
  [("album","yankee-hotel-foxtrot","Yankee Hotel Foxtrot","bass","Wilco")],
  "John Stirratt is Wilco's bassist and the only member to appear on every Wilco album.")

make_person("glenn-kotche","Glenn Kotche",1970,"American",
  ["drummer","percussionist","composer"],
  [("wilco","Wilco","Drummer (2001–present)"),
   ("loose-fur","Loose Fur","Drummer")],
  [("album","yankee-hotel-foxtrot","Yankee Hotel Foxtrot","drums","Wilco"),
   ("album","a-ghost-is-born","A Ghost Is Born","drums","Wilco")],
  "Glenn Kotche is Wilco's drummer since 2001, known for his sophisticated polyrhythmic style that transformed the band's sound from alt-country to art rock.")

make_person("jim-orourke","Jim O'Rourke",1969,"American",
  ["producer","multi-instrumentalist","composer"],
  [("wilco","Wilco","Multi-instrumentalist (2000–2004)"),
   ("tortoise","Tortoise","Collaborator"),
   ("gastr-del-sol","Gastr del Sol","Musician")],
  [("album","yankee-hotel-foxtrot","Yankee Hotel Foxtrot","producer","Wilco")],
  "Jim O'Rourke is a Chicago-based multi-instrumentalist and producer who co-produced Wilco's Yankee Hotel Foxtrot. He has also collaborated with Sonic Youth, Stereolab, and Tortoise.")

make_person("nels-cline","Nels Cline",1956,"American",
  ["guitarist","composer"],
  [("wilco","Wilco","Guitarist (2004–present)"),
   ("nels-cline-singers","Nels Cline Singers","Guitarist")],
  [("album","a-ghost-is-born","A Ghost Is Born","guitar","Wilco")],
  "Nels Cline joined Wilco as lead guitarist in 2004, bringing an avant-garde jazz sensibility to the band's sound.")

# ── CHEAP TRICK people ────────────────────────────────────────────────────
make_person("robin-zander","Robin Zander",1953,"American",
  ["vocalist","guitarist"],
  [("cheap-trick","Cheap Trick","Lead Vocalist, Guitarist")],
  [("song","surrender-ct","Surrender","vocalist","Cheap Trick"),
   ("song","i-want-you-to-want-me","I Want You to Want Me","vocalist","Cheap Trick"),
   ("album","at-budokan","At Budokan","vocalist","Cheap Trick")],
  "Robin Zander is the lead vocalist of Cheap Trick, known for his powerful tenor and melodic pop sensibility.")

make_person("rick-nielsen","Rick Nielsen",1946,"American",
  ["guitarist","songwriter"],
  [("cheap-trick","Cheap Trick","Lead Guitarist, Songwriter")],
  [("song","surrender-ct","Surrender","songwriter/guitarist","Cheap Trick"),
   ("song","i-want-you-to-want-me","I Want You to Want Me","songwriter/guitarist","Cheap Trick"),
   ("album","at-budokan","At Budokan","guitarist","Cheap Trick")],
  "Rick Nielsen is Cheap Trick's lead guitarist and primary songwriter, known for his eccentric stage presence and collection of unusual guitars.")

make_person("tom-petersson","Tom Petersson",1950,"American",
  ["bassist","vocalist"],
  [("cheap-trick","Cheap Trick","Bassist")],
  [("album","at-budokan","At Budokan","bass","Cheap Trick")],
  "Tom Petersson is Cheap Trick's bassist, known for pioneering the 12-string bass guitar.")

make_person("bun-e-carlos","Bun E. Carlos",1951,"American",
  ["drummer"],
  [("cheap-trick","Cheap Trick","Drummer (1973–2010)")],
  [("album","at-budokan","At Budokan","drums","Cheap Trick")],
  "Bun E. Carlos was Cheap Trick's original drummer, known for his distinctive appearance and powerful playing.")

make_person("tom-werman","Tom Werman",1945,"American",
  ["producer"],
  [],
  [("album","cheap-trick-debut","Cheap Trick","producer","Cheap Trick"),
   ("album","in-color","In Color","producer","Cheap Trick")],
  "Tom Werman produced Cheap Trick's early studio albums, helping craft their commercial power pop sound.")

make_person("jack-douglas-ct","Jack Douglas",1942,"American",
  ["producer","engineer"],
  [],
  [("album","at-budokan","At Budokan","producer","Cheap Trick")],
  "Jack Douglas is a veteran rock producer who produced Cheap Trick's landmark live album At Budokan. He also produced Aerosmith and John Lennon.")

# ── THE JESUS LIZARD people ────────────────────────────────────────────────
make_person("david-yow","David Yow",1960,"American",
  ["vocalist"],
  [("the-jesus-lizard","The Jesus Lizard","Vocalist"),
   ("scratch-acid","Scratch Acid","Vocalist")],
  [("song","mouth-breather","Mouth Breather","vocalist","The Jesus Lizard"),
   ("album","goat","Goat","vocalist","The Jesus Lizard")],
  "David Yow is the vocalist of the Jesus Lizard, known for his unhinged stage presence and confrontational vocal style. He previously fronted Scratch Acid.")

make_person("duane-denison","Duane Denison",1959,"American",
  ["guitarist"],
  [("the-jesus-lizard","The Jesus Lizard","Guitarist"),
   ("tomahawk","Tomahawk","Guitarist")],
  [("album","goat","Goat","guitarist","The Jesus Lizard"),
   ("album","liar","Liar","guitarist","The Jesus Lizard")],
  "Duane Denison is the guitarist of the Jesus Lizard, known for his angular, mathematical riff writing.")

make_person("david-wm-sims","David Wm. Sims",1963,"American",
  ["bassist"],
  [("the-jesus-lizard","The Jesus Lizard","Bassist"),
   ("scratch-acid","Scratch Acid","Bassist")],
  [("album","goat","Goat","bass","The Jesus Lizard")],
  "David Wm. Sims is the bassist of the Jesus Lizard, previously a member of Scratch Acid.")

make_person("mac-mcneilly","Mac McNeilly",1967,"American",
  ["drummer"],
  [("the-jesus-lizard","The Jesus Lizard","Drummer (1989–1999)")],
  [("album","goat","Goat","drums","The Jesus Lizard"),
   ("album","liar","Liar","drums","The Jesus Lizard")],
  "Mac McNeilly was the Jesus Lizard's drummer during their peak years, known for his thunderous, unwavering groove.")

# ── URGE OVERKILL people ──────────────────────────────────────────────────
make_person("nash-kato","Nash Kato",1965,"American",
  ["vocalist","guitarist"],
  [("urge-overkill","Urge Overkill","Vocalist, Lead Guitarist")],
  [("song","sister-havana","Sister Havana","vocalist/guitarist","Urge Overkill"),
   ("album","saturation","Saturation","vocalist/guitarist","Urge Overkill")],
  "Nash Kato is the co-vocalist and lead guitarist of Urge Overkill.")

make_person("eddie-roeser","Eddie Roeser",1964,"American",
  ["guitarist","vocalist"],
  [("urge-overkill","Urge Overkill","Guitarist, Vocalist")],
  [("album","saturation","Saturation","guitar/vocals","Urge Overkill")],
  "Eddie Roeser is the guitarist and co-vocalist of Urge Overkill.")

make_person("blackie-onassis","Blackie Onassis",1967,"American",
  ["drummer"],
  [("urge-overkill","Urge Overkill","Drummer")],
  [("album","saturation","Saturation","drums","Urge Overkill")],
  "Blackie Onassis is the drummer for Urge Overkill.")

# ── TORTOISE people ───────────────────────────────────────────────────────
make_person("douglas-mccombs","Douglas McCombs",1965,"American",
  ["bassist","guitarist"],
  [("tortoise","Tortoise","Bassist"),
   ("pullman","Pullman","Guitarist"),
   ("eleventh-dream-day","Eleventh Dream Day","Bassist")],
  [("album","millions-now-living-will-never-die","Millions Now Living Will Never Die","bass","Tortoise"),
   ("album","tnt-tortoise","TNT","bass","Tortoise")],
  "Douglas McCombs is the bassist and co-founder of Tortoise, also known for his work with Pullman and Eleventh Dream Day.")

make_person("john-herndon","John Herndon",1968,"American",
  ["drummer","percussionist"],
  [("tortoise","Tortoise","Drummer, Percussionist")],
  [("album","millions-now-living-will-never-die","Millions Now Living Will Never Die","drums","Tortoise")],
  "John Herndon is one of Tortoise's two drummers, contributing to the band's layered polyrhythmic sound.")

make_person("john-mcentire","John McEntire",1966,"American",
  ["drummer","producer","sound engineer","keyboardist"],
  [("tortoise","Tortoise","Drummer, Producer"),
   ("the-sea-and-cake","The Sea and Cake","Drummer")],
  [("album","millions-now-living-will-never-die","Millions Now Living Will Never Die","drums/producer","Tortoise"),
   ("album","tnt-tortoise","TNT","drums/producer","Tortoise")],
  "John McEntire is Tortoise's co-drummer, producer, and engineer. He runs Soma Electronic Music Studios in Chicago and has worked with Stereolab, Yo La Tengo, and many others.")

make_person("jeff-parker","Jeff Parker",1961,"American",
  ["guitarist","composer"],
  [("tortoise","Tortoise","Guitarist"),
   ("isotope-217","Isotope 217","Guitarist")],
  [("album","tnt-tortoise","TNT","guitar","Tortoise")],
  "Jeff Parker is Tortoise's guitarist, a jazz-trained musician who brings a sophisticated harmonic palette to the band's post-rock sound.")

make_person("dan-bitney","Dan Bitney",1966,"American",
  ["percussionist","keyboardist","multi-instrumentalist"],
  [("tortoise","Tortoise","Percussionist, Keyboards")],
  [("album","millions-now-living-will-never-die","Millions Now Living Will Never Die","percussion/keyboards","Tortoise")],
  "Dan Bitney is Tortoise's percussionist and keyboardist, adding layers of texture to the band's densely arranged sound.")

# ── MUDDY WATERS / BUDDY GUY / HOWLIN WOLF people ────────────────────────
make_person("muddy-waters-person","Muddy Waters",1913,"American",
  ["vocalist","guitarist","songwriter","bandleader"],
  [("muddy-waters","Muddy Waters","Vocalist, Guitarist")],
  [("song","hoochie-coochie-man","Hoochie Coochie Man","vocalist/guitarist","Muddy Waters"),
   ("song","ive-got-my-mojo-working","I've Got My Mojo Working","vocalist/guitarist","Muddy Waters"),
   ("album","folk-singer","Folk Singer","vocalist/guitarist","Muddy Waters"),
   ("album","electric-mud","Electric Mud","vocalist/guitarist","Muddy Waters")],
  "Muddy Waters (1913–1983) was the father of modern Chicago blues. Born McKinley Morganfield in Mississippi, he moved to Chicago and electrified the Delta blues, influencing the Rolling Stones, Led Zeppelin, and virtually every rock musician who followed.",
  died=1983)

make_person("buddy-guy-person","Buddy Guy",1936,"American",
  ["vocalist","guitarist","songwriter"],
  [("buddy-guy","Buddy Guy","Vocalist, Guitarist")],
  [("song","damn-right-ive-got-the-blues-song","Damn Right, I've Got the Blues","vocalist/guitarist","Buddy Guy"),
   ("album","damn-right-ive-got-the-blues","Damn Right, I've Got the Blues","vocalist/guitarist","Buddy Guy"),
   ("album","folk-singer","Folk Singer","guitarist","Muddy Waters")],
  "Buddy Guy is a legendary Chicago blues guitarist and vocalist, inducted into the Rock and Roll Hall of Fame in 2005. His flamboyant, aggressive style influenced Jimi Hendrix, Eric Clapton, and Stevie Ray Vaughan.")

make_person("howlin-wolf-person","Howlin' Wolf",1910,"American",
  ["vocalist","guitarist","harmonica","songwriter"],
  [("howlin-wolf","Howlin' Wolf","Vocalist, Guitarist")],
  [("song","smokestack-lightning","Smokestack Lightning","songwriter/vocalist","Howlin' Wolf"),
   ("song","back-door-man","Back Door Man","vocalist","Howlin' Wolf"),
   ("song","killing-floor","Killing Floor","songwriter/vocalist","Howlin' Wolf"),
   ("album","moanin-in-the-moonshine","Moanin' in the Moonshine","vocalist/guitarist","Howlin' Wolf"),
   ("album","the-real-folk-blues","The Real Folk Blues","vocalist/guitarist","Howlin' Wolf")],
  "Howlin' Wolf (Chester Arthur Burnett, 1910–1976) was one of the most important figures in Chicago blues. His enormous voice and magnetic stage presence made songs like Smokestack Lightning and Back Door Man enduring classics.",
  died=1976)

make_person("willie-dixon","Willie Dixon",1915,"American",
  ["bassist","songwriter","producer","arranger"],
  [],
  [("song","hoochie-coochie-man","Hoochie Coochie Man","songwriter/bass","Muddy Waters"),
   ("song","wang-dang-doodle","Wang Dang Doodle","songwriter","Howlin' Wolf"),
   ("song","back-door-man","Back Door Man","songwriter","Howlin' Wolf"),
   ("song","the-red-rooster","The Red Rooster","songwriter","Howlin' Wolf"),
   ("album","folk-singer","Folk Singer","bass/producer","Muddy Waters"),
   ("album","the-real-folk-blues","The Real Folk Blues","bass/producer","Howlin' Wolf")],
  "Willie Dixon (1915–1992) was the most prolific songwriter of the Chicago blues era, writing classics for Muddy Waters, Howlin' Wolf, Koko Taylor, and many others. He was also the house bassist and producer at Chess Records.",
  died=1992)

make_person("hubert-sumlin","Hubert Sumlin",1931,"American",
  ["guitarist"],
  [("howlin-wolf","Howlin' Wolf","Lead Guitarist")],
  [("song","smokestack-lightning","Smokestack Lightning","lead guitar","Howlin' Wolf"),
   ("song","killing-floor","Killing Floor","lead guitar","Howlin' Wolf"),
   ("album","moanin-in-the-moonshine","Moanin' in the Moonshine","lead guitar","Howlin' Wolf")],
  "Hubert Sumlin (1931–2011) was Howlin' Wolf's guitarist, whose distinctive sparse, angular style influenced generations of rock players including Keith Richards and Eric Clapton.",
  died=2011)

make_person("john-porter-bg","John Porter",1947,"British",
  ["producer","guitarist"],
  [],
  [("album","damn-right-ive-got-the-blues","Damn Right, I've Got the Blues","producer","Buddy Guy")],
  "John Porter is a British record producer and guitarist who produced Buddy Guy's Grammy-winning album Damn Right, I've Got the Blues.")

# ── BIG BLACK / SHELLAC people ────────────────────────────────────────────
make_person("santiago-durango","Santiago Durango",1962,"American",
  ["guitarist"],
  [("big-black","Big Black","Guitarist"),
   ("naked-raygun","Naked Raygun","Guitarist")],
  [("album","atomizer","Atomizer","guitarist","Big Black"),
   ("album","songs-about-fucking","Songs About Fucking","guitarist","Big Black")],
  "Santiago Durango was the guitarist of Big Black, having previously played with Chicago punk band Naked Raygun.")

make_person("dave-riley","Dave Riley",1953,"American",
  ["bassist"],
  [("big-black","Big Black","Bassist")],
  [("album","atomizer","Atomizer","bass","Big Black"),
   ("album","songs-about-fucking","Songs About Fucking","bass","Big Black")],
  "Dave Riley was the bassist of Big Black, joining for their Atomizer album.")

make_person("bob-weston","Bob Weston",1967,"American",
  ["guitarist","engineer"],
  [("shellac","Shellac","Guitarist"),
   ("mclusky","McLusky","Collaborator")],
  [("album","at-action-park","At Action Park","guitarist","Shellac"),
   ("album","terraform","Terraform","guitarist","Shellac")],
  "Bob Weston is the guitarist of Shellac and a recording engineer at Steve Albini's Electrical Audio studio in Chicago.")

make_person("todd-trainer","Todd Trainer",1964,"American",
  ["drummer"],
  [("shellac","Shellac","Drummer"),
   ("brick-layer-cake","Brick Layer Cake","Drummer")],
  [("album","at-action-park","At Action Park","drums","Shellac"),
   ("album","terraform","Terraform","drums","Shellac")],
  "Todd Trainer is Shellac's drummer, known for his powerful, minimalist approach.")

make_person("dave-jerden","Dave Jerden",1950,"American",
  ["producer","engineer"],
  [],
  [("album","facelift","Facelift","producer","Alice in Chains"),
   ("album","dirt","Dirt","producer","Alice in Chains"),
   ("album","alice-in-chains-1995","Alice in Chains","producer","Alice in Chains")],
  "Dave Jerden is the producer of all three of Alice in Chains' studio albums during Layne Staley's tenure. He helped define the band's heavy, down-tuned sound.")

make_person("toby-wright","Toby Wright",1958,"American",
  ["producer","engineer"],
  [],
  [("album","alice-in-chains-1995","Alice in Chains","producer","Alice in Chains")],
  "Toby Wright is a record producer and engineer who produced Alice in Chains' self-titled album.")

make_person("terry-date","Terry Date",1957,"American",
  ["producer","engineer"],
  [],
  [("album","louder-than-love","Louder Than Love","producer","Soundgarden"),
   ("album","badmotorfinger","Badmotorfinger","producer","Soundgarden"),
   ("album","apple","Apple","producer","Mother Love Bone")],
  "Terry Date is a Seattle-based producer who worked with Soundgarden on Louder Than Love and Badmotorfinger, and produced Mother Love Bone's Apple.")

make_person("nick-raskulinecz","Nick Raskulinecz",1971,"American",
  ["producer"],
  [],
  [("album","black-gives-way-to-blue","Black Gives Way to Blue","producer","Alice in Chains")],
  "Nick Raskulinecz is a Nashville-based producer who produced Alice in Chains' reunion album Black Gives Way to Blue.")

make_person("toshi-kasai","Toshi Kasai",1970,"Japanese-American",
  ["producer","engineer"],
  [],
  [("album","houdini","Houdini","engineer","Melvins")],
  "Toshi Kasai is a Los Angeles-based producer and engineer who has worked with Melvins and other heavy rock acts.")

make_person("conrad-uno","Conrad Uno",1954,"American",
  ["producer","engineer"],
  [],
  [("album","every-good-boy-deserves-fudge","Every Good Boy Deserves Fudge","producer","Mudhoney")],
  "Conrad Uno is a Seattle-based producer and engineer who ran Egg Studios, recording many Pacific Northwest indie acts including Mudhoney.")

print(f"After people: {_c} created, {_s} skipped")

# ══════════════════════════════════════════════════════ UPDATE EXISTING PEOPLE ════
import re, yaml as _yaml
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

def read_frontmatter(path):
    """Read file, split frontmatter from body. Returns (dict, body_str)."""
    txt = Path(path).read_text(encoding="utf-8-sig")
    # split on --- delimiters
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', txt, re.DOTALL)
    if not m:
        return {}, txt
    fm_str, body = m.group(1), m.group(2)
    # parse manually since yaml may not be available
    return fm_str, body

def update_person_file(slug, new_bands=None, new_credits=None):
    """Add bands/credits to an existing person file, deduplicating by slug/key."""
    path = PEOPLE / f"{slug}.md"
    if not path.exists():
        print(f"  MISSING: {slug}.md")
        return
    txt = path.read_text(encoding="utf-8-sig")
    # We'll do string-level append into the YAML lists
    # Strategy: find the bands: or credits: block and append if not present

    new_bands = new_bands or []
    new_credits = new_credits or []

    for bs, bn, br in new_bands:
        if f'slug: "{bs}"' not in txt:
            # find bands: block and append
            if 'bands:' in txt:
                # insert after last band entry (before next top-level key or ---)
                # Simple approach: find 'bands:' and append just before next non-indented line
                txt = re.sub(
                    r'(bands:.*?)(\n(?:credits:|draft:|---|\Z))',
                    lambda m2: m2.group(1) + f'\n  - slug: "{bs}"\n    name: "{bn}"\n    role: "{br}"' + m2.group(2),
                    txt, count=1, flags=re.DOTALL)
            else:
                # insert bands: block before credits: or draft:
                txt = re.sub(
                    r'(\n)(credits:|draft:)',
                    f'\nbands:\n  - slug: "{bs}"\n    name: "{bn}"\n    role: "{br}"\n' + r'\2',
                    txt, count=1)

    for ctype, cslug, ctitle, crole, cartist in new_credits:
        key = "song_slug" if ctype == "song" else "album_slug"
        if f'{key}: "{cslug}"' not in txt:
            if 'credits:' in txt:
                txt = re.sub(
                    r'(credits:.*?)(\ndraft:|\Z)',
                    lambda m2: m2.group(1) + f'\n  - {key}: "{cslug}"\n    title: "{ctitle}"\n    role: "{crole}"\n    artist: "{cartist}"' + m2.group(2),
                    txt, count=1, flags=re.DOTALL)
            else:
                txt = re.sub(
                    r'(\n)(draft:)',
                    f'\ncredits:\n  - {key}: "{cslug}"\n    title: "{ctitle}"\n    role: "{crole}"\n    artist: "{cartist}"\n' + r'\2',
                    txt, count=1)

    path.write_text(txt, encoding="utf-8")
    print(f"  Updated {slug}.md")

# ── jack-endino ───────────────────────────────────────────────────────────
update_person_file("jack-endino",
  new_bands=[],
  new_credits=[
    ("album","ultramega-ok","Ultramega OK","producer","Soundgarden"),
    ("album","louder-than-love","Louder Than Love","producer","Soundgarden"),
    ("album","mudhoney-debut","Mudhoney","producer","Mudhoney"),
    ("album","gluey-porch-treatments","Gluey Porch Treatments","producer","Melvins"),
    ("album","buzz-factory","Buzz Factory","producer","Screaming Trees"),
    ("song","flower-sg","Flower","producer","Soundgarden"),
    ("song","touch-me-im-sick","Touch Me I'm Sick","producer","Mudhoney"),
    ("song","leetle-lulu","Leetle Lulu","producer","Melvins"),
  ])

# ── mark-lanegan ──────────────────────────────────────────────────────────
update_person_file("mark-lanegan",
  new_bands=[
    ("screaming-trees","Screaming Trees","Vocalist (1985–1996)"),
  ],
  new_credits=[
    ("album","sweet-oblivion","Sweet Oblivion","vocalist","Screaming Trees"),
    ("album","dust-st","Dust","vocalist","Screaming Trees"),
    ("song","nearly-lost-you","Nearly Lost You","songwriter/vocalist","Screaming Trees"),
    ("song","shadow-of-the-season","Shadow of the Season","vocalist","Screaming Trees"),
    ("song","halo-of-ashes","Halo of Ashes","vocalist","Screaming Trees"),
  ])

# ── steve-albini ──────────────────────────────────────────────────────────
update_person_file("steve-albini",
  new_bands=[
    ("big-black","Big Black","Vocalist, Guitarist, Producer"),
    ("shellac","Shellac","Vocalist, Guitarist, Producer"),
  ],
  new_credits=[
    ("album","atomizer","Atomizer","vocalist/guitarist/producer","Big Black"),
    ("album","songs-about-fucking","Songs About Fucking","vocalist/guitarist/producer","Big Black"),
    ("album","at-action-park","At Action Park","vocalist/guitarist/producer","Shellac"),
    ("album","terraform","Terraform","vocalist/guitarist/producer","Shellac"),
    ("album","goat","Goat","producer","The Jesus Lizard"),
    ("album","liar","Liar","producer","The Jesus Lizard"),
    ("song","kerosene","Kerosene","songwriter/vocalist","Big Black"),
    ("song","my-black-ass","My Black Ass","vocalist/guitarist","Shellac"),
    ("song","mouth-breather","Mouth Breather","producer","The Jesus Lizard"),
  ])

# ── butch-vig ─────────────────────────────────────────────────────────────
update_person_file("butch-vig",
  new_bands=[],
  new_credits=[
    ("album","gish","Gish","producer","Smashing Pumpkins"),
    ("album","siamese-dream","Siamese Dream","producer","Smashing Pumpkins"),
    ("album","saturation","Saturation","producer","Urge Overkill"),
    ("song","cherub-rock","Cherub Rock","producer","Smashing Pumpkins"),
    ("song","today-sp","Today","producer","Smashing Pumpkins"),
    ("song","disarm","Disarm","producer","Smashing Pumpkins"),
    ("song","sister-havana","Sister Havana","producer","Urge Overkill"),
  ])

# ── stone-gossard ─────────────────────────────────────────────────────────
update_person_file("stone-gossard",
  new_bands=[
    ("mother-love-bone","Mother Love Bone","Guitarist"),
    ("temple-of-the-dog","Temple of the Dog","Guitarist"),
    ("green-river","Green River","Guitarist"),
  ],
  new_credits=[
    ("album","apple","Apple","guitarist","Mother Love Bone"),
    ("album","temple-of-the-dog","Temple of the Dog","guitarist","Temple of the Dog"),
    ("song","stardog-champion","Stardog Champion","guitarist","Mother Love Bone"),
    ("song","hunger-strike","Hunger Strike","guitarist","Temple of the Dog"),
  ])

# ── jeff-ament ────────────────────────────────────────────────────────────
update_person_file("jeff-ament",
  new_bands=[
    ("mother-love-bone","Mother Love Bone","Bassist"),
    ("temple-of-the-dog","Temple of the Dog","Bassist"),
    ("green-river","Green River","Bassist"),
  ],
  new_credits=[
    ("album","apple","Apple","bass","Mother Love Bone"),
    ("album","temple-of-the-dog","Temple of the Dog","bass","Temple of the Dog"),
    ("song","stardog-champion","Stardog Champion","bass","Mother Love Bone"),
    ("song","hunger-strike","Hunger Strike","bass","Temple of the Dog"),
  ])

# ── kurt-cobain ───────────────────────────────────────────────────────────
update_person_file("kurt-cobain",
  new_bands=[],
  new_credits=[
    ("album","houdini","Houdini","producer","Melvins"),
    ("song","hooch","Hooch","producer","Melvins"),
    ("song","night-goat","Night Goat","producer","Melvins"),
  ])

print("Existing people updates done.")
print(f"FINAL: {_c} created, {_s} skipped")
