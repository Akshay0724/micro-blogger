import json

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

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


@login_required
def edit_blog(request, blog_id):
    blog = get_object_or_404(models.Blog, pk=blog_id)
    if blog.user.id != request.user.id:
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        form = forms.BlogForm(request.POST)

        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            messages.success(request, 'Blog successfully updated')
            return redirect('post_detail', blog_id=blog.id)
    else:
        form = forms.BlogForm(instance=blog)
    
    return render(request, 'blogs/create.html', {'form': form, 'edit': True})


@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(models.Blog, pk=blog_id)
    if blog.user.id != request.user.id:
        return HttpResponse('Unauthorized', status=401)
    blog.delete()
    messages.success(request, 'Blog successfully deleted')
    return redirect(reverse('index'))

def render_markdown(request):
    md = request.POST.get('md', '')
    print(md)
    response = markdown.markdown(md)
    print(response)
    return HttpResponse(response)


@login_required
def create_comment(request, blog_id):
    if request.method == 'POST':
        blog = models.Blog.objects.get(pk=blog_id)
        if not blog:
            return HttpResponse(json.dumps({
                'success': False,
                'message': "Blog {} not found".format(blog_id)
            }))
        user = request.user
        content = request.POST.get('content', None)
        if not content or content.strip() == '':
            return HttpResponse(json.dumps({
                'success': False,
                'message': 'Content must not be empty'
            }))
        comment = models.Comment.objects.create(
            content=content,
            blog=blog,
            user=user
        )

        comment_data = {
            'content': comment.content,
            'border_tag': comment.border_tag,
            'is_op': comment.user.id == blog.user.id,
            'created_at': comment.created_at.isoformat(),
            'updated_at': comment.updated_at.isoformat(),
            'user': {
                'username': comment.user.username,
                'first_name': comment.user.first_name,
                'last_name': comment.user.last_name,
                'full_name': comment.user.first_name + ' ' + comment.user.last_name
            }
        }

        return HttpResponse(json.dumps({
            'success': True,
            'message': 'Comment created successfully',
            'comment': comment_data
        }))
    return HttpResponse(json.dumps({
        'success': False,
        'message': 'Method not supported'
    }))
