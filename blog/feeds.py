from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post

class LatestPostFeed(Feed):
	title = 'my_blog'
	link  = '/'
	description = 'New posts of my blog'

	def items(self):
		return Post.published.order_by('-publish')[:5]

	def item_title(self,item):
		return item.title

	def item_description(self,item):
		return truncatewords(item.body,30)