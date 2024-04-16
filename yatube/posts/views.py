from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PostForm
from .models import Post, Group
from django.core.paginator import Paginator
from django import forms


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = 'YaTube'
    posts = Post.objects.order_by('-pub_date')[:10]
    context = {'title': title,
               'text': 'Главная страница проекта YaTube',
               'posts': posts,
               'page_obj': page_obj,
               }
    template = 'posts/index.html'
    return render(request, 'posts/index.html', context)




def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    group_list = Post.objects.filter(group=group).order_by('-pub_date')
    paginator = Paginator(group_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    context = {
        'group': group,
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)

def profile(request, username):
    count = Post.objects.filter(author__username=username).count()
    user_posts = Post.objects.filter(author__username=username).order_by('-pub_date')
    context = {
        'username': username,
        'user_posts': user_posts,
        'count': count,
    }
    return render(request, 'posts/profile.html', context)

def post_detail(request, post_id):
    post_id = get_object_or_404(Post, pk=post_id)
    context = {
        'post_id': post_id,
    }
    return render(request, 'posts/post_detail.html', context)

def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', request.user)
    context = {
        "form": form,
    }
    return render(request, "posts/create_post.html", context)

def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author == request.user:
        form = PostForm(request.POST or None, instance=post)
        if form.is_valid():
            post.save()
            return redirect('posts:post_detail', post_id)
        context = {
            "form": form,
        }
        return render(request, "posts/create_post.html", context)
    return redirect('posts:post_detail', post_id)