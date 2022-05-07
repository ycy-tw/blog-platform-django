from django.http.response import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, QueryDict
from django.db.models import Count, F
from django.urls import reverse
from django.core.paginator import (
    Paginator, EmptyPage, PageNotAnInteger
)
from .forms import CommentForm, SearchForm, ArticleForm
from .models import Follow, Post, Like, Comment, CustomTag, Bookmark
from account.models import Account
from account.forms import UserEditForm
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
import pytz
import re


def my_bookmarks(request):

    user = request.user
    bookmark_posts = user.bookmark_set.all().values_list('post_id', flat=True)
    bookmarks = Post.objects.filter(id__in=list(bookmark_posts))

    paginator_post = Paginator(bookmarks, 6)
    page = request.GET.get('page')

    try:
        bookmarks = paginator_post.page(page)
    except PageNotAnInteger:
        bookmarks = paginator_post.page(1)
    except EmptyPage:
        bookmarks = paginator_post.page(paginator_post.num_pages)

    context = {
        'bookmarks': bookmarks
    }

    return render(request, 'article/bookmarks/bookmarks.html', context)


def author_profile(request, author):

    author = get_object_or_404(Account, username=author)
    follower = list(author.following.values_list('user', flat=True))

    posts = Post.objects \
        .filter(author=author) \
        .filter(status='published') \
        .order_by('-publish_date')

    comments = Comment.objects \
        .filter(name=author) \
        .order_by('-created')

    latest_comments = []
    for comment in comments:
        if comment.post.status == 'published':
            latest_comments.append(comment)

    paginator_post = Paginator(posts, 5)
    page = request.GET.get('page')

    try:
        posts = paginator_post.page(page)
    except PageNotAnInteger:
        posts = paginator_post.page(1)
    except EmptyPage:
        posts = paginator_post.page(paginator_post.num_pages)

    context = {
        'author': author,
        'posts': posts,
        'follower': follower,
        'latest_comments': latest_comments,
    }

    if request.user == author:

        form = UserEditForm(instance=request.user)
        context['form'] = form

    return render(request, 'article/profile/profile.html', context)


@csrf_exempt
def show_liked_user(request):

    if request.POST:

        if request.POST['Target'] == 'Comment':

            identify = request.POST['identify']
            comment = get_object_or_404(Comment, id=identify)
            likes_list = comment.like_set.all

        elif request.POST['Target'] == 'Post':

            identify = request.POST['identify']
            post = get_object_or_404(Post, id=identify)
            likes_list = post.like_set.all

        context = {
            'likes_list': likes_list,
        }

        return render(request, 'article/post/likes_list.html', context)


def post_page(request, slug):

    post = get_object_or_404(Post, slug=slug, status='published')
    comments = post.post_comments.all().order_by('created')
    likes = post.like_set.all().count()

    # for recommend posts
    current_post_tags = list(post.tags.values_list('id', flat=True))
    related_post = Post.objects \
        .filter(status='published') \
        .filter(tags__in=current_post_tags) \
        .exclude(slug=slug).distinct()[:2]
    context = {
        'post': post,
        'comments': comments,
        'likes': likes,
        'related_post': related_post,
        'form': CommentForm(),
    }

    return render(request, 'article/post/post.html', context)


def home_view(request):

    slogan_text2 = _('Come join us.')
    slogan_text3 = _('Share our knowledge.')

    slogan = f'[" {slogan_text2} ", " {slogan_text3} "]'

    # exclude default cover for beauty home page
    posts = Post.objects \
        .filter(status='published') \
        .exclude(cover_image='cover_photos/default_cover.jpg')

    featured_posts = posts.order_by('-post_views')[:5]

    hot_tags = posts \
        .values(name=F('tags__name')) \
        .annotate(num_times=Count('tags')) \
        .order_by('-num_times')[:5]

    topic_posts = posts \
        .annotate(count=Count('post_comments')) \
        .exclude(id__in=featured_posts) \
        .order_by('-count')[:4]

    latest_posts = posts \
        .order_by('-publish_date') \
        .exclude(id__in=featured_posts) \
        .exclude(id__in=topic_posts)[:4]

    most_popular = posts \
        .annotate(count=Count('bookmark')) \
        .order_by('-count') \
        .exclude(id__in=featured_posts) \
        .exclude(id__in=topic_posts) \
        .exclude(id__in=latest_posts)[:4]

    latest_comments = Comment.objects \
        .order_by('-created')[:5]

    if request.user.is_authenticated:
        logout = False
    else:
        logout = True

    context = {
        # 'featured_slider': featured_slider,
        'slogan': slogan,
        'featured_posts': featured_posts,
        'hot_tags': hot_tags,
        'latest_posts': latest_posts,
        'most_popular': most_popular,
        'latest_comments': latest_comments,
        'topic_posts': topic_posts,
        'logout': logout,  # for home page header background color
    }

    if featured_posts:

        top_featured_post = featured_posts[0]
        featured_posts = featured_posts[1:]

        context['top_featured_post'] = top_featured_post
        context['featured_posts'] = featured_posts

    return render(request, 'article/home/home.html', context)


@csrf_exempt
def bookmark(request):

    if request.POST:

        user = request.user

        if user.is_authenticated:

            identify = request.POST['identify']
            post = get_object_or_404(Post, id=identify)

            if Bookmark.objects.filter(post=post, user=user).exists():
                Bookmark.objects.filter(post=post, user=user).delete()
                action = 'Delete'

            else:
                bookmark = Bookmark(post=post, user=user)
                bookmark.save()
                action = 'Add'

            response = {'status': 'success', 'action': f'{action}'}
            return JsonResponse(response)

        else:

            action = 'RedirectLogIn'
            response = {'status': 'fail', 'action': f'{action}'}

            return JsonResponse(response)


@login_required
def stats(request):

    author = request.user
    posts = Post.objects.filter(author=author)
    views_count = posts.aggregate(Sum('post_views'))['post_views__sum']
    likes_count = posts.aggregate(Count('like'))['like__count']
    views_count = 0 if views_count == None else views_count

    context = {
        'posts': posts,
        'likes_count': likes_count,
        'views_count': views_count,
    }
    return render(request, 'article/stats/stats.html', context)


@login_required
@csrf_exempt
def delete_article(request, slug):

    post = get_object_or_404(Post, slug=slug)

    if request.user == post.author:
        post.delete()
        return JsonResponse({'status': 'success'})
    else:
        return Http404('?')


@login_required
def update_editor(request, slug):

    post = get_object_or_404(Post,  slug=slug)
    form = ArticleForm(instance=post)

    context = {
        'form': form,
        'mode': 'update',
        'slug': slug,
    }

    return render(request, 'article/editor/editor.html', context)


@login_required
@csrf_exempt
def update_article(request, slug):

    if request.POST:

        post = get_object_or_404(Post,  slug=slug)

        body = request.POST['body']
        cover_image = request.FILES.get('cover_image')
        description = request.POST['description']
        tags = request.POST['tags']
        status = request.POST['status']
        title = request.POST['title']

        # this will be a problem if one more language
        if request.POST['status'] == '公開':
            status = 'published'
        elif request.POST['status'] == '草稿':
            status = 'draft'
        else:
            status = request.POST['status']

        post.body = body
        post.description = description
        post.status = status
        post.title = title

        # delete original tags and add new updated tags
        ori_tags = list(post.tags.values_list('name', flat=True))
        for tag in ori_tags:
            post.tags.remove(tag)

        if len(tags) > 0:
            tags = tags.split(',')
            for tag in tags:
                post.tags.add(tag.strip())

        if cover_image:
            post.cover_image = cover_image

        post.save()

        if post.status == 'draft':
            response = {'status': 'success', 'action': 'to_backend'}
            return JsonResponse(response)
        else:
            response = {'status': 'success', 'action': 'to_article', 'slug': post.slug}
            return JsonResponse(response)


@login_required
def create_article(request):

    if request.POST:

        form = ArticleForm(request.POST)

        if form.is_valid():

            body = request.POST['body']
            cover_image = request.FILES.get('cover_image')
            description = request.POST['description']
            tags = request.POST['tags']
            status = request.POST['status']
            title = request.POST['title']
            author = request.user

            if request.POST['status'] == '公開':
                status = 'published'
            elif request.POST['status'] == '草稿':
                status = 'draft'
            else:
                status = request.POST['status']

            if title == '':
                title = 'Untitled'

            post = Post(
                body=body,
                description=description,
                author=author,
                status=status,
                title=title,
            )

            # order is matter, put this line before post.save()
            if cover_image:
                post.cover_image = cover_image

            # order is matter, you have to save post first for getting pk
            # then post.tags.add() will be fine
            post.save()

            if len(tags) > 0:

                tags = tags.split(',')
                for tag in tags:
                    post.tags.add(tag.strip())

            if post.status == 'draft':
                response = {'status': 'success', 'action': 'to_backend'}
                return JsonResponse(response)
            else:
                response = {'status': 'success', 'action': 'to_article', 'slug': post.slug}
                return JsonResponse(response)

        else:
            print(form.errors.as_data())


@login_required
def editor(request, mode):

    form = ArticleForm()
    context = {'form': form, 'mode': mode}

    return render(request, 'article/editor/editor.html', context)


@login_required
@csrf_exempt
def update_comment(request, comment_id):

    comment = Comment.objects.filter(id=comment_id).first()
    paras = QueryDict(request.body)
    updated_comment = paras.get('comment_body')

    if request.user == comment.name:
        comment.comment_body = updated_comment
        comment.save()

        context = {
            'comment': comment,
        }
        return render(request, 'article/post/comment.html', context)

    else:
        Http404('Who are you?')
        return JsonResponse({'status': 'update Fail'})


@login_required
@csrf_exempt
def delete_comment(request, comment_id):
    comment = Comment.objects.filter(id=comment_id).first()
    if request.user == comment.name:
        comment.delete()
        return JsonResponse({'status': 'deleted success'})
    else:
        Http404('Who are you?')
        return JsonResponse({'status': 'deleted fail'})


@login_required
def create_comment(request):

    if request.POST:

        new_reply_update = request.POST['new_reply_update']
        name = request.user
        post_id = request.POST['post_id']
        post = Post.objects.filter(id=post_id).first()
        comment_body = request.POST['comment_body']

        comment = Comment(
            post=post,
            name=name,
            comment_body=comment_body,
        )

        if new_reply_update == 'Reply':

            comment_id = int(request.POST['parent_comment_id'])
            comment.parent = Comment.objects.filter(id=comment_id).first()
            comment.save()
            context = {
                'comment': comment,
            }

            return render(request, 'article/post/child_comment.html', context)

        comment.save()
        context = {
            'comment': comment,
        }

        return render(request, 'article/post/parent_comment.html', context)


@login_required
def edit_profile(request):

    if request.POST:

        identify = request.POST['identify']
        name = request.POST['name']
        intro = request.POST['intro']
        profile_img = request.FILES.get('profile_img')

        author = get_object_or_404(Account, username=identify)
        author.name = name
        author.intro = intro

        if profile_img != None:
            # author.profile_img.delete()
            author.profile_img = profile_img

        author.save()
        context = {
            'author': author
        }

        return render(request, 'article/profile/author_profile.html', context)


def tag_result(request, tag_slug=None, condition=None):

    post_list = Post.objects.filter(status='published')

    if tag_slug:

        tag = get_object_or_404(CustomTag, name=tag_slug)

        if condition:

            if condition == 'latest':
                post_list = post_list.filter(tags__in=[tag]).order_by('-publish_date')

            if condition == 'view':
                post_list = post_list.filter(tags__in=[tag]).order_by('-post_views')

            if condition == 'popular':
                post_list = post_list.filter(tags__in=[tag]) \
                    .annotate(count=Count('post_comments')) \
                    .order_by('-count')

        else:
            post_list = post_list.filter(tags__in=[tag])

    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts,
        'keyword': tag,
        'search_type': 'tag',
    }

    return render(request, 'article/search.html', context)


def search_view(request):
    form = SearchForm()

    if 'query' in request.POST:
        form = SearchForm(request.POST)
        if form.is_valid():

            query = form.cleaned_data['query']
            return HttpResponseRedirect(
                reverse('article:search_result', kwargs={'keyword': query})
            )

    else:
        return redirect('article:home')


@csrf_exempt
def search_result(request, keyword, condition=None):

    post_list = Post.objects.filter(status='published')

    if condition:

        if condition == 'latest':
            post_list = post_list.filter(Q(title__contains=keyword) | Q(body__contains=keyword)).order_by('-publish_date')

        if condition == 'view':
            post_list = post_list.filter(Q(title__contains=keyword) | Q(body__contains=keyword)).order_by('-post_views')

        if condition == 'popular':
            post_list = post_list.filter(Q(title__contains=keyword) | Q(body__contains=keyword)) \
                .annotate(count=Count('post_comments')) \
                .order_by('-count')

    else:
        post_list = post_list.filter(Q(title__contains=keyword) | Q(body__contains=keyword))

    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'keyword': keyword,
        'page': page,
        'posts': posts,
        'search_type': 'normal',  # distinguish tag result and normal search
        'count': len(posts),
    }

    return render(request, 'article/search.html', context)


@csrf_exempt
def like(request):

    if request.POST:

        user = request.user

        if user.is_authenticated:

            post_or_comment = request.POST['post_or_comment']
            identify = request.POST['identify']

            # Check from post or comment
            if post_or_comment == 'Post':

                post = get_object_or_404(Post, id=identify)

                if Like.objects.filter(post=post, user=user).exists():
                    Like.objects.filter(post=post, user=user).delete()
                    action = 'Unlike'

                else:
                    like = Like(post=post, user=user)
                    like.save()
                    action = 'Like'

            if post_or_comment == 'Comment':

                comment = get_object_or_404(Comment, id=identify)

                if Like.objects.filter(comment=comment, user=user).exists():
                    Like.objects.filter(comment=comment, user=user).delete()
                    action = 'Unlike'

                else:
                    like = Like(comment=comment, user=user)
                    like.save()
                    action = 'Like'

            response = {'status': 'success', 'action': f'{action}'}

            return JsonResponse(response)

        else:

            action = 'RedirectLogIn'
            response = {'status': 'fail', 'action': f'{action}'}

            return JsonResponse(response)


@csrf_exempt
def follow(request):

    if request.POST:

        user = request.user

        if user.is_authenticated:

            following = request.POST['Following']
            following = get_object_or_404(Account, username=following)

            if Follow.objects.filter(user=user, following=following).exists():
                Follow.objects.filter(user=user, following=following).delete()
                action = 'Unfollow'

            else:
                bookmark = Follow(user=user, following=following)
                bookmark.save()
                action = 'Follow'

            response = {'status': 'success', 'action': f'{action}'}
            return JsonResponse(response)

        else:
            action = 'RedirectLogIn'
            response = {'status': 'fail', 'action': f'{action}'}

            return JsonResponse(response)


@login_required
def backend(request):

    author = request.user
    user_edit_form = UserEditForm(instance=request.user)

    context = {
        'author': author,
        'user_edit_form': user_edit_form,
        'timezones': pytz.common_timezones,
    }

    if request.POST:

        name = request.POST['name']
        intro = request.POST['intro']
        profile_img = request.FILES.get('profile_img')

        author = get_object_or_404(Account, username=author.username)
        author.name = name
        author.intro = intro

        if profile_img != None:
            author.profile_img = profile_img

        author.save()

        context['user_edit_form'] = UserEditForm(instance=author)
        context['author'] = author

        return render(request, 'article/backend/backend.html', context)

    return render(request, 'article/backend/backend.html', context)


@login_required
def set_loc(request):

    if request.method == 'POST':

        request.session['django_timezone'] = request.POST['timezone']
        previous_page = request.META.get('HTTP_REFERER', '/')

        return redirect(previous_page)


def handler404(request, exception):

    context = {}
    response = render(request, 'article/404.html', context=context)
    response.status_code = 404

    return response
