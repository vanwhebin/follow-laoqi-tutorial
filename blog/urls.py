from django.contrib import admin
from django.urls import path, include, re_path
from blog import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "blog"
urlpatterns = [
    path('<str:slug>', views.blog_article, name='blog_detail'),
    path('comment/<str:slug>', views.comment_article, name='post_comment'),
    path('', views.blog_list, name='blog_list'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
