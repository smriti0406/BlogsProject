from django.urls import path
from django.contrib.auth import views as auth_views
from . import views as user_views

app_name = 'BlogsBook'
urlpatterns = [
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='BlogsBook/login.html'), name='user-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='BlogsBook/logout.html'), name='user-logout'),
    path('', user_views.home, name='home'),
    path('Add_blog/', user_views.add_blog, name='add-blog'),
    path('View_blog/<int:blog_id>/', user_views.viewblog, name='view-blog'),
    path('View_blog/<int:blog_id>/delete/', user_views.deleteblog, name='delete-blog'),
    path('View_blog/<int:blog_id>/update/', user_views.updateblog, name='update-blog'),
    path('View_user/<int:user_id>/', user_views.viewuser, name='view-user'),
    path('View_user/edit/', user_views.edituser, name='edit-user'),
    path('reset_password/', user_views.passwordrest, name='reset-password'),
    path('View_blog/<int:blog_id>/delete_comment/<int:comment_id>/', user_views.commentdelete, name='delete-comment'),
    path('delete_user/', user_views.delete_user, name='delete-user'),
    path('search/category/', user_views.searchcategory, name='category-search'),
    path('search/category/query=<str:query>/', user_views.searchcatname, name='category-query'),
    path('search/user/', user_views.searchuser, name='user-search'),
    path('search/user/query=<str:query>/', user_views.userquery, name='user-query'),
]