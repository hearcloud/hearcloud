import io, os # BytesIO

from django.core.files import File

from mutagen import File as MutaFile
from mutagen.mp4 import MP4, MP4Cover

from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import (ID3, APIC, TIT2, TPE1, TDRC, TALB, TPE2, TRCK, TBPM, 
                        TOPE, TKEY, TCOM, TEXT, COMM, TPE4, TPUB, TCON)

from datetime import timedelta

# ### #
# MP3 #
# ### #
def mp3_tags_to_song_model(audio_file_name, audio_file_path, song):
    """
    Read all the ID3 tags from an mp3 file an store them according to the
    song model attributes
    """
    # ID3 tags stuff
    # 1.- Creating a mutagen file instance
    file = MutaFile(audio_file_path)

    #print file.tags.getall("USLT")

    # 2.- Read all the ID3 tags from the file and save them on the song model
    for i in file.tags:
        # - APIC: Artwork
        if i.startswith("APIC"):
            image_data = file.tags[i].data
            image_io = io.BytesIO(image_data)
            image_name = os.path.splitext(audio_file_name)[0] + " - Artwork" + ".jpg"
            song.artwork.save(image_name, File(image_io))

        # - TIT2: Song Title
        elif i.startswith("TIT2"):
            song.song_title = file.tags[i].text[0]

        # - TPE1: Artist
        elif i.startswith("TPE1"):
            song.artist = file.tags[i].text[0]

        # - TDRC: Year
        elif i.startswith("TDRC"):
            song.year = int(file.tags[i].text[0].get_text())

        # - TALB: Album
        elif i.startswith("TALB"):
            song.album = file.tags[i].text[0]

        #: Release date?
        # release_date = 
        
        # - TPE2: Album artist
        elif i.startswith("TPE2"):
            song.album_artist = file.tags[i].text[0]

        # - TRCK: Track number
        elif i.startswith("TRCK"):
            song.track_number = int(file.tags[i].text[0].split('/')[0])

        # - TBPM: BPM
        elif i.startswith("TBPM"):
            song.bpm = float(file.tags[i].text[0])
        
        # - TOPE: Original artist
        elif i.startswith("TOPE"):
            song.original_artist = file.tags[i].text[0]

        # - TKEY: Key
        elif i.startswith("TKEY"):
            song.key = file.tags[i].text[0]

        # - TCOM: Composer
        elif i.startswith("TCOM"):
            song.composer = file.tags[i].text[0]

        # - TEXT: Lyricist
        elif i.startswith("TEXT"):
            song.lyricist = file.tags[i].text[0]

        # - COMM: Comments
        elif i.startswith("COMM"):
            song.comments = file.tags[i].text[0]

        # - TPE4: Remixer
        elif i.startswith("TPE4"):
            song.remixer = file.tags[i].text[0]

        # - TPUB: Label/Publisher
        elif i.startswith("TPUB"):
            song.label = file.tags[i].text[0]

        # - TCON: Genre/content type
        elif i.startswith("TCON"):
            song.genre = file.tags[i].text[0]

    # Get the song length
    song.duration = timedelta(seconds=int(file.info.length))

def tags_from_song_model_to_mp3(song):
    """
    Read all the new model attributes and save them according to the ID3 tags
    of the mp3 file stored
    """
    # ID3 tags stuff
    # 1.- Creating an ID3 tag if not present or read it if present
    try: 
        tags = ID3(song.audio_file.path)
    except ID3NoHeaderError:
        tags = ID3()

    # 2.- Save everything into ID3 tags
    # - TIT2: Song Title
    tags["TIT2"] = TIT2(encoding=3, text=song.song_title.decode('unicode-escape'))

    # - TPE1: Artist
    tags["TPE1"] = TPE1(encoding=3, text=song.artist.decode('unicode-escape'))

    # - TDRC: Year
    tags["TDRC"] = TDRC(encoding=3, text=str(song.year).decode('unicode-escape'))

    # - TALB: Album
    tags["TALB"] = TALB(encoding=3, text=song.album.decode('unicode-escape'))

    #: Release date?
    # release_date = 
    
    # - TPE2: Album artist
    tags["TPE2"] = TPE2(encoding=3, text=song.album_artist.decode('unicode-escape'))

    # - TRCK: Track number
    tags["TRCK"] = TRCK(encoding=3, text=str(song.track_number).decode('unicode-escape'))

    # - TBPM: BPM
    tags["TBPM"] = TBPM(encoding=3, text=str(song.bpm).decode('unicode-escape'))

    # - TOPE: Original artist
    tags["TOPE"] = TOPE(encoding=3, text=song.original_artist.decode('unicode-escape'))

    # - TKEY: Key
    tags["TKEY"] = TKEY(encoding=3, text=song.key.decode('unicode-escape'))

    # - TCOM: Composer
    tags["TCOM"] = TCOM(encoding=3, text=song.composer.decode('unicode-escape'))

    # - TEXT: Lyricist
    tags["TEXT"] = TEXT(encoding=3, text=song.lyricist.decode('unicode-escape'))

    # - COMM: Comments
    tags["COMM"] = COMM(encoding=3, text=song.comments.decode('unicode-escape'))

    # - TPE4: Remixer
    tags["TPE4"] = TPE4(encoding=3, text=song.remixer.decode('unicode-escape'))

    # - TPUB: Label/Publisher
    tags["TPUB"] = TPUB(encoding=3, text=song.label.decode('unicode-escape'))

    # - TCON: Genre/content type
    tags["TCON"] = TCON(encoding=3, text=song.genre.decode('unicode-escape'))

    tags.save(song.audio_file.path)

# ### #
# M4A #
# ### #


def m4a_tags_to_song_model(audio_file_name, audio_file_path, song):
    """
    Read all the tags from an m4a file an store them according to the
    song model attributes
    """
    file = MP4(audio_file_path)

    # Read all tags and save them on the song model
    for i in file.tags:
        # - covr: Artwork
        if i.startswith("covr"):
            image_data = file.tags[i][0]
            artworkformat = "jpg"
            if file.tags[i][0].imageformat == MP4Cover.FORMAT_PNG:
                artworkformat = "png"
            
            image_io = io.BytesIO(image_data)
            song.artwork.save(
                os.path.splitext(audio_file_name)[0] + " - Artwork." + artworkformat, 
                File(image_io)
            )

        # - \xa9nam: Song Title
        elif i.startswith("\xa9nam"):
            song.song_title = file.tags[i][0]

        # - \xa9ART: Artist
        elif i.startswith("\xa9ART"):
            song.artist = file.tags[i][0]

        # - \xa9day: Year
        elif i.startswith("\xa9day"):
            song.year = int(file.tags[i][0])

        # - \xa9alb: Album
        elif i.startswith("\xa9alb"):
            song.album = file.tags[i][0]

        #: Release date?
        # release_date = 
        
        # - aART: Album artist
        elif i.startswith("aART"):
            song.album_artist = file.tags[i][0]

        # - trkn: Track number
        elif i.startswith("trkn"):
            song.track_number = int(file.tags[i][0][0])

        # - tmpo: BPM
        elif i.startswith("tmpo"):
            song.bpm = float(file.tags[i][0])
        
        # - ???: Original artist
        #elif i.startswith("TOPE"):
        #    song.original_artist = file.tags[i][0]

        # - ???: Key
        #elif i.startswith("TKEY"):
        #    song.key = file.tags[i].text[0]

        # - \xa9wrt: Composer
        elif i.startswith("\xa9wrt"):
            song.composer = file.tags[i][0]

        # - \xa9lyr: Lyricist
        elif i.startswith("\xa9lyr"):
            song.lyricist = file.tags[i][0]

        # - \xa9cmt: Comments
        elif i.startswith("\xa9cmt"):
            song.comments = file.tags[i][0]

        # - ???: Remixer
        #elif i.startswith("TPE4"):
        #    song.remixer = file.tags[i][0]

        # - ???: Label/Publisher
        #elif i.startswith("TPUB"):
        #    song.label = file.tags[i][0]

        # - \xa9gen: Genre/content type
        elif i.startswith("\xa9gen"):
            song.genre = file.tags[i][0]

    # Get the song length
    song.duration = timedelta(seconds=int(file.info.length))
