from django.urls import path
from . import views
from .feeds import LatestPostFeed


app_name = 'blog'

urlpatterns = [
	path('',views.post_list,name='post-list'),
	path('tag/<slug:tag_slug>/',views.post_list,name='post-list-tag'),
	path('detail/<slug:slug>/',views.post_detail,name='post-detail'),
	path('share/<slug:slug>/',views.share_post,name='share'),
	path('feed/',LatestPostFeed(),name='post_feed'),
	path('search/',views.post_search,name='search'),
	
]
