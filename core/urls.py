from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('portfolio/resume/', views.download_resume, name='resume'),
    path('portfolio/contact/', views.contact, name='contact'),
    path('portfolio/', views.portfolio, name='portfolio')
]