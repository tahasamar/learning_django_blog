from django.shortcuts import render, get_object_or_404
from .models import Post
from django.db.models import Count

def firstPage(request):
    latest_posts = Post.objects.order_by('-created_at')[:3]
    context = {
        'posts_count': Post.objects.all().aggregate(Count('id'))['id__count'],
        'latest_posts': latest_posts
    }
    return render(request, "blogApp/firstPage.html", context)

def post_list(request):
    posts = Post.objects.order_by('-created_at')
    context = {
        'posts': posts
    }
    return render(request, "blogApp/post_list.html", context)

def post_detail(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    context = {
        'post': post
    }
    return render(request, "blogApp/post_detail.html", context)
