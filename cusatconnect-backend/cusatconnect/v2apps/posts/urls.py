from django.urls import path
from .views import PostView, CommentView, PostImageView, LikeGetView, LikeAddView


urlpatterns = [
    path('users/posts-image/', PostImageView.as_view(), name="post-image-upload"),
    path('users/posts/', PostView.as_view(), name="post-upload"),
    path('users/comment-add/', CommentView.as_view(), name="comment-add"),
    path('users/vote-get/<int:pk>/', LikeGetView.as_view(), name="like-get"),
    path('users/vote-add/', LikeAddView.as_view(), name="vote-add"),

]
