from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import BlogPost
from .forms import SignUpForm

# Create your views here.

class BlogPostListView(LoginRequiredMixin, ListView):
    model = BlogPost
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        # Show all approved posts on the home page
        return BlogPost.objects.filter(is_approved=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add a flag to indicate if the user is viewing their own posts
        context['viewing_my_posts'] = False
        return context

class BlogPostDetailView(LoginRequiredMixin, DetailView):
    model = BlogPost
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        # Allow viewing all approved posts
        return BlogPost.objects.filter(is_approved=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        # Add flag to check if user can edit/delete the post
        context['can_edit'] = self.request.user == post.author or self.request.user.is_superuser
        context['related_posts'] = BlogPost.objects.filter(is_approved=True).exclude(pk=post.pk)[:3]
        return context

class BlogPostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    template_name = 'blog/post_form.html'
    fields = ['title', 'description', 'content', 'image']
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.is_approved = False
        messages.success(self.request, 'Your post has been submitted for approval.')
        return super().form_valid(form)

class BlogPostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    template_name = 'blog/post_form.html'
    fields = ['title', 'description', 'content', 'image']
    success_url = reverse_lazy('blog:post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_superuser

class BlogPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_superuser

class PendingPostsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = BlogPost
    template_name = 'blog/pending_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_superuser

    def get_queryset(self):
        return BlogPost.objects.filter(is_approved=False)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def approve_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    post.is_approved = True
    post.save()
    messages.success(request, f'Post "{post.title}" has been approved.')
    return redirect('blog:pending_posts')

class SignUpView(FormView):
    template_name = 'registration/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Account created successfully! Please log in.')
        return super().form_valid(form)

class MyPostsView(LoginRequiredMixin, ListView):
    model = BlogPost
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        return BlogPost.objects.filter(author=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['viewing_my_posts'] = True
        return context
