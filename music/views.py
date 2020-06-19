# encoding=utf-8
from functools import wraps

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse

from music.models import *
from .forms import RegisterForm, LoginForm, SongForm, AlbumForm

AUDIO_FILE_TYPES = ["wav", "mp3", "ogg"]
IMAGE_FILE_TYPES = ["png", "jpg", "jpeg"]
app_name = "music"


def login_in(func):  # 验证用户是否登录
    @wraps(func)
    def wrapper(*args, **kwargs):
        request = args[0]
        is_login = request.session.get("login_in")
        if is_login:
            return func(*args, **kwargs)
        else:
            return redirect(reverse("login"))

    return wrapper


# 登录功能
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            # phone = form.cleaned_data["phone"]
            user = User.objects.filter(username=username).first()
            if user and user.password == password:
                request.session["login_in"] = True
                request.session["user_id"] = user.id
                request.session["name"] = username
                # 用户第一次注册，让他选标签
                # new = request.session.get('new')
                # if new:
                #     tags = Tags.objects.all()
                #     return render(request, 'music/choose_tag.html', {'tags': tags})
                return redirect(reverse("music:index"))
            else:
                return render(
                    request, "music/login.html", {"form": form, "message": "账户或密码错误"}
                )
        else:
            print('form invalid')
    else:
        form = LoginForm()
        return render(request, "music/login.html", {"form": form})


# 注册功能
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        error = None
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password2"]
            phone = form.cleaned_data['phone']
            User.objects.create(username=username, password=password, phone=phone)
            request.session['new'] = 'true'
            # 根据表单数据创建一个新的用户
            return redirect(reverse("music:login"))  # 跳转到登录界面
        else:
            return render(
                request, "music/register.html", {"form": form, "error": error}
            )  # 表单验证失败返回一个空表单到注册页面
    form = RegisterForm()
    return render(request, "music/register.html", {"form": form})


def logout(request):
    if not request.session.get("login_in", None):  # 不在登录状态跳转回首页
        return redirect(reverse("index"))
    request.session.flush()  # 清除session信息
    return redirect(reverse("index"))


def index(request):
    # try:
    # if not request.music.is_authenticated:
    #     return render(request, "music/login.html")
    # else:
    albums = Album.objects.all()
    songs = random_choice_songs()
    # query = request.GET.get("q")

    # if query:
    #     albums = albums.filter(
    #         Q(album_title__icontains=query) | Q(artist__icontains=query)
    #     ).distinct()
    #
    #     song_results = song_results.filter(Q(song_title__contains=query)).distinct()
    return render(
        request,
        "music/index.html",
        {"all_albums": albums, 'songs': songs},
    )
    # return render(request, "music/index.html", {"all_albums": albums})


# except Exception as e:
#     return render(request, 'music/httperror.html')


def detail(request, album_id):
    album=Album.objects.get(id=album_id)
    return render(request, 'music/detail.html',{'album':album})


def random_choice_songs():
    return Song.objects.order_by('?')[:5]


# add_song
def Add_Song(request, album_id):
    # 未登录
    if not request.music.is_authenticated:
        return render(request, "music/login.html")
    else:
        # 是否提交表单
        song_form = SongForm(request.POST or None, request.FILES or None)
        album = get_object_or_404(Album, pk=album_id)
        if song_form.is_valid():
            album_songs = album.song_set.all()

            # 判断歌曲是否存在
            for s in album_songs:
                if s.song_title == song_form.cleaned_data.get("name"):
                    context = {
                        "album": album,
                        "form": song_form,
                        "error": "you have already have this song",
                    }
                    return render(request, "music/add_song.html", context)

            song = song_form.save(commit=False)
            song.audio_file = request.FILES["audio_file"]
            a = request.FILES["audio_file"]
            a = str(a)
            song.album = album
            file_type = a.split(".")[-1]
            file_name = a.split(".")[0]
            song.song_title = file_name
            file_type = file_type.lower()
            # 格式不支持
            if file_type not in AUDIO_FILE_TYPES:
                context = {
                    "all_albums": album,
                    "form": song_form,
                    "error": "your song is not supported",
                }
                return render(request, "music/add_song.html", context)
            song.save()
            return render(request, "music/detail.html", {"album": album})

        else:
            context = {"form": song_form, "album": album}
            return render(request, "music/add_song.html", context)


# create album
def Creatalbum(request):
    # 未登录
    if not request.music.is_authenticated:
        return render(request, "music/login.html")
    else:
        album_form = AlbumForm(request.POST or None, request.FILES or None)
        if album_form.is_valid():
            album = album_form.save(commit=False)
            album.music = request.music
            album.album_logo = request.FILES["album_logo"]

            file_type = album.album_logo.url.split(".")[-1]
            file_type = file_type.lower()

            # 格式不对
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    "albums": album,
                    "form": album_form,
                    "error": "file type is not supported",
                }
                return render(request, "music/album_form.html", context)
            print("here is right")
            album.save()
            all_albums = Album.objects.filter(music=request.music)
            return render(request, "music/index.html", {"all_albums": all_albums})
        #
        else:
            # 处理从 details 页面发来的请求 返回到创建界面
            context = {"form": album_form}
            return render(request, "music/album_form.html", context)


# Delete
def Delete(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    album.delete()
    all_albums = Album.objects.filter(music=request.music)
    return render(request, "music/index.html", {"all_albums": all_albums})


def Delete_song(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    song.delete()
    album = song.album
    return render(request, "music/detail.html", {"album": album})


# register


def favorite_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)

    try:
        if album.is_favorite:
            album.is_favorite = False
        else:
            album.is_favorite = True

        album.save()
    except (KeyError, Album.DoesNotExist):
        return JsonResponse({"success": False})
    all_album = Album.objects.filter(music=request.music)
    return render(request, "music/index.html", {"all_albums": all_album})


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
    except (KeyError, Song.DoesNotExist):
        return JsonResponse({"error": "song is not exist"})
    return render(request, "music/detail.html", {"album": album})
