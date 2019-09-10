from django.contrib import admin

from song.models import Song, SongCategory

admin.site.register(Song)
admin.site.register(SongCategory)
