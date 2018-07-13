from django.http import HttpResponse
from django.shortcuts import render
from . import models

def index(request):
	blogs = models.Blog.objects.all()
	return render(request, 'blogs/index.html', {'blogs': blogs})