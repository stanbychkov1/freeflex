from django.contrib import admin

from . import models


class FileInline(admin.TabularInline):
    model = models.Course.file.through
    extra = 0
    min_num = 1


class LinkInline(admin.TabularInline):
    model = models.Course.link.through
    extra = 0
    min_num = 1


@admin.register(models.File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'file',)
    search_fields = ('title', 'file')
    list_filter = ('title',)
    empty_value_display = '-empty-'


@admin.register(models.Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'link',)
    search_fields = ('title', 'link')
    list_filter = ('title',)
    empty_value_display = '-empty-'


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'description',
                    'score',)
    exclude = ('file', 'link', 'score',)
    inlines = (FileInline, LinkInline,)
    search_fields = ('title',)
    list_filter = ('title', 'score',)
    empty_value_display = '-empty-'


@admin.register(models.Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'course', 'rating',)
    search_fields = ('user', 'course', 'rating',)
    list_filter = ('user', 'course', 'rating',)
    empty_value_display = '-empty-'


@admin.register(models.Subscription)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'course',)
    search_fields = ('user', 'course',)
    list_filter = ('user', 'course',)
    empty_value_display = '-empty-'
