from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name='account'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('account:login')), name='logout'),
    path('<int:user_id>/profile/', views.account, name='profile')
]
