from django.urls import path
from .views import (
    post_page,
    home_view,
    tag_result,
    search_view,
    search_result,
    author_profile,
    create_comment,
    delete_comment,
    update_comment,
    like,
    edit_profile,
    create_article,
    update_article,
    stats,
    backend,
    delete_article,
    bookmark,
    follow,


    home_view,
    post_page,
    show_liked_user,
    set_loc,
    editor,
    update_editor,
    my_bookmarks,
)

app_name = 'article'

urlpatterns = [

    path('', home_view, name='home'),
    path('a/<str:slug>', post_page, name='post_page'),

    # comment system
    path('create_comment', create_comment, name='create_comment'),
    path('delete_comment/<int:comment_id>', delete_comment, name='delete_comment'),
    path('update_comment/<int:comment_id>', update_comment, name='update_comment'),

    path('search', search_view, name='search_view'),
    path('search/<str:keyword>', search_result, name='search_result'),
    path('search/<str:keyword>/<str:condition>', search_result, name='condition_search_result'),

    # function url
    path('show_liked_user', show_liked_user, name='show_like_user'),
    path('like', like, name='like'),
    path('bookmark', bookmark, name='bookmark'),
    path('follow', follow, name='follow'),

    path('set_loc', set_loc, name='set_loc'),

    # article
    path('create_article', create_article, name='create_article'),
    path('delete_article/<str:slug>', delete_article, name='delete_article'),
    path('update_article/<str:slug>', update_article, name='update_article'),


    path('<str:mode>-article', editor, name='editor'),
    path('update/<str:slug>', update_editor, name='update_editor'),
    path('bookmarks', my_bookmarks, name='my_bookmarks'),

    path('tag/<str:tag_slug>/', tag_result, name='tag_result'),
    path('tag/<str:tag_slug>/<str:condition>', tag_result, name='condition_tag_result'),

















    # path('', home_view),  # , name='home'),



    #path('a/<str:slug>', post_page, name='post_page'),
    path('author/<str:author>', author_profile, name='author_profile'),

    path('stats', stats, name='stats'),
    path('backend', backend, name='backend'),
    path('edit_profile', edit_profile, name='edit_profile'),





]
