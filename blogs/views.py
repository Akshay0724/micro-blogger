from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from . import forms, models


def index(request):
    blogs = models.Blog.objects.all()
    return render(request, 'blogs/index.html', {'blogs': blogs})


def blog_detail(request, blog_id):
    blog = models.Blog.objects.get(pk=blog_id)
    return render(request, 'blogs/post_detail.html', {'blog': blog})


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
