from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('new', views.create_blog, name='create_blog'),
    path('blogs/<int:blog_id>', views.blog_detail, name='post_detail'),
]
