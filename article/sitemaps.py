from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):

    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return Post.objects.filter(status='published')

    def lastmode(self, obj):
        return obj.modified_date
