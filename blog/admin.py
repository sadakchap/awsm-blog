from django.contrib import admin
from .models import Post,Comment
# Register your models here.

class CommentInline(admin.StackedInline):
	model = Comment
	extra = 2

class PostAdmin(admin.ModelAdmin):
	list_display = ('title','slug','author','publish','feature')
	prepopulated_fields = {'slug':('title',)}
	search_fields = ('title',)
	list_filter   = ('publish','feature',)
	date_hierarchy	=	'publish'
	inlines = [CommentInline,]

admin.site.register(Post,PostAdmin)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('name','email','post','created','active')
	list_filter  = ('active','created','updated')
	search_fields = ('name','email','text')