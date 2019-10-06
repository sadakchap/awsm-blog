from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.

class PublishManager(models.Manager):
	def get_queryset(self):
		return super(PublishManager,self).get_queryset().filter(feature=True)


class Post(models.Model):
	title		= models.CharField(max_length=255)
	slug		= models.SlugField(max_length=255,unique_for_date='publish')
	image		= models.ImageField(upload_to='blog_pics/',default='default.jpg')
	author		= models.ForeignKey(User,on_delete=models.CASCADE,related_name='bog_posts')	
	body		= models.TextField()
	publish		= models.DateTimeField(default=timezone.now)	
	created		= models.DateTimeField(auto_now_add=True)
	updated		= models.DateTimeField(auto_now=True)
	feature		= models.BooleanField(default=False)
	tags		= TaggableManager()

	#need to specify both 
	objects		= models.Manager()  #the default manager
	published	= PublishManager() # our manager

	class Meta:
		ordering = ('-publish',)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog:post-detail',kwargs={'slug':self.slug})


class Comment(models.Model):
	post 		= models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
	name		= models.CharField(max_length=255)
	email 		= models.EmailField(max_length=255)
	text 		= models.TextField()
	created		= models.DateTimeField(auto_now_add=True)
	updated		= models.DateTimeField(auto_now=True)
	active		= models.BooleanField(default=True)

	class Meta:
		ordering = ('-created',)

	def __str__(self):
		return 'Comment by {} on {}'.format(self.name,self.post)