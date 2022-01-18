from dataclasses import fields
from django import forms
from .models import Comment, Post
from ckeditor.fields import RichTextField
from datetime import date

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                'class': 'w-full border rounded p-2 outline-none',
                'placeholder': 'Add a comment...',
                'rows': '3',
                'id': 'comment'                
            }
        )
    )
    
    class Meta:
        model = Comment
        fields = ['content',]
        
class PostForm(forms.ModelForm):
    title = forms.CharField(
        label="Title",
        widget=forms.TextInput(
            attrs={
                'class': 'w-full border rounded p-1 outline-none'
            }
        ), 
        required=True, 
        max_length=100
    )
    meta_title=forms.CharField(
        label="Meta Title",
        widget=forms.TextInput(
            attrs={
                'class': 'w-full border rounded p-1 outline-none'
            }
        ), 
        required=True, 
        max_length=100
    )
    slug = forms.CharField(
        label="Slug",
        widget=forms.TextInput(
            attrs={
                'class': 'w-full border rounded p-1 outline-none'
            }
        ),
        required=True,
        max_length=50
    )
    summary = forms.CharField(
        label="Summary",
        widget = forms.Textarea(
             attrs={
                'class': 'w-full border rounded p-2 outline-none',
                'placeholder': 'Add a summary...',
                'rows': '3'
            }  
        ), 
        required=True
    )
    content = RichTextField()
    
    def save(self, user=None):
        post = super(PostForm, self).save(commit=False)
        if user and post:
            post.published = True
            post.author = user
            post.pub_date = date.today()
        post.save()
        return post
    
    class Meta:
        model = Post
        fields = ['title', 'meta_title', 'slug', 'summary', 'content']