from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from article.models import Bookmark, Follow, Post, CustomTag, Account
from .forms import SearchForm
from notification.models import Notification
from django.db.models import Count


def common_context(request):

    context = {}
    user = request.user
    suggested_keywords = CustomTag.objects.annotate(count=Count('name')).order_by('count')[:3]

    if user.is_authenticated:

        user = get_object_or_404(Account, username=user.username)

        notifications = Notification.objects.filter(receiver=user)\
            .order_by('-date')
        context['notifications'] = notifications

        who_following_me = list(user.following.values_list('user', flat=True))
        my_following_list = list(user.follower.values_list('following', flat=True))
        liked_comments = user.like_set.all().values_list('comment_id', flat=True)
        liked_posts = user.like_set.all().values_list('post_id', flat=True)
        bookmark_posts = user.bookmark_set.all().values_list('post_id', flat=True)

        context['user'] = user
        context['user_id'] = user.username
        context['who_following_me'] = who_following_me
        context['my_following_list'] = my_following_list
        context['liked_comments'] = liked_comments
        context['liked_posts'] = liked_posts
        context['bookmark_posts'] = bookmark_posts

        unread = len(Notification.objects.filter(receiver=user).filter(is_seen=False))
        if unread > 0:
            context['unread'] = unread

    context['search_form'] = SearchForm
    context['suggested_keywords'] = suggested_keywords

    return context


def recommend_posts(request):

    recommend_category1 = _('You may like')
    recommend_category2 = _('Try some new')
    recommend_category3 = _('What is special')

    recommend_post1 = Post.objects \
        .filter(status='published') \
        .order_by('-post_views')[:3]

    recommend_post2 = Post.objects \
        .filter(status='published') \
        .order_by('-post_views')[:3]

    recommend_post3 = Post.objects \
        .filter(status='published') \
        .order_by('-post_views')[:3]

    context = {
        'recommend_category1': recommend_category1,
        'recommend_category2': recommend_category2,
        'recommend_category3': recommend_category3,
        'recommend_post1': recommend_post1,
        'recommend_post2': recommend_post2,
        'recommend_post3': recommend_post3,
    }

    return context
