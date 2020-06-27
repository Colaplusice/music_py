import random

from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField


class User(models.Model):
    username = models.CharField(max_length=255, unique=True, verbose_name="账号")
    password = models.CharField(max_length=255, verbose_name="密码")
    phone = PhoneNumberField(null=False, blank=False, unique=True)


class Album(models.Model):
    # user = models.ForeignKey(User, default=1, on_delete=True)
    # is_favorite = models.BooleanField(default=False)
    # artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100, default='英语')
    album_logo = models.FileField()

    def __str__(self):
        return self.album_title + " - " + self.genre


class Word(models.Model):
    content = models.CharField(max_length=32, verbose_name='单词内容')

    def __str__(self):
        return self.content


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, verbose_name='音频专辑')
    name = models.CharField(max_length=250, verbose_name='名字')
    author = models.CharField(verbose_name='作者', max_length=128)
    audio_file = models.URLField(null=False)
    content = models.TextField(verbose_name='音频内容')
    word = models.ManyToManyField(Word, verbose_name='单词')
    created = models.DateTimeField(auto_now=True)
    size = models.FloatField(verbose_name='文件大小')
    view_num = models.IntegerField(default=0, verbose_name='播放数')
    translation = models.TextField(verbose_name='翻译内容')

    def __str__(self):
        return self.name

    # def on
    def delete(self, using=None, keep_parents=False):
        file = Song.objects.filter(audio_file=self.audio_file)
        file.delete()
        super(Song, self).delete()


@receiver(signals.post_init, sender=Song)
def create_word(sender, instance, **kwargs):
    
    print('this is sender', sender, type(sender))
    print('this is intstance', instance, type(instance))


class UserSong(models.Model):
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    song = models.ForeignKey(Song, verbose_name='歌曲', on_delete=models.CASCADE)
    finished = models.SmallIntegerField(verbose_name='当前状态')


def gen_newcode():
    length = 5
    strs = 'abcdefghijk_mnopqrstuvwxyz'
    new_code = ''.join(random.choices(strs, k=length))
    code = RegisterCode.objects.filter(code=new_code).first()
    while code is not None:
        new_code = ''.join(random.choices(strs, k=length))
        code = RegisterCode.objects.filter(code=new_code).first()
    return code


class RegisterCode(models.Model):
    # 注册码
    code = models.CharField(primary_key=True, default=gen_newcode, max_length=10)
