from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormView
from django.urls import reverse
from .models import Post, Admin
from .forms import PostCommentForm, LoginForm, SignUpForm

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
    paginate_by = 12




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


class LoginView(FormView):
    template_name = 'blogApp/login.html'
    form_class = LoginForm
    success_url = '/'

    def get(self,request,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.success_url)
        return super().get(request,*args,**kwargs)

    def form_valid(self, form):
        user = authenticate(self.request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(self.request,user)
            return super().form_valid(form)
        else:
            form.add_error(None , "نام کاربری یا رمزعبور صحیح نیست")
            return super().form_invalid(form)


class LogoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('/')


class SignUpView(FormView):
    template_name = 'blogApp/signup.html'
    form_class = SignUpForm
    success_url = '/'

    def form_valid(self, form):
        if Admin.objects.get(username=form.cleaned_data['username']).is_active:
            form.add_error('username','نام کاربری تکراری است')
            return super().form_invalid(form)
        user=Admin.objects.create_user(form.cleaned_data['username'], "", form.cleaned_data['password'])
        login(self.request,user )
        return super().form_valid(form)


