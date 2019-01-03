from django.urls import path, re_path
from article import views
from django.conf import settings
from django.conf.urls.static import static


app_name = "article"
urlpatterns = [
    re_path('^article_column/$', views.article_column, name='article_column'),
    re_path('^article_column/(?P<pk>[0-9]+)/$', views.edit_article_column, name='edit_article_column'),
    re_path('^del_article_column/(?P<pk>[0-9]+)/$', views.del_article_column, name='del_article_column'),
    re_path('^article_post/$', views.article_post, name='article_post'),
    re_path('^article_list/$', views.article_list, name='article_list'),
    re_path('^posts/$', views.post_list, name='posts'),
    re_path('^posts_class/$', views.PostListNew.as_view(), name='posts_class'),
    re_path('^post_list/(?P<author>[\w+.])/$', views.PostListNew.as_view(), name='author_posts'),
    re_path('^detail_class/(?P<pk>[0-9]+)/(?P<slug>[\w-]+)/$', views.PostDetailNew.as_view(), name='detail_class'),
    re_path('^article_detail/(?P<pk>[0-9]+)/(?P<slug>[\w-]+)/$', views.article_detail, name='article_detail'),
    re_path('^article_post/(?P<pk>[0-9]+)$', views.edit_article_post, name='edit_article_post'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
