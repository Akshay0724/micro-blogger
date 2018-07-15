from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import markdown

from . import forms, models


def index(request):
    blogs = models.Blog.objects.all()
    return render(request, 'blogs/index.html', {'blogs': blogs})


def blog_detail(request, blog_id):
    blog = models.Blog.objects.get(pk=blog_id)
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


def show_markdown(request):
    if request.method == 'POST':
        saved = request.POST['content']
        extensions = ['pymdownx.extra', 'pymdownx.emoji', 'pymdownx.progressbar', 'pymdownx.magiclink', 'pymdownx.mark',
                      'pymdownx.keys', 'pymdownx.smartsymbols', 'pymdownx.superfences', 'pymdownx.highlight',
                      'pymdownx.tasklist', 'pymdownx.details']
        content = markdown.markdown(saved, extensions)
        return render(request, 'blogs/md.html', {
            'content': content,
            'saved': saved
        })
    return render(request, 'blogs/md.html')
