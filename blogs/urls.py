from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('new', views.create_blog, name='create_blog'),
    path('blogs/<int:blog_id>', views.blog_detail, name='post_detail'),
    path('api/markdown', views.render_markdown, name='render_markdown'),
    path('blogs/<int:blog_id>/comment', views.create_comment, name='create_comment'),
    path('blogs/<int:blog_id>/edit', views.edit_blog, name='edit_blog'),
]
