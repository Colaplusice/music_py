from django.urls import path

from . import views

app_name = "music"
urlpatterns = [
    # 登录注册
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),

    path('', views.index, name='index'),
    # /music/album_
    path('detail/<int:album_id>/', views.detail,name="detail"),
    # /music/add
    # url(r"^create_album/$", views.Creatalbum, name="index"),
    # /music/2/add_song
    # url(r"^(?P<album_id>[0-9]+)/add_song/$", views.Add_Song, name="add_song"),
    # /music/2/delete_song/3
    # url(r"delete_song/(?P<song_id>[0-9]+)$", views.Delete_song, name="song-delete"),
    # /music/2/delete
    # url(r"^(?P<album_id>[0-9]+)/delete_album/$", views.Delete, name="album-delete"),
    # /music/login
    # url(r"^login/$", views.Login_user, name="login"),
    # /music/register
    # url(r"^register$", views.UserFormView.as_view(), name="register"),
    # music/albumid/favorite_album/
    path(
        "<int:album_id>/favorite_album/",
        views.favorite_album,
        name="favorite_album",
    ),
    # music/song_id/favorite_song/
    path(
        "<int:song_id>/favorite_song/",
        views.favorite_song,
        name="favorite_song", )
]
