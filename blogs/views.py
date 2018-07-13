from django.http import HttpResponse
from django.shortcuts import render
from . import models

def index(request):
	blogs = models.Blog.objects.all()
	return render(request, 'blogs/index.html', {'blogs': blogs})


def blog(request,blog_id):
	blog = models.Blog.objects.get(pk=blog_id)
	return render(request, 'blogs/post_detail.html', {'blog': blog})