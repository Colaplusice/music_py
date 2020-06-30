import random

from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class AutoCreatedField(models.DateTimeField):
    """
    A DateTimeField that automatically populates itself at
    object creation.

    By default, sets editable=False, default=datetime.now.

    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', False)
        kwargs.setdefault('default', now)
        super(AutoCreatedField, self).__init__(*args, **kwargs)


class AutoLastModifiedField(AutoCreatedField):
    """
    A DateTimeField that updates itself on each save() of the model.

    By default, sets editable=False and default=datetime.now.

    """

    def pre_save(self, model_instance, add):
        value = now()
        setattr(model_instance, self.attname, value)
        return value


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.

    """
    created = AutoCreatedField(_('created'))
    modified = AutoLastModifiedField(_('modified'))

    # 不能以此类直接建立表
    class Meta:
        abstract = True


class User(TimeStampedModel):
    username = models.CharField(max_length=255, unique=True, verbose_name="账号")
    password = models.CharField(max_length=255, verbose_name="密码")
    phone = PhoneNumberField(null=False, blank=False, unique=True)

    def __str__(self):
        return self.username


class Album(TimeStampedModel):
    # user = models.ForeignKey(User, default=1, on_delete=True)
    # is_favorite = models.BooleanField(default=False)
    # artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100, default='英语')
    album_logo = models.FileField()

    def __str__(self):
        return self.album_title + " - " + self.genre


class Word(TimeStampedModel):
    content = models.CharField(max_length=32, verbose_name='单词内容')

    def __str__(self):
        return self.content


class Song(TimeStampedModel):
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

    def save(self, *args, **kwargs):
        # 第一次添加单词时会更新释义
        if self._state.adding is True:
            word_content = self.content

        super(Song, self).save(*args, **kwargs)


class UserSong(TimeStampedModel):
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


class RegisterCode(TimeStampedModel):
    # 注册码
    code = models.CharField(primary_key=True, default=gen_newcode, max_length=10)


class UserWord(TimeStampedModel):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, verbose_name='单词')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    learned = models.BooleanField(verbose_name='是否掌握')

    def __str__(self):
        return self.user.username + ':' + self.word.content + '是否掌握:' + str(self.learned)


class MessageBoard(TimeStampedModel):
    title = models.CharField(max_length=32, verbose_name='公告标题')
    content = models.TextField(verbose_name='公告内容')

    def __str__(self):
        return self.content
