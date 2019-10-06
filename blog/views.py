from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.views.generic import TemplateView
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.core.mail import send_mail
from django.db.models import Count

from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank
from taggit.models import Tag

from .models import Post
from .forms import PostEmailForm,CommentForm,SearchForm

def post_list(req,tag_slug=None):
	object_list = Post.published.all()
	tag = None

	if tag_slug:
		 tag = get_object_or_404(Tag,slug=tag_slug)
		 object_list = Post.published.filter(tags__in=[tag])

	paginator = Paginator(object_list,4)
	page = req.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)
	context = {
		'posts':posts,
		'page':page,
		'tag':tag
	}
	return render(req,'blog/post_list.html',context)


def post_detail(req,slug):
	post = get_object_or_404(Post,slug=slug)
	comments = post.comments.filter(active=True)
	form = CommentForm(req.POST or None)
	if form.is_valid():
		comment = form.save(commit=False)
		comment.post = post 
		comment.save()
		messages.info(req,"Your Comment has been Added!")
		return redirect("blog:post-detail",slug=post.slug)
	
	tags = post.tags.values_list('id',flat=True)
	similar_posts = Post.published.filter(tags__in=tags).exclude(id=post.id)
	similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

	context = {
		'post':post,
		'comments':comments,
		'comment_form':form,
		'similar_posts':similar_posts
	}
	return render(req,'blog/post_detail.html',context)

class AboutPage(TemplateView):
	template_name = 'about.html'

def share_post(req,slug):
	post = get_object_or_404(Post,slug=slug)
	form = PostEmailForm(req.POST or None)
	if form.is_valid():
		email = form.cleaned_data.get('email')
		to	  = form.cleaned_data.get('to')
		name  = form.cleaned_data.get('name')
		comment = form.cleaned_data.get('comment')
		post_url = req.build_absolute_uri(post.get_absolute_url())
		subject  = '{} ({}) recommends you reading {}'.format(name,email,post.title)
		body = 'Read "{}" at {} \n\n {}\'s comments: {}'.format(post.title,post_url,name,comment)
		
		send_mail(subject,body,email,[to])
		msg = 'A "{}" share link has been successfully emailed to {}'.format(post.title,to)
		messages.success(req,msg)
		return redirect('blog:share',post.slug)

	context = {
		'form':form,
		'post':post
	}

	return render(req,'blog/share_post.html',context)


def post_search(req):
	form = SearchForm()
	query = None
	res = []
	if 'query' in req.GET:
		form = SearchForm(req.GET)
		if form.is_valid():
			query = form.cleaned_data.get('query')
			search_vector = SearchVector('title',weight='A') + SearchVector('body',weight='B')
			search_query  = SearchQuery(query)
			res += Post.published.annotate(
				rank=SearchRank(search_vector,search_query)).filter(rank__gte=0.3).order_by('-rank','-publish')
			
			res	+= Post.published.annotate(
					similarity=TrigramSimilarity(
						'title',query)).filter(similarity__gt=0.3).order_by('-similarity')
			res = set(res)
	return render(req,'blog/post_search.html',{'form':form,'res':res,'query':query})