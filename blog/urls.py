from django.contrib import admin
from django.urls import path, include, re_path
from blog import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "blog"
urlpatterns = [
    re_path('title/(?P<article_id>[\\d]+)', views.blog_article, name='blog_detail'),
    path('', views.blog_title, name='blog_titles'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
