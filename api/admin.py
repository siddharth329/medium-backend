from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
# Register your models here.


class PostAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ('title', 'slug')
    list_display = ('title', 'upvote_count', 'published', 'created_at')
    list_filter = ('published',)
    ordering = ('-created_at',)
    fieldsets = (
        ('Required', {'fields': ('user', 'title', 'subtitle', 'content')}),
        ('Optionals', {'fields': ('cover_image', 'tags', 'published')}),
        ('Auto Generated', {'fields': ('slug', 'upvote_count', 'comment_count', 'read_time')}),
        ('Metrics', {'fields': ('published_at', 'created_at', 'updated_at')})
    )
    readonly_fields = ('published_at', 'created_at', 'updated_at')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Bookmark)
admin.site.register(Follower)
admin.site.register(Upvote)
admin.site.register(View)
