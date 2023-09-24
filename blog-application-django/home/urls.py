from django.urls import path
from . import views
from .views import UpdatePostView

urlpatterns = [
    #     blogs
    path("", views.blogs, name="blogs"),
    path("blog/<str:slug>/<str:post_id>", views.blogs_comments, name="blogs_comments"),
    path("add_blogs/", views.add_blogs, name="add_blogs"),
    path("edit_blog_post/<str:slug>/", UpdatePostView.as_view(), name="edit_blog_post"),
    path("like_dislike/<str:post_id>/<str:is_like>", views.like_dislike, name="like_dislike"),
    path("delete_blog_post/<str:slug>/", views.Delete_Blog_Post, name="delete_blog_post"),
    path("search/", views.search, name="search"),
    path("like_dislike/", views.like_dislike, name="like_dislike"),

    # admin
    path("adminlogin/", views.adminlogin, name="adminlogin"),
    path("adminmainpage/", views.adminmainpage, name="adminmainpage"),
    path("adminviewusers/", views.adminviewusers, name="adminviewusers"),
    path("adminviewblogs/", views.adminviewblogs, name="adminviewblogs"),
    path("adminviewlikes_unlikes/", views.adminviewlikes_unlikes, name="adminviewlikes_unlikes"),
    path("adminaccept_rejectblogs/", views.adminaccept_rejectblogs, name="adminaccept_rejectblogs"),
    path("accept_rejectblogs/<str:id>/<str:status>", views.accept_rejectblogs, name="adminaccept_rejectblogs"),

    #profile
    path("profile/", views.UserProfile, name="profile"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("user_profile/<int:myid>/", views.user_profile, name="user_profile"),
    path('userforgotpassword/', views.userforgotpassword),
    path('generateotppage/', views.generateotppage),
    path('enterotppage/', views.enterotppage),
    path('passwordchangepage/', views.passwordchangepage),

    #user authentication
    path("register/", views.Register, name="register"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),
]
