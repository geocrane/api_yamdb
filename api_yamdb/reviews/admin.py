""" Настройки админ панели."""
from django.contrib import admin

from reviews.models import Category, Genre, Review, Comment


class ReviewAdmin(admin.ModelAdmin):
    """ Настройка отображения по отзывам в админ панели."""
    list_display = ('pk', 'text', 'pub_date', 'author', 'title',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'



admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Comment)
