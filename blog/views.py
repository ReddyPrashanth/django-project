from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from .forms import CommentForm, PostForm
from django.views.generic.edit import FormMixin

# Post related generic views

# Add post generic view
class AddPostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name= 'blog/add_post.html'
    login_url = '/account/login'
        
    def get_success_url(self):
        return reverse('blog:index')
        
    def form_valid(self, form):
        form.save(self.request.user)
        return super(AddPostView, self).form_valid(form)

# List post generic view
class PostListView(LoginRequiredMixin, ListView):
    template_name = 'blog/index.html'
    paginate_by = 5
    model = Post
    login_url = '/account/login'
    
    def get_queryset(self):
        """Return last five published questions."""
        return Post.objects.order_by('-pub_date').values('id', 'title', 'content', 'author_id')

# Detail post generic view
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

# Delete post generic view
class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')

# Update post generic view
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name= 'blog/add_post.html'
    login_url = '/account/login'
    success_url = reverse_lazy('blog:index')
        
    def get_object(self, *args, **kwargs):
        post = get_object_or_404(self.model, pk = self.kwargs['pk'])
        return post