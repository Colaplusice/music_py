"""
@time: 2020-06-28 21:57
@author: colaplusice
@contact: fjl2401@163.com vx:18340071291
"""
from django.http import JsonResponse

from music.models import UserSong


def have_listened(request):
    listened = UserSong.objects
    return JsonResponse(request)
