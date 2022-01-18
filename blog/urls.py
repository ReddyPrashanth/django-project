from django.urls import path, include

from . import views

# Blog application URLs

app_name = 'blog'

urlpatterns = [
    path('add/', views.AddPostView.as_view(), name="add_post"),
    path('', views.PostListView.as_view(), name='index'),
    path('api/', include('blog.api.urls')),
    path('<int:pk>/delete', views.PostDeleteView.as_view(), name='delete'),
    path('<int:pk>/update', views.PostUpdateView.as_view(), name='update'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='detail')
]