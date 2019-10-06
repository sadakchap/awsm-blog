from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from blog.views import AboutPage

from blog.sitemaps import PostSitemap

sitemaps = {
	'posts': PostSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('blog.urls')),
    path('about/',AboutPage.as_view(),name='about'),
    path(
    		'sitemaps.xml',
    		sitemap,
    		{'sitemaps':sitemaps},
    		name='django.contrib.sitemaps.views.sitemap'
    	),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
