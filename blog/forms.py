from django import forms
from .models import Comment

class PostEmailForm(forms.Form):
	name	= forms.CharField(max_length=255)
	email 	= forms.EmailField()
	to	 	= forms.EmailField()
	comment	= forms.CharField(required=False,widget=forms.Textarea)

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('name','email','text',)

class SearchForm(forms.Form):
	query = forms.CharField(max_length=355)