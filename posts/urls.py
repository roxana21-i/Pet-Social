from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostList.as_view(), name='all'),
    path('new/<group_slug>/', views.CreatePost.as_view(), name='create'),
    path('by/<username>/', views.UserPosts.as_view(), name='for_user'),
    path('by/<username>/change_picture/', views.update_profile_picture, name='change_picture'),
    path('by/<username>/<int:pk>/', views.PostDetail.as_view(), name='single'),
    path('by/<username>/<int:pk>/like', views.add_like_to_post, name='add_like'),
    path('by/<username>/<int:post_pk>/like/remove/<int:like_pk>/', views.remove_like_from_post, name='remove_like'),
    path('by/<username>/<int:pk>/comment/', views.CommentForm.as_view(), name='comment'),
    path('by/<username>/<int:post_pk>/comment/<int:comment_pk>/reply', views.ReplyForm.as_view(), name='reply'),
    path('delete/<int:pk>/', views.DeletePost.as_view(), name='delete'),
]
