from django.urls import path
from . import views

urlpatterns = [
    path('comment/<int:comment_id>/reply', views.post, name='reply'),
    path('post/<int:post_id>/like', views.like_a_post, name="like_dislike")
]
