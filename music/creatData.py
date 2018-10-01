import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
import django

django.setup()
from music.models import Album, Song


def CreateAlbum():
    a = Album(artist='Taylor swift', album_title="red", genre="Country",
              album_logo="/Users/fanjialiang2401/Desktop/Imag/1_12.jpg")
    a.save()


def CreateSong():
    a = Album.objects.get(artist='Taylor swift')
    d = Song(song_title='red', album=a, file_type='mp3')
    d.save()


def Out():
    s = Album.objects.all()
    p = Song.objects.all()
    print(p)
    print(s)


def Delete():
    d = Album.objects.all()
    d.delete()


if __name__ == '__main__':
    # Delete()
    # CreateAlbum()
    # CreateSong()
    # Out()
    # Delete()
    album1 = Album.objects.get(pk=16)
    album1.song_set.create(song_title='i love bacon', file_type='mp3')
    album1.song_set.create(song_title='bucky is lucky', file_type='mp3')
    a = album1.song_set.all()
    print(a)
