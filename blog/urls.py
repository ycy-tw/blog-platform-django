from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from article.sitemaps import PostSitemap


sitemaps = {
    'posts': PostSitemap,
}


urlpatterns = [
    # path('admin/', admin.site.urls),

    path('', include('article.urls')),
    path('account/', include('account.urls')),
    path('notification/', include('notification.urls')),

    # order is matter, 'upload' and 'browse' should be placed behind.

    # path('ckeditor/upload/', login_required(ckeditor_views.upload), name='ckeditor_upload'),
    # path('ckeditor/browse/', never_cache(login_required(ckeditor_views.browse)), name='ckeditor_browse'),
    # path('ckeditor', include('ckeditor_uploader.urls')),

    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('i18n/', include('django.conf.urls.i18n')),


    # solution for -> Not Found: /favicon.ico
    path('favicon.ico', RedirectView.as_view(url='/static/images/favicon.ico')),
    path(
        'sitemap.xml', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'article.views.handler404'
