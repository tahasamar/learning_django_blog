from IPython.core.inputsplitter import comment_line_re
from django.shortcuts import render, get_object_or_404


from .models import Post
from django.db.models import Count
from .forms import PostCommentForm

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
    if request.method == "POST":
        comment_form = PostCommentForm(request.POST)
        if comment_form.is_valid():
            comment_model = comment_form.save(commit=False)
            comment_model.post = post
            comment_model.save()


    comment_form = PostCommentForm()

    context = {
        'post': post,
        'comment_form': comment_form
    }

    return render(request, "blogApp/post_detail.html", context)
