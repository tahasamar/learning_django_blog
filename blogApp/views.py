from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormView
from django.urls import reverse
from .models import Post
from .forms import PostCommentForm

class FirstPageView(TemplateView):
    template_name = "blogApp/firstPage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts_count'] = Post.objects.all().count()
        context['latest_posts'] = Post.objects.all().order_by('-created_at')[:3]
        context['seen_posts'] = self.request.session.get('seen_posts', [])
        return context


class PostListView(ListView):
    template_name = "blogApp/post_list.html"
    model = Post
    context_object_name = 'posts'
    paginate_by = 10




class PostDetailView(DetailView, FormView):
    template_name = "blogApp/post_detail.html"
    model = Post
    context_object_name = 'post'
    form_class = PostCommentForm

    def post(self, request, *args, **kwargs): # a wired bug shows up if I don't write this.
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("post_detail", args=[self.get_object().slug])

    def form_valid(self, form):
        form_model = form.save(commit=False)
        form_model.post = self.get_object()
        form_model.save()

        return super().form_valid(form)

    def get(self,request,*args,**kwargs):
        self.object = self.get_object()

        if not request.session.get('seen_posts'):
            request.session['seen_posts'] = [self.object.slug]

        else:
            if not self.object.slug in request.session.get('seen_posts'):
                request.session['seen_posts'].append(self.object.slug)
                print(request.session['seen_posts'])
                request.session.save()

        return super().get(request,*args,**kwargs)