from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('myblogs/', views.myblogs, name='myblogs'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    # -----------BLOG----------------------
    path('create_blog/', views.create_blog, name='create_blog'),
    path('blog/<int:blog_id>/', views.blog, name='blog' ),
    path('blog/<int:blog_id>/create_post/', views.create_post, name='create_post'),
    path('edit_blog/<int:blog_id>/',views.edit_blog, name='edit_blog'),
    path('delete_blog/<int:blog_id>/', views.delete_blog, name='delete_blog'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('post/<int:post_id>/', views.read_post, name='read_post'),


]
