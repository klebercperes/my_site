from django.urls import path

from . import views

urlpatterns = [
    path("", views.StartingPageView.as_view(), name="starting-page"),
    path("posts/", views.AllPostsView.as_view(), name="posts-page"),
    path("posts/<slug:slug>", views.SinglePostView.as_view(), name="post-detail-page"),
    path("read-later", views.ReadLaterView.as_view(), name="read-later"),
    path("stored-posts", views.StoredPostsView.as_view(), name="stored-posts"),
    path("posts/<slug:slug>/delete-comment/<int:comment_id>", views.delete_comment, name="delete-comment"),
]
