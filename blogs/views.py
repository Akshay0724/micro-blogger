from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from . import forms, models
from .templatetags import markdown


def index(request):
    blogs = models.Blog.objects.all()
    return render(request, 'blogs/index.html', {'blogs': blogs})


def blog_detail(request, blog_id):
    blog = get_object_or_404(models.Blog, pk=blog_id)
    return render(request, 'blogs/blog_detail.html', {'blog': blog})


def register(request):
    if request.method == 'POST':
        form = forms.UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Successfully Registered')
            return redirect('index')
    else:
        form = forms.UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def create_blog(request):
    if request.method == 'POST':
        form = forms.BlogForm(request.POST)

        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            messages.success(request, 'Blog successfully created')
            return redirect('index')
    else:
        form = forms.BlogForm()

    return render(request, 'blogs/create.html', {'form': form})


def render_markdown(request):
    md = request.POST.get('md', '')
    response = markdown.markdown(md)
    print(response)
    return HttpResponse(response)
