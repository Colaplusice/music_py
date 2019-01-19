from . import views
from django.conf.urls import url

app_name = "music"
urlpatterns = [
    url(r"^$", views.Index, name="index"),
    # /music/album_
    url(r"^(?P<pk>[0-9]+)$", views.Detailview.as_view(), name="detail"),
    # /music/add
    url(r"^create_album/$", views.Creatalbum, name="album-add"),
    # /music/2/add_song
    url(r"^(?P<album_id>[0-9]+)/add_song/$", views.Add_Song, name="add_song"),
    # /music/2/delete_song/3
    url(r"delete_song/(?P<song_id>[0-9]+)$", views.Delete_song, name="song-delete"),
    # /music/2/delete
    url(r"^(?P<album_id>[0-9]+)/delete_album/$", views.Delete, name="album-delete"),
    # /music/logout
    url(r"^logout/$", views.Logout_user, name="logout"),
    # /music/login
    url(r"^login/$", views.Login_user, name="login"),
    # /music/register
    url(r"^register$", views.UserFormView.as_view(), name="register"),
    # music/albumid/favorite_album/
    url(
        r"^(?P<album_id>[0-9]+)/favorite_album/$",
        views.favorite_album,
        name="favorite_album",
    ),
    # music/song_id/favorite_song/
    url(
        r"^(?P<song_id>[0-9]+)/favorite_song/$",
        views.favorite_song,
        name="favorite_song",
    ),
]
