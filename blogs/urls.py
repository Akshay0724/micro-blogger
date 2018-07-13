from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('blogs/<int:blog_id>', views.blog, name='post_detail'),
]