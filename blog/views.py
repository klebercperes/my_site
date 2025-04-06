from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, SavedPost
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Post
from .forms import CommentForm


# Create your views here.

class StartingPageView(LoginRequiredMixin, ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"
    login_url = 'account_login'

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


class AllPostsView(LoginRequiredMixin, ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"
    login_url = 'account_login'


class SinglePostView(LoginRequiredMixin, DetailView):
    template_name = "blog/post-detail.html"
    model = Post
    context_object_name = "post"
    login_url = 'account_login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_tags"] = self.object.tags.all()
        context["comment_form"] = CommentForm()
        context["comments"] = self.object.comments.all().order_by("-id")
        context["is_saved"] = SavedPost.objects.filter(
            user=self.request.user,
            post=self.object
        ).exists()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = self.object
            comment.user = request.user
            comment.save()
            messages.success(request, "Your comment was added successfully!")
            return HttpResponseRedirect(reverse("post-detail-page", kwargs={"slug": self.object.slug}))
        
        context = self.get_context_data(**kwargs)
        context["comment_form"] = comment_form
        response = self.render_to_response(context)
        response['Location'] = f"{request.path}#error-message"
        return response
    
class ReadLaterView(LoginRequiredMixin, View):
    login_url = 'account_login'

    def post(self, request):
        post_id = request.POST.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        
        saved_post, created = SavedPost.objects.get_or_create(
            user=request.user,
            post=post
        )
        
        if not created:
            saved_post.delete()
            messages.success(request, "Post removed from your reading list!")
        else:
            messages.success(request, "Post added to your reading list!")
            
        return redirect("starting-page")    

class StoredPostsView(LoginRequiredMixin, ListView):
    template_name = "blog/stored-posts.html"
    model = SavedPost
    context_object_name = "saved_posts"
    login_url = 'account_login'

    def get_queryset(self):
        return SavedPost.objects.filter(user=self.request.user).select_related('post')

@login_required(login_url='account_login')
def delete_comment(request, slug, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user == request.user:
        comment.delete()
        messages.success(request, "Comment deleted successfully!")
        return redirect('post-detail-page', slug=slug)
    else:
        messages.error(request, "You can only delete your own comments!")
        return redirect('post-detail-page', slug=slug)    
