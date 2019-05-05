from django.urls import path
from . import views

urlpatterns = [
    path('comment/post/<int:blog_pk>',views.blog_comment,name='blog_comment')
]