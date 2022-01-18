from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserProfile
from .forms import UserProfileForm
from django.views.generic import UpdateView
# Create your views here.

class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'account/profile.html'
    model = UserProfile
    login_url = '/account/login'
    form_class = UserProfileForm
    
    def get_success_url(self):
        return reverse('account:profile', kwargs={'pk': self.object.pk})
    
    def get_object(self, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(pk=self.kwargs['pk'])
        except UserProfile.DoesNotExist:
            profile = UserProfile()
        return profile
    
    def form_valid(self, form):
        form.save(self.request.user)
        return super(ProfileView, self).form_valid(form)