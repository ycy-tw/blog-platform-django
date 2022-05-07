from django.db import models
from django.db.models.signals import post_save, pre_delete
from account.models import Account
from article.models import Comment, Like, Post, Follow
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from blog.settings import BASE_DIR


class Notification(models.Model):

    CATEGORY = (
        ('like', 'Like',),
        ('follow', 'follow',),
        ('comment', 'Comment',),
        ('system', 'System',),
    )

    sender = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='notify_sender'
    )
    receiver = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='notify_receiver',
        null=True,
    )
    notify_text = models.CharField(max_length=255)
    notify_text_zhhant = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)
    is_seen = models.BooleanField(default=False)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='notify_post',
        null=True,
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='notify_comment',
        null=True
    )
    like = models.ForeignKey(
        Like,
        on_delete=models.CASCADE,
        related_name='notify_like',
        null=True
    )
    follow = models.ForeignKey(
        Follow,
        on_delete=models.CASCADE,
        related_name='notify_follow',
        null=True
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY,
        null=True,
    )


def notify(
    sender,
    receiver,
    category,
    notify_text,
    notify_text_zhhant,
    post=None,
    comment=None,
    like=None,
    follow=None,
):

    notification = Notification()
    notification.sender = sender
    notification.receiver = receiver
    notification.post = post
    notification.comment = comment
    notification.like = like
    notification.follow = follow
    notification.category = category
    notification.notify_text = notify_text
    notification.notify_text_zhhant = notify_text_zhhant
    notification.save()


def new_comment(sender, instance, **kwargs):

    comment = instance
    comment_user = comment.name  # user object
    comment_post = comment.post
    post_author = comment.post.author

    # it is a parent comment
    # parent comment only under a post
    if comment.parent is None:

        # author no need to notify himself
        if comment_user == post_author:
            pass
        else:

            # focus on parent comment
            who_commented_before = Comment.objects \
                .filter(post=comment_post) \
                .filter(parent=None) \
                .exclude(name=comment_user) \
                .order_by('-created') \
                .distinct()  # remove duplicated

            if len(who_commented_before) == 0:

                # no one liked before
                notify_text = f'{comment_user.name} commented on your post'
                notify_text_zhhant = f'{comment_user.name}在你的文章上留言'
                notify(
                    sender=comment_user,
                    receiver=post_author,
                    post=comment_post,
                    category='comment',
                    notify_text=notify_text,
                    notify_text_zhhant=notify_text_zhhant,
                )

            elif len(who_commented_before) > 0:

                # someone liked before, there should be a existed notification.
                notification = Notification.objects.filter(category='comment', post=comment_post)[0]

                how_many_users = len(who_commented_before)
                notify_text = f'{comment_user.name} and other {how_many_users} commented on your post.'
                notify_text_zhhant = f'{comment_user.name}和另外{how_many_users}位使用者在你的文章中留言'

                notification.notify_text = notify_text
                notification.notify_text_zhhant = notify_text_zhhant
                notification.is_seen = False
                notification.save()

            else:
                pass

    # it is a child comment
    else:
        # user no need to notify himself
        parent_comment_user = comment.parent.name
        if comment_user == parent_comment_user:
            pass
        else:
            who_commented_before = Comment.objects \
                .filter(parent=comment.parent) \
                .exclude(name=comment_user) \
                .order_by('-created') \
                .distinct()  # remove duplicated

            if len(who_commented_before) == 0:

                # no one liked before
                notify_text = f'{comment_user.name} replied to your comment.'
                notify_text_zhhant = f'{comment_user.name}回覆了你的留言'
                notify(
                    sender=comment_user,
                    receiver=parent_comment_user,
                    comment=comment.parent,
                    category='comment',
                    notify_text=notify_text,
                    notify_text_zhhant=notify_text_zhhant,
                )

            elif len(who_commented_before) > 0:

                # someone liked before, there should be a existed notification.
                notification = Notification.objects.filter(
                    category='comment',
                    comment=comment.parent
                )[0]

                how_many_users = len(who_commented_before)
                notify_text = f'{comment_user.name} and other {how_many_users} replied to your comment.'
                notify_text_zhhant = f'{comment_user.name}和另外{who_commented_before}回覆了你的留言'
                notification.notify_text = notify_text
                notification.notify_text_zhhant = notify_text_zhhant
                notification.is_seen = False
                notification.save()

            else:
                pass


def new_like(sender, instance, **kwargs):

    like = instance
    like_user = like.user
    like_user_name = like.user.name

    # Like comment
    if like.comment:

        if like_user == like.comment.name:
            pass

        else:
            who_liked_before = Like.objects \
                .filter(comment=like.comment) \
                .exclude(user=like_user) \
                .order_by('-created')

            if len(who_liked_before) == 0:

                # no one liked before
                notify_text = f'{like_user_name} likes your comment.'
                notify_text_zhhant = f'{like_user_name}喜歡你的留言'
                notify(
                    sender=like_user,
                    receiver=like.comment.name,
                    comment=like.comment,
                    category='like',
                    notify_text=notify_text,
                    notify_text_zhhant=notify_text_zhhant,
                )

            elif len(who_liked_before) > 0:

                # someone liked before, there should be a existed notification.
                notification = Notification.objects.filter(category='like', comment=like.comment)[0]

                how_many_users = len(who_liked_before)
                notify_text = f'{like_user_name} and other {how_many_users} like your comment'
                notify_text_zhhant = f'{like_user_name}和另外{how_many_users}位使用者喜歡你的留言'

                notification.notify_text = notify_text
                notification.notify_text_zhhant = notify_text_zhhant
                notification.is_seen = False
                notification.save()

            else:
                pass

    # Like post
    if like.post:

        if like_user == like.post.author:
            pass

        else:

            who_liked_before = Like.objects \
                .filter(post=like.post) \
                .exclude(user=like_user) \
                .order_by('-created')

            if len(who_liked_before) == 0:

                # no one liked before
                notify_text = f'{like_user_name} likes your post.'
                notify_text_zhhant = f'{like_user_name}喜歡你的文章'
                notify(
                    sender=like_user,
                    receiver=like.post.author,
                    post=like.post,
                    category='like',
                    notify_text=notify_text,
                    notify_text_zhhant=notify_text_zhhant,
                )

            elif len(who_liked_before) > 0:

                # someone liked before, there should be a existed notification.
                notification = Notification.objects.filter(category='like', post=like.post)[0]

                how_many_users = len(who_liked_before)
                notify_text = f'{like_user_name} and other {how_many_users} like your post.'
                notify_text_zhhant = f'{like_user_name}和另外{how_many_users}位使用者喜歡你的文章'

                notification.notify_text = notify_text
                notification.notify_text_zhhant = notify_text_zhhant
                notification.is_seen = False
                notification.save()

            else:
                pass


def new_follow(sender, instance, created, **kwargs):

    follow = instance
    username = follow.user.name
    notify_text = f'{username} starts following you.'
    notify_text_zhhant = f'{username}開始追蹤你'

    notify(
        sender=follow.user,
        receiver=follow.following,
        follow=follow,
        category='follow',
        notify_text=notify_text,
        notify_text_zhhant=notify_text_zhhant,
    )


def new_user(sender, instance, created, **kwargs):
    """Greeting from official"""

    if created and instance.username != 'KnowsList':

        official = get_object_or_404(
            Account,
            username='KnowsList',
            email='official@knowslist.com'

        )
        user = instance

        notification = Notification()
        notification.sender = official
        notification.receiver = user
        notification.category = 'system'
        notification.notify_text = f'Greeting from Knowslist! Share your knowledge today.'
        notification.notify_text_zhhant = f'來自Knowslist的問候，一起分享知識吧!'
        notification.save()

        # import os

        # # create user own directory
        # username = user.username
        # path = os.path.join(BASE_DIR, 'media', 'images', username)

        # if not os.path.exists(path):
        #     os.makedirs(path)

    else:
        pass


def delete_like(sender, instance, **kwargs):

    like = instance
    comment = like.comment
    post = like.post
    if like.comment:
        who_liked_before = Like.objects \
            .filter(comment=comment) \
            .exclude(user=like.user)

        how_many_users = len(who_liked_before)

        if how_many_users == 0:
            Notification.objects.filter(category='like', comment=comment).delete()

        elif how_many_users > 0:
            notification = Notification.objects.filter(category='like', comment=comment)[0]
            previous_sender = who_liked_before[0].user

            if how_many_users == 1:

                notification.sender = previous_sender
                notification.notify_text = f'{previous_sender.name} likes your comment.'
                notification.notify_text_zhhant = f'{previous_sender.name}喜歡你的留言'
                notification.save()

            else:
                how_many_users = how_many_users - 1
                notification.sender = previous_sender
                notification.notify_text = f'{previous_sender.name} and other {how_many_users} likes your comment.'
                notification.notify_text_zhhant = f'{previous_sender.name}和另外{how_many_users}使用者喜歡你的留言'
                notification.save()

        else:
            pass

    if like.post:
        who_liked_before = Like.objects \
            .filter(post=post) \
            .exclude(user=like.user)

        how_many_users = len(who_liked_before)

        if how_many_users == 0:
            Notification.objects.filter(category='like', post=post).delete()

        elif how_many_users > 0:
            notification = Notification.objects.filter(category='like', post=post)[0]
            previous_sender = who_liked_before[0].user

            if how_many_users == 1:

                notification.sender = previous_sender
                notification.notify_text = f'{previous_sender.name} likes your post.'
                notification.notify_text_zhhant = f'{previous_sender.name}喜歡你的文章'
                notification.save()

            else:
                how_many_users = how_many_users - 1
                notification.sender = previous_sender
                notification.notify_text = f'{previous_sender.name} and other {how_many_users} likes your comment.'
                notification.notify_text_zhhant = f'{previous_sender.name}和另外{how_many_users}使用者喜歡你的文章'
                notification.save()

        else:
            pass


def delete_comment(sender, instance, **kwargs):

    comment = instance
    post = comment.post
    parent = comment.parent

    if parent is None:

        who_commented_before = Comment.objects \
            .filter(post=post) \
            .filter(parent=None) \
            .exclude(name=comment.name) \
            .order_by('-created') \
            .distinct()

        how_many_users = len(who_commented_before)

        if how_many_users == 0:
            Notification.objects.filter(category='comment', post=post).delete()

        elif how_many_users > 0:
            notification = Notification.objects.filter(category='comment', post=post)[0]
            previous_sender = who_commented_before[0].name

            if how_many_users == 1:

                notification.sender = previous_sender
                notification.notify_text = f'{previous_sender.name} commented on your post.'
                notification.notify_text_zhhant = f'{previous_sender.name}在你的文章上留言'
                notification.save()

            else:
                how_many_users = how_many_users - 1
                notification.sender = previous_sender
                notification.notify_text = f'{previous_sender.name} and other {how_many_users}commented on your post.'
                notification.notify_text_zhhant = f'{previous_sender.name}和另外{how_many_users}在你的文章上留言'
                notification.save()

        else:
            pass

    else:
        who_commented_before = Comment.objects \
            .filter(parent=parent) \
            .exclude(name=comment.name) \
            .order_by('-created') \
            .distinct()

        how_many_users = len(who_commented_before)

        if how_many_users == 0:
            Notification.objects.filter(category='comment', comment=comment).delete()

        elif how_many_users > 0:
            notification = Notification.objects.filter(category='comment', comment=comment)[0]
            previous_sender = who_commented_before[0].name

            if how_many_users == 1:

                notification.sender = previous_sender
                notification.notify_text = f'{previous_sender.name} replied to your comment.'
                notification.notify_text_zhhant = f'{previous_sender.name}回覆了你的留言'
                notification.save()

            else:
                how_many_users = how_many_users - 1
                notification.sender = previous_sender
                notification.notify_text = f'{previous_sender.name} and other {how_many_users} replied to your comment.'
                notification.notify_text_zhhant = f'{previous_sender.name}和另外{how_many_users}回覆了你的留言'
                notification.save()

        else:
            pass


post_save.connect(new_comment, sender=Comment)
post_save.connect(new_like, sender=Like)
post_save.connect(new_user, sender=Account)
post_save.connect(new_follow, sender=Follow)

pre_delete.connect(delete_like, sender=Like)
pre_delete.connect(delete_comment, sender=Comment)
