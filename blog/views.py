from django.urls import reverse
from django.http import HttpResponseForbidden
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from .forms import CommentForm, PostForm
from django.views.generic.edit import FormMixin
from datetime import date
# Create your views here.

class AddPostView(LoginRequiredMixin, FormMixin, ListView):
    model = Post
    form_class = PostForm
    template_name= 'blog/add_post.html'
    login_url = '/account/login'
    
    def get_success_url(self):
        return reverse('blog:index', kwargs={'pk': self.object.pk})
    
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def form_valid(self, form, user):
        post = form.save(commit=False)
        post.published = True
        post.pub_date = date.today()
        post.save()
        return super().form_valid(form)

class PostListView(AddPostView):
    template_name = 'blog/index.html'
    paginate_by = 5
    model = Post
    login_url = '/account/login'
    
    def get_queryset(self):
        """Return last five published questions."""
        return Post.objects.order_by('-pub_date').values('id', 'title', 'content')

class PostDetailView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = 'blog/detail.html'
    model = Post
    login_url = '/account/login'
    form_class = CommentForm
    
    def get_success_url(self):
        return reverse('blog:detail', kwargs={'pk': self.object.pk})
    
    def get_queryset(self):
        return Post.objects.prefetch_related('likes')
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form, request.user)
        else:
            return self.form_invalid(form)
        
    def form_valid(self, form, user):
        comment = form.save(commit=False)
        comment.user = user
        comment.post = self.object
        comment.save()
        return super().form_valid(form)