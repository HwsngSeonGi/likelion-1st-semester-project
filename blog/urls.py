from django.contrib import admin
from django.urls import path
from django.conf import settings
from . import views


urlpatterns = [

    path('post/<int:post_id>', views.detail, name = 'detail'),
    path('new/', views.new, name='new'),
    path('create/', views.create, name="create"),
    path('update/<int:post_id>/', views.update, name='update'),
    path('modify/<int:post_id>/', views.modify, name='modify'),
    path('comment_write/<int:post_pk>/', views.comment_write, name="comment_write" ),
    path('delete/<int:post_id>', views.delete, name = 'delete'),
    path('delete1/<int:post_id>/<int:comment_id>', views.delete1, name = 'delete1'),
    path('newpost', views.newpost, name= "newpost"),
    path('updatemodify/<int:post_id>', views.updatemodify, name="updatemodify"),
    path('like/<int:post_id>/', views.post_like, name='post_like'),
]