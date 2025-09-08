from django.contrib import admin
from django.urls import path
from .views import index, resume, projects, contact, details

app_name = 'main'
urlpatterns = [
    path('', index, name='index'),
    path('resume/', resume, name='resume'),
    path('projects/', projects, name='projects'),
    path('contact/', contact, name='contact'),
    path('projects/<str:content>/', details, name='details'),
]
