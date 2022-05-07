import imp
from django.db import models
from django.db.models.fields import IntegerField
from django.utils import timezone
from django.urls import reverse
from account.models import Account
from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
import secrets


class CustomTag(TagBase):
    slug = models.SlugField(verbose_name=_('slug'), unique=True, max_length=100, allow_unicode=True)

    def slugify(self, tag, i=None):
        slug = slugify(tag, allow_unicode=True)
        if i is not None:
            slug += '_%d' % i
        return slug

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'
        app_label = 'taggit'


class TaggedWhatever(GenericTaggedItemBase):

    tag = models.ForeignKey(
        CustomTag,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_items',
    )


def random_slug():
    return secrets.token_urlsafe(8)


class Post(models.Model):

    STATUS_CHOICES = (
        ('draft', _('Draft')),
        ('published', _('Published')),
    )

    publish_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    cover_image = models.ImageField(
        upload_to='cover_photos/',
        default='cover_photos/default_cover.jpg',
    )
    description = models.TextField(max_length=100)
    body = CKEditor5Field(config_name='default')
    slug = models.SlugField(
        max_length=255,
        unique=True,
        default=random_slug,
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='Draft'
    )
    post_views = IntegerField(default=0)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    tags = TaggableManager(through=TaggedWhatever)

    class Meta:
        ordering = ('-publish_date', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article:post_page', args=[self.slug])


class Comment(models.Model):

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='post_comments'
    )
    name = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    comment_body = models.TextField('Comment')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    parent = models.ForeignKey(
        'Comment',
        on_delete=models.CASCADE,
        related_name="replies",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ('created', )

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'


class Like(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True,)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True,)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'post', 'comment'),)


class Bookmark(models.Model):

    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'post'),)


class Follow(models.Model):
    """
    user is who click the follow button.
    following are who the user is following.
    """
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='following')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'following'),)
