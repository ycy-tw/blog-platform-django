from django.contrib import admin
from .models import Bookmark, Comment, CustomTag, Follow, Post, Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'publish_date', 'post_views', 'slug', 'author')
    list_filter = ('status', 'publish_date',)
    search_fields = ('title', 'body')
    date_hierarchy = 'publish_date'
    ordering = ('status', 'publish_date')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'comment_body', 'created', 'updated', 'post', 'parent')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'post')


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'following')


@admin.register(CustomTag)
class CustomTagAdmin(admin.ModelAdmin):
    pass
