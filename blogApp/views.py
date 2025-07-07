from django.shortcuts import render, get_object_or_404
from .models import Post

def firstPage(request):
    latest_posts = Post.objects.order_by('-created_at')[:3]
    context = {
        'latest_posts': latest_posts
    }
    return render(request, "blogApp/firstPage.html", context)

def post_list(request):
    posts = Post.objects.order_by('-created_at')
    context = {
        'posts': posts
    }
    return render(request, "blogApp/post_list.html", context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {
        'post': post
    }
    return render(request, "blogApp/post_detail.html", context)
