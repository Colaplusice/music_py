from django.contrib.auth.models import User
from .models import Song,Album
from django import forms

class AlbumForm(forms.ModelForm):

    class Meta:
        model=Album
        fields=['artist','album_title','genre','album_logo']


class SongForm(forms.ModelForm):

    class Meta():
        model=Song
        fields=['audio_file']


class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model=User
        fields=['username','email','password']


