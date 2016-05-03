import io, os # BytesIO

from django.core.files import File

from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import (ID3, APIC, TIT2, TPE1, TDRC, TALB, TPE2, TRCK, TBPM, 
                        TOPE, TKEY, TCOM, TEXT, COMM, TPE4, TPUB, TCON)

def mp3_tags_to_song_model(audio_file_name, audio_file_path, song):
    """
    Read all the ID3 tags from an mp3 file an store them according to the
    song model attributes
    """
    # ID3 tags stuff
    # 1.- Creating an ID3 tag if not present or read it if present
    try: 
        tags = ID3(audio_file_path)
    except ID3NoHeaderError:
        tags = ID3()

    # 2.- Read all the ID3 tags and save them on the song model
    for i in tags:
        # - APIC: Artwork
        if i.startswith("APIC"):
            image_data = tags[i].data
            image_io = io.BytesIO(image_data)
            song.artwork.save(
                os.path.splitext(audio_file_name)[0] + " - Artwork.jpg", 
                File(image_io)
            )

        # - TIT2: Song Title
        elif i.startswith("TIT2"):
            song.song_title = tags[i].text[0]

        # - TPE1: Artist
        elif i.startswith("TPE1"):
            song.artist = tags[i].text[0]

        # - TDRC: Year
        elif i.startswith("TDRC"):
            song.year = int(tags[i].text[0].get_text())

        # - TALB: Album
        elif i.startswith("TALB"):
            song.album = tags[i].text[0]

        #: Release date?
        # release_date = 
        
        # - TPE2: Album artist
        elif i.startswith("TPE2"):
            song.album_artist = tags[i].text[0]

        # - TRCK: Track number
        elif i.startswith("TRCK"):
            print tags[i].text[0]
            song.track_number = int(tags[i].text[0].split('/')[0])

        # - TBPM: BPM
        elif i.startswith("TBPM"):
            song.bpm = float(tags[i].text[0])
        
        # - TOPE: Original artist
        elif i.startswith("TOPE"):
            song.original_artist = tags[i].text[0]

        # - TKEY: Key
        elif i.startswith("TKEY"):
            song.key = tags[i].text[0]

        # - TCOM: Composer
        elif i.startswith("TCOM"):
            song.composer = tags[i].text[0]

        # - TEXT: Lyricist
        elif i.startswith("TEXT"):
            song.lyricist = tags[i].text[0]

        # - COMM: Comments
        elif i.startswith("COMM"):
            song.comments = tags[i].text[0]

        # - TPE4: Remixer
        elif i.startswith("TPE4"):
            song.remixer = tags[i].text[0]

        # - TPUB: Label/Publisher
        elif i.startswith("TPUB"):
            song.label = tags[i].text[0]

        # - TCON: Genre/content type
        elif i.startswith("TCON"):
            song.genre = tags[i].text[0]

    return song;

def tags_from_song_model_to_mp3(song):
    """
    Read all the new model attributes and save them according to the ID3 tags
    of the mp3 file stored
    """
    # ID3 tags stuff
    # 1.- Creating an ID3 tag if not present or read it if present
    try: 
        tags = ID3(song.audio_file.path)
        print "Leo tags"
    except ID3NoHeaderError:
        print "No leo tags"
        tags = ID3()

    print tags

    # 2.- Save everything into ID3 tags
    # - TIT2: Song Title
    tags["TIT2"] = TIT2(encoding=3, text=song.song_title.decode('unicode-escape'))
    print "TIT2:" + str(tags["TIT2"])

    # - TPE1: Artist
    tags["TPE1"] = TPE1(encoding=3, text=song.artist.decode('unicode-escape'))
    print "TPE1:" + str(tags["TPE1"])

    # - TDRC: Year
    tags["TDRC"] = TDRC(encoding=3, text=str(song.year).decode('unicode-escape'))
    print "TDRC:" + str(tags["TDRC"])

    # - TALB: Album
    tags["TALB"] = TALB(encoding=3, text=song.album.decode('unicode-escape'))
    print "TALB:" + str(tags["TALB"])

    #: Release date?
    # release_date = 
    
    # - TPE2: Album artist
    tags["TPE2"] = TPE2(encoding=3, text=song.album_artist.decode('unicode-escape'))
    print "TPE2:" + str(tags["TPE2"])

    # - TRCK: Track number
    tags["TRCK"] = TRCK(encoding=3, text=str(song.track_number).decode('unicode-escape'))
    print "TRCK:" + str(tags["TRCK"])

    # - TBPM: BPM
    tags["TBPM"] = TBPM(encoding=3, text=str(song.bpm).decode('unicode-escape'))
    print "TBPM:" + str(tags["TBPM"])

    # - TOPE: Original artist
    tags["TOPE"] = TOPE(encoding=3, text=song.original_artist.decode('unicode-escape'))
    print "TOPE:" + str(tags["TOPE"])

    # - TKEY: Key
    tags["TKEY"] = TKEY(encoding=3, text=song.key.decode('unicode-escape'))
    print "TKEY:" + str(tags["TKEY"])

    # - TCOM: Composer
    tags["TCOM"] = TCOM(encoding=3, text=song.composer.decode('unicode-escape'))
    print "TCOM:" + str(tags["TCOM"])

    # - TEXT: Lyricist
    tags["TEXT"] = TEXT(encoding=3, text=song.lyricist.decode('unicode-escape'))
    print "TEXT:" + str(tags["TEXT"])

    # - COMM: Comments
    tags["COMM"] = COMM(encoding=3, text=song.comments.decode('unicode-escape'))
    print "COMM:" + str(tags["COMM"])

    # - TPE4: Remixer
    tags["TPE4"] = TPE4(encoding=3, text=song.remixer.decode('unicode-escape'))
    print "TPE4:" + str(tags["TPE4"])

    # - TPUB: Label/Publisher
    tags["TPUB"] = TPUB(encoding=3, text=song.label.decode('unicode-escape'))
    print "TPUB:" + str(tags["TPUB"])

    # - TCON: Genre/content type
    tags["TCON"] = TCON(encoding=3, text=song.genre.decode('unicode-escape'))
    print "TCON:" + str(tags["TCON"])

    tags.save(song.audio_file.path)
