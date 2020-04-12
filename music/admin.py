from django.contrib import admin
from music.models import Album, Song

# register your models here.
admin.site.register(Album)

admin.site.register(Song)
