from django.contrib import admin

from django.contrib import admin

from recommandation.utils.getSerieInfo import getInfos
from .models import Series, KeyWords, Posting, Rating

@admin.register(Series)
class Seriesdmin(admin.ModelAdmin):
    list_display = ('name', 'real_name')
    actions = [getInfos]

    class Meta:
        verbose_name_plural = "Series"

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    pass

@admin.register(Posting)
class PostingAdmin(admin.ModelAdmin):
    pass