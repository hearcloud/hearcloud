import io  # BytesIO
import os

from django.core.files import File

from mutagen import File as MutaFile
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4, MP4Cover, MP4Tags
from mutagen.aiff import _IFFID3

from mutagen.id3 import ID3NoHeaderError, ID3
from mutagen.id3._frames import (APIC, TIT2, TPE1, TDRC, TALB, TPE2, TRCK, TBPM,
                                 TOPE, TKEY, TCOM, TEXT, COMM, TPE4, TPUB, TCON, USLT)

from datetime import timedelta

###############################################################################
#                               Common functions                              #
###############################################################################
def read_and_store_id3_tags(audio_file, file_name, song):
    """
    Read all the ID3 tags from the file and save them on the song model
    """
    for i in audio_file.tags:
        # - APIC: Artwork
        if i.startswith("APIC"):
            image_data = audio_file.tags[i].data
            image_io = io.BytesIO(image_data)
            image_name = os.path.splitext(file_name)[0] + " - Artwork" + ".jpg"
            song.artwork.save(image_name, File(image_io))

        # - TIT2: Song Title
        elif i.startswith("TIT2"):
            song.title = audio_file.tags[i].text[0]

        # - TPE1: Artist
        elif i.startswith("TPE1"):
            song.artist = audio_file.tags[i].text[0]

        # - TDRC: Year
        elif i.startswith("TDRC"):
            try:
                song.year = int(audio_file.tags[i].text[0].get_text())
            except ValueError:
                pass

        # - TALB: Album
        elif i.startswith("TALB"):
            song.album = audio_file.tags[i].text[0]

        #: Release date?
        # release_date =

        # - TPE2: Album artist
        elif i.startswith("TPE2"):
            song.album_artist = audio_file.tags[i].text[0]

        # - TRCK: Track number
        elif i.startswith("TRCK"):
            try:
                aux = audio_file.tags[i].text[0].split('/')
                if len(aux) > 1:
                    song.track_number = int(aux[0])
                    song.track_total = int(aux[1])
                else:
                    song.track_number = int(aux[0])
                    song.track_total = int(aux[0])
            except ValueError:
                pass

        # - TBPM: BPM
        elif i.startswith("TBPM"):
            try:
                song.bpm = float(audio_file.tags[i].text[0])
            except ValueError:
                pass

        # - TOPE: Original artist
        elif i.startswith("TOPE"):
            song.original_artist = audio_file.tags[i].text[0]

        # - TKEY: Key
        elif i.startswith("TKEY"):
            song.key = audio_file.tags[i].text[0]

        # - TCOM: Composer
        elif i.startswith("TCOM"):
            song.composer = audio_file.tags[i].text[0]

        # - TEXT: Lyricist
        elif i.startswith("TEXT"):
            song.lyricist = audio_file.tags[i].text[0]

        # - COMM: Comments
        elif i.startswith("COMM"):
            song.comments = audio_file.tags[i].text[0]

        # - TPE4: Remixer
        elif i.startswith("TPE4"):
            song.remixer = audio_file.tags[i].text[0]

        # - TPUB: Label/Publisher
        elif i.startswith("TPUB"):
            song.label = audio_file.tags[i].text[0]

        # - TCON: Genre/content type
        elif i.startswith("TCON"):
            song.genre = audio_file.tags[i].text[0]

        # -
        elif i.startswith("USLT"):
            song.lyrics = audio_file.tags[i].text


def save_song_attrs_to_id3tags(tags, song):
    # - APIC: Artwork
    if song.artwork:
        tags["APIC"] = APIC(
            encoding=3,  # 3 is for utf-8
            mime='image/jpeg',  # image/jpeg or image/png
            type=3,  # 3 is for the cover image
            desc=u'Cover',
            data=song.artwork.read()
        )

    # - TIT2: Song Title
    if song.title:
        tags["TIT2"] = TIT2(encoding=3, text=song.title.decode('unicode-escape'))

    # - TPE1: Artist
    if song.artist:
        tags["TPE1"] = TPE1(encoding=3, text=song.artist.decode('unicode-escape'))

    # - TDRC: Year
    if song.year:
        tags["TDRC"] = TDRC(encoding=3, text=str(song.year).decode('unicode-escape'))

    # - TALB: Album
    if song.album:
        tags["TALB"] = TALB(encoding=3, text=song.album.decode('unicode-escape'))

    #: Release date?
    # release_date =

    # - TPE2: Album artist
    if song.album_artist:
        tags["TPE2"] = TPE2(encoding=3, text=song.album_artist.decode('unicode-escape'))

    # - TRCK: Track number
    if song.track_number:
        tags["TRCK"] = TRCK(encoding=3, text=str(song.track_number).decode('unicode-escape'))

    # - TBPM: BPM
    if song.bpm:
        tags["TBPM"] = TBPM(encoding=3, text=str(song.bpm).decode('unicode-escape'))

    # - TOPE: Original artist
    if song.original_artist:
        tags["TOPE"] = TOPE(encoding=3, text=song.original_artist.decode('unicode-escape'))

    # - TKEY: Key
    if song.key:
        tags["TKEY"] = TKEY(encoding=3, text=song.key.decode('unicode-escape'))

    # - TCOM: Composer
    if song.composer:
        tags["TCOM"] = TCOM(encoding=3, text=song.composer.decode('unicode-escape'))

    # - TEXT: Lyricist
    if song.lyricist:
        tags["TEXT"] = TEXT(encoding=3, text=song.lyricist.decode('unicode-escape'))

    # - COMM: Comments
    if song.comments:
        tags["COMM"] = COMM(encoding=3, text=song.comments.decode('unicode-escape'))

    # - TPE4: Remixer
    if song.remixer:
        tags["TPE4"] = TPE4(encoding=3, text=song.remixer.decode('unicode-escape'))

    # - TPUB: Label/Publisher
    if song.label:
        tags["TPUB"] = TPUB(encoding=3, text=song.label.decode('unicode-escape'))

    # - TCON: Genre/content type
    if song.genre:
        tags["TCON"] = TCON(encoding=3, text=song.genre.decode('unicode-escape'))

    if song.lyrics:
        tags["USLT"] = USLT(encoding=3, text=song.lyrics.decode('unicode-escape'))


def read_and_store_mp4_tags(audio_file, file_name, song):
    # Read all tags and save them on the song model
    for i in audio_file.tags:
        # - covr: Artwork
        if i.startswith("covr"):
            image_data = audio_file.tags[i][0]
            artworkformat = "jpg"
            if audio_file.tags[i][0].imageformat == MP4Cover.FORMAT_PNG:
                artworkformat = "png"

            image_io = io.BytesIO(image_data)
            song.artwork.save(
                os.path.splitext(file_name)[0] + " - Artwork." + artworkformat,
                File(image_io)
            )

        # - \xa9nam: Song Title
        elif i.startswith("\xa9nam"):
            song.title = audio_file.tags[i][0]

        # - \xa9ART: Artist
        elif i.startswith("\xa9ART"):
            song.artist = audio_file.tags[i][0]

        # - \xa9day: Year
        elif i.startswith("\xa9day"):
            song.year = int(audio_file.tags[i][0])

        # - \xa9alb: Album
        elif i.startswith("\xa9alb"):
            song.album = audio_file.tags[i][0]

        #: Release date?
        # release_date =

        # - aART: Album artist
        elif i.startswith("aART"):
            song.album_artist = audio_file.tags[i][0]

        # - trkn: Track number
        elif i.startswith("trkn"):
            song.track_number = int(audio_file.tags[i][0][0])

        # - tmpo: BPM
        elif i.startswith("tmpo"):
            song.bpm = float(audio_file.tags[i][0])

        # - ???: Original artist
        # elif i.startswith("TOPE"):
        #    song.original_artist = file.tags[i][0]

        # - ???: Key
        # elif i.startswith("TKEY"):
        #    song.key = file.tags[i].text[0]

        # - \xa9wrt: Composer
        elif i.startswith("\xa9wrt"):
            song.composer = audio_file.tags[i][0]

        # - \xa9lyr: Lyricist/Lyrics
        elif i.startswith("\xa9lyr"):
            song.lyrics = audio_file.tags[i][0]

        # - \xa9cmt: Comments
        elif i.startswith("\xa9cmt"):
            song.comments = audio_file.tags[i][0]

        # - ???: Remixer
        # elif i.startswith("TPE4"):
        #    song.remixer = file.tags[i][0]

        # - ???: Label/Publisher
        # elif i.startswith("TPUB"):
        #    song.label = file.tags[i][0]

        # - \xa9gen: Genre/content type
        elif i.startswith("\xa9gen"):
            song.genre = audio_file.tags[i][0]


def save_song_attrs_to_mp4tags(tags, song):
    # - covr: Artwork
    if song.artwork:
        tags["covr"] = [
            MP4Cover(song.artwork.read(), imageformat=MP4Cover.FORMAT_JPEG)
        ]

    # - \xa9nam: Song Title
    if song.title:
        tags["\xa9nam"] = song.title.decode('unicode-escape')

    # - \xa9ART: Artist
    if song.artist:
        tags["\xa9ART"] = song.artist.decode('unicode-escape')

    # - \xa9day: Year
    if song.year:
        tags["\xa9day"] = str(song.year).decode('unicode-escape')

    # - \xa9alb: Album
    if song.album:
        tags["\xa9alb"] = song.album.decode('unicode-escape')

    # - Release date?
    # release_date =

    # - aART: Album artist
    if song.album_artist:
        tags["aART"] = song.album_artist.decode('unicode-escape')

    # - trkn: Track number
    if song.track_number:
        tags["trkn"] = str(song.track_number).decode('unicode-escape')

    # - tmpo: BPM
    if song.bpm:
        tags["tmpo"] = str(song.bpm).decode('unicode-escape')

    # - Original artist
    # if song.original_artist:
    #    ???

    # - Key
    # if song.key:
    #    ???

    # - \xa9wrt: Composer
    if song.composer:
        tags["\xa9wrt"] = song.composer.decode('unicode-escape')

    # - \xa9lyr: Lyricist
    if song.lyrics:
        tags["\xa9lyr"] = song.lyrics.decode('unicode-escape')

    # - \xa9cmt: Comments
    if song.comments:
        tags["\xa9cmt"] = song.comments.decode('unicode-escape')

    # - Remixer
    # if song.remixer:
    #    ???

    # - Label/Publisher
    # if song.label:
    #    ???

    # - \xa9gen: Genre/content type
    if song.genre:
        tags["\xa9gen"] = song.genre.decode('unicode-escape')

###############################################################################
#                                     MP3                                     #
###############################################################################
def mp3_tags_to_song_model(file_name, file_path, song):
    """
    Read all the ID3 tags from a mp3 file an store them according to the
    song model attributes
    """
    # ID3 tags stuff
    # Creating a mutagen file instance
    try:
        audio_file = MutaFile(file_path)

        if audio_file:
            read_and_store_id3_tags(audio_file, file_name, song)

            # Get the song length
            song.duration = timedelta(seconds=int(audio_file.info.length))
    except ValueError:
        pass


def tags_from_song_model_to_mp3(song, file_path):
    """
    Read all the new model attributes and save them according to the ID3 tags
    of the mp3 file stored
    """
    # ID3 tags stuff
    # 1.- Creating an ID3 tag if not present or read it if present
    try:
        tags = ID3(file_path)
    except ID3NoHeaderError:
        tags = ID3()

    save_song_attrs_to_id3tags(tags, song)

    tags.save(file_path)


###############################################################################
#                                     M4A                                     #
###############################################################################
def m4a_tags_to_song_model(file_name, file_path, song):
    """
    Read all the tags from a m4a file an store them according to the
    song model attributes
    """
    try:
        audio_file = MP4(file_path)

        if audio_file:
            read_and_store_mp4_tags(audio_file, file_name, song)

            # Get the song length
            song.duration = timedelta(seconds=int(audio_file.info.length))
    except ValueError:
        pass


def tags_from_song_model_to_m4a(song, file_path):
    """
    Read all the new model attributes and save them according to the MP4 tags
    of the m4a stored file
    """
    # Creating an MP4 tag if not present or read it if present
    try:
        tags = MP4(file_path).tags
    except ValueError:
        tags = MP4Tags()

    save_song_attrs_to_mp4tags(tags, song)

    tags.save(file_path)


###############################################################################
#                                     AIFF                                    #
###############################################################################
def aiff_tags_to_song_model(file_name, file_path, song):
    """
    Read all the ID3 tags from an aiff file an store them according to the
    song model attributes
    """
    # ID3 tags stuff
    # Creating a mutagen file instance
    try:
        audio_file = MutaFile(file_path)

        if audio_file.tags:
            read_and_store_id3_tags(audio_file, file_name, song)
        if audio_file:
            # Get the song length
            song.duration = timedelta(seconds=int(audio_file.info.length))
    except ValueError:
        pass


def tags_from_song_model_to_aiff(song, file_path):
    """
    Read all the new model attributes and save them according to the ID3 tags
    of the aiff file stored
    """
    # ID3 tags stuff
    # 1.- Creating an ID3 tag if not present or read it if present
    try:
        tags = _IFFID3(file_path)
    except ID3NoHeaderError:
        tags = _IFFID3()

    save_song_attrs_to_id3tags(tags, song)

    tags.save(file_path)


###############################################################################
#                                      WAV                                    #
###############################################################################
def wav_tags_to_song_model(file_name, file_path, song):
    """
    Read all the tags from a wav file an store them according to the
    song model attributes
    """
    pass

def tags_from_song_model_to_wav(song, file_path):
    """
    Read all the new model attributes and save them according to the Wav tags
    of the wav file stored
    """
    pass