from django.urls import path, include

from . import views

# Blog application URLs

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('add/', views.AddPostView.as_view(), name="add_post"),
    path('api/', include('blog.api.urls')),
    path('<int:pk>', views.PostDetailView.as_view(), name='detail')
]