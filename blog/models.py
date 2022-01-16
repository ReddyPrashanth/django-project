from dataclasses import fields
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from ckeditor.fields import RichTextField

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True)
    title = models.CharField(max_length=100)
    meta_title = models.CharField(max_length=100)
    slug = models.CharField(max_length=50)
    summary = models.TextField()
    published = models.BooleanField(default=False)
    pub_date = models.DateField(null=True)
    content = RichTextField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return self.title
    
    class Meta:
        indexes = [
            models.Index(fields=['author_id'], name='idx_author_id'),
            models.Index(['parent_id'], name='idx_parent_id')
        ]
        constraints = [
            models.UniqueConstraint(fields=['slug'], name='uq_slug'),
        ]

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    @property
    def reply_count(self):
        return self.reply_set.count()
    
    def __str__(self):
        return self.content
    
    class Meta:
        indexes = [
            models.Index(fields=['user_id'], name='idx_user_id'),
            models.Index(fields=['post_id'], name='idx_post_id')
        ]

class Reply(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.content
    
    class Meta:
        indexes = [
            models.Index(fields=['user_id'], name='idx_reply_user_id'),
            models.Index(fields=['comment_id'], name='idx_comment_id')
        ]
        
class Likedislike(models.Model):
    liked = models.BooleanField(default=False)
    disliked = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    
    def __str__(self):
        return "Liked : {} Disliked: {}".format(self.liked, self.disliked)
    
    class Meta:
        unique_together = ['user', 'post']
        indexes = [
            models.Index(fields=['user_id'], name="idx_like_user_id"),
            models.Index(fields=['post_id'], name='idx_like_post_id')
        ]