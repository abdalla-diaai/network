from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.post, name="post"),
    path("allposts", views.allposts, name="allposts"),
    path("profile", views.profile, name="profile"),
    path("follow/<int:user_id>", views.follow, name="follow"),
    path("unfollow/<int:user_id>", views.unfollow, name="unfollow"),
    path("view_profile/<int:user_id>", views.view_profile, name="view_profile"),
    path("comment/<int:post_id>", views.comment, name="comment"),
    path("following", views.view_following, name="following"),
]
