from django import forms
from phonenumber_field.formfields import PhoneNumberField

from .models import Song, Album
from .models import User


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ["album_title", "genre", "album_logo"]


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ["audio_file"]


class LoginForm(forms.Form):
    username = forms.CharField(
        label="昵称",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control required",'placeholder':'密码'}),
    )
    # phone = PhoneNumberField(widget=forms.TextInput(attrs={"class": "form-control required", 'placeholder': '手机号'}), label='手机号', required=True)
    #
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={"class": "form-control required", 'placeholder': '密码'}),
    )


class RegisterForm(forms.Form):
    username = forms.CharField(
        label="昵称(不可重复)",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': '昵称(不可重复)'}),
    )
    phone = PhoneNumberField(label='手机号', region='CN', widget=forms.TextInput(attrs={'class': 'form-control required', 'placeholder': '手机号'}))
    password1 = forms.CharField(
        label="密码",
        max_length=128,
        widget=forms.PasswordInput(attrs={"class": "form-control", 'placeholder': '密码'}),
    )
    password2 = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(attrs={"class": "form-control", 'placeholder': '确认密码'}),
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if len(username) < 6:
            raise forms.ValidationError(
                "Your username must be at least 6 characters long."
            )
        elif len(username) > 50:
            raise forms.ValidationError("Your username is too long.")
        else:
            filter_result = User.objects.filter(username=username)
            if len(filter_result) > 0:
                raise forms.ValidationError("Your username already exists.")
        return username

    def clean_name(self):
        name = self.cleaned_data.get("name")
        filter_result = User.objects.filter(name=name)
        if len(filter_result) > 0:
            raise forms.ValidationError("Your name already exists.")
        return name

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 6:
            raise forms.ValidationError("Your password is too short.")
        elif len(password1) > 20:
            raise forms.ValidationError("Your password is too long.")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password mismatch. Please enter again.")
        return password2
