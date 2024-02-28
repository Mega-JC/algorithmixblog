from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("about", views.about, name="about"),
    path("discover", views.discover, name="discover"),
    path("search", views.search, name="search"),
    
    path("user/<int:user_id>/", views.user_profile, name="user_profile"),
    path("user/<int:user_id>/followers", views.user_followers, name="user_followers"),
    path("user/<int:user_id>/following", views.user_following, name="user_following"),
    path("blogpost/<int:blogpost_id>/", views.view_blogpost, name="view_blogpost"),
    path("blogpost/create", views.create_blogpost, name="create_blogpost"),
    path("blogpost/<int:blogpost_id>/edit", views.edit_blogpost, name="edit_blogpost"),
    path("feed/liked", views.liked_blogposts, name="liked_blogposts"),
    path("feed/following", views.following_feed_blogposts, name="following_feed_blogposts"),
    path("feed/favorites", views.favorite_blogposts, name="favorite_blogposts"),
    
    #path("algostructpost/<int:id>", views.algostructpost_view, name="algostructpost"),
    
    ## API Routes
    path("<int:blogpost_id>/toggleblogpostlike", views.toggle_blogpost_like, name="toggle_blogpost_like"),
    path("<int:blogpost_id>/toggleblogpostfavorites", views.toggle_blogpost_favorites, name="toggle_blogpost_favorites"),
    path("<int:blogpost_id>/toggleblogpostvisibility", views.toggle_blogpost_visibility, name="toggle_blogpost_visibility"),
    path("<int:blogpost_id>/blogpostdelete", views.blogpost_delete, name="blogpost_delete"),
    path("toggleblogpostcommentlike/<int:comment_id>", views.toggle_blogpost_comment_like, name="toggle_blogpost_comment_like"),
    path("blogpostcommentdelete/<int:comment_id>", views.blogpost_comment_delete, name="blogpost_comment_delete"),
    path("<int:user_id>/togglefollowuser", views.toggle_follow_user, name="toggle_follow_user"),
    path("<int:user_id>/deleteuser", views.user_delete, name="user_delete"),
    path("userspreview", views.users_preview, name="users_preview"),
    path("blogpostspreview", views.blogposts_preview, name="blogposts_preview"),
    path("blogpostspreview", views.blogposts_preview, name="blogposts_preview"),
    path("getblogpostcomment/<int:comment_id>", views.get_blogpost_comment, name="get_blogpost_comment"),
    path("getblogpostcomments", views.get_blogpost_comments, name="get_blogpost_comments"),
]
