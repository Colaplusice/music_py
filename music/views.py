# encoding=utf-8
from django.views import generic
from django.views.generic.edit import View
from .models import Album, Song
from .forms import UserForm, AlbumForm, SongForm
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']
app_name = 'music'


def Index(request):
    # try:
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        albums = Album.objects.filter(user=request.user)
        song_results = Song.objects.all()
        query = request.GET.get("q")
        if query:
            albums = albums.filter(Q(album_title__icontains=query) |
                                   Q(artist__icontains=query)
                                   ).distinct()

            song_results = song_results.filter(Q(song_title__contains=query)
                                               ).distinct()
            return render(request, 'music/index.html', {'all_albums': albums, 'songs': song_results})

    return render(request, 'music/index.html', {'all_albums': albums})


# except Exception as e:
#     return render(request, 'music/httperror.html')


class Detailview(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'


# add_song
def Add_Song(request, album_id):
    # 未登录
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        # 是否提交表单
        song_form = SongForm(request.POST or None, request.FILES or None)
        album = get_object_or_404(Album, pk=album_id)
        if song_form.is_valid():
            album_songs = album.song_set.all()

            # 判断歌曲是否存在
            for s in album_songs:
                if s.song_title == song_form.cleaned_data.get("song_title"):
                    context = {
                        'album': album,
                        'form': song_form,
                        'error': 'you have already have this song'
                    }
                    return render(request, 'music/add_song.html', context)

            song = song_form.save(commit=False)
            song.audio_file = request.FILES['audio_file']
            a = request.FILES['audio_file']
            a = str(a)
            song.album = album
            file_type = a.split('.')[-1]
            file_name = a.split('.')[0]
            song.song_title = file_name
            file_type = file_type.lower()
            # 格式不支持
            if file_type not in AUDIO_FILE_TYPES:
                context = {
                    'all_albums': album,
                    'form': song_form,
                    'error': 'your song is not supported'
                }
                return render(request, 'music/add_song.html', context)
            song.save()
            return render(request, 'music/detail.html', {'album': album})

        else:
            context = {'form': song_form, 'album': album}
            return render(request, 'music/add_song.html', context)


# create album
def Creatalbum(request):
    # 未登录
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        album_form = AlbumForm(request.POST or None, request.FILES or None)
        if album_form.is_valid():
            album = album_form.save(commit=False)
            album.user = request.user
            album.album_logo = request.FILES['album_logo']

            file_type = album.album_logo.url.split('.')[-1]
            file_type = file_type.lower()

            # 格式不对
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'albums': album,
                    'form': album_form,
                    'error': 'file type is not supported'
                }
                return render(request, 'music/album_form.html', context)
            print('here is right')
            album.save()
            all_albums = Album.objects.filter(user=request.user)
            return render(request, 'music/index.html', {'all_albums': all_albums})
        #
        else:
            # 处理从 details 页面发来的请求 返回到创建界面
            context = {"form": album_form}
            return render(request, 'music/album_form.html', context)


# Delete
def Delete(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    album.delete()
    all_albums = Album.objects.filter(user=request.user)
    return render(request, 'music/index.html', {'all_albums': all_albums})


def Delete_song(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    song.delete()
    album = song.album
    return render(request, 'music/detail.html', {'album': album})


# register

class UserFormView(View):
    form_class = UserForm
    template_name = 'music/register.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})
        pass

    def post(self, request):
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            user.set_password(password)
            user.save()
            # return
            user = authenticate(username=username, password=password)
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                print(albums)
                return render(request, 'music/index.html', {'all_albums': albums})

            context = {"form": user_form}
        return render(request, 'music/register.html', context)


# login
def Login_user(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:

            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'all_albums': albums})
            else:
                return render(request, 'music/index.html', {'error': 'you account is not active'})
        else:
            return render(request, 'music/login.html', {'error': 'invaild account'})

    else:
        return render(request, 'music/login.html')


# logout
def Logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)

    context = {
        'form': form
    }
    return render(request, 'music/login.html', context)


# favorite album
def favorite_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)

    try:
        if album.is_favorite:
            album.is_favorite = False
        else:
            album.is_favorite = True

        album.save()
    except(KeyError, Album.DoesNotExist):
        return JsonResponse({'success': False})
    all_album = Album.objects.filter(user=request.user)
    return render(request, 'music/index.html', {'all_albums': all_album})


# favorite song
def favorite_song(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    album = song.album
    try:
        if song.is_favorite:
            song.is_favorite = False
        else:
            song.is_favorite = True

        song.save()
    except(KeyError, Song.DoesNotExist):
        return JsonResponse({'error': 'song is not exist'})
    return render(request, 'music/detail.html', {'album': album})
