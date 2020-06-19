"""
@time: 2020-06-10 08:08
@author: colaplusice
@contact: fjl2401@163.com vx:18340071291
"""
import datetime
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "music_py.settings")
django.setup()
image_url = 'https://avatars2.githubusercontent.com/u/29660460?s=460&u=8acdf1db716bbda333dbeb09cd0219977063464a&v=4'
from music.models import Album, Song, Word

data_path = '../data'


def populate_album_song_word():
    albums = os.listdir(data_path)
    for album in albums:
        album_path = os.path.join(data_path, album)
        if not os.path.isdir(album_path):
            continue
        for file in os.listdir(album_path):
            file_path = os.path.join(album_path, file)
            if not file_path.endswith('.txt'):
                continue
            with open(file_path, 'r', encoding='utf8')as opener:
                lines = opener.readlines()
                author = lines[0].split('：')[1].strip()
                like_num = lines[1].split('：')[1].strip()
                cover = lines[2].split('：')[1].strip()
                created = lines[3].split('：')[1:]
                created = '：'.join(created).strip()
                date_time_obj = datetime.datetime.strptime(created, '%Y/%m/%d %H：%M')
                size = lines[4].split('：')[1].strip()
                title = lines[5].split('：')[1].strip()
                content = lines[6].split('：')[1].strip()
                translation = lines[7].split('：')[1].strip()
                words = lines[8].split('：')[1].split(' ')
                audio_url = lines[9].split('：')[1].strip()
                album = lines[10].split('：')[1].strip()
                watched_num = lines[11].split('：')[1].strip()
                # word = models.ManyToManyField(Word, verbose_name='单词')
                # created = models.DateTimeField(auto_now=True)
                # size = models.FloatField(verbose_name='文件大小')
                # view_num = models.IntegerField(default=0, verbose_name='播放数')

                album, _ = Album.objects.get_or_create(album_title=album, defaults={'album_logo': image_url})
                print('add album: {} {}'.format(album.album_title, created))

                song, created = Song.objects.get_or_create(name=title, defaults={'audio_file': audio_url, 'author': author,
                                                                                 'view_num': watched_num, 'size': size[:-2],
                                                                                 'content': content,
                                                                                 'translation': translation,
                                                                                 'album': album,
                                                                                 'created': date_time_obj
                                                                                 })
                print('add song: {} {}'.format(song.name, created))

                for word in words:
                    word, created = Word.objects.get_or_create(content=word)
                    song.word.add(word)
                print(author, like_num, cover, created, size, title, content, translation, word, audio_url, album, watched_num)

        # print(album)


if __name__ == '__main__':
    populate_album_song_word()
