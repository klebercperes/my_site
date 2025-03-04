from django.shortcuts import render
from .models import Post # Import your Post model


# Create your views here.

def starting_page(request):
    return render(request, "blog/index.html")

def posts(request):
    posts = Post.objects.all() #Fetch all posts from the database
    return render(request, "blog/all-posts.html", {"posts":posts}) #Pass posts to template.

def post_detail(request):
    return render(request, "blog/post-detail.html")

