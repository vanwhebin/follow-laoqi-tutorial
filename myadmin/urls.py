from django.urls import path, re_path
from myadmin.views import views
from myadmin.views import blog
from django.conf import settings
from django.conf.urls.static import static

app_name = "myadmin"
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('blog/list/', blog.blog_list, name='blog_list'),
    path('blog/', blog.create_blog, name='create_blog'),
    path('blog/<int:pk>/', blog.update_blog, name='update_blog'),
    path('column/list/', blog.blog_column, name='blog_column'),
    path('column/', blog.create_column, name='create_column'),
    path('column/<int:pk>', blog.update_column, name='update_column'),
    path('comment/<int:pk>', blog.reply_comment, name='reply_comment'),
    path('comment/list', blog.comment_list, name='blog_comment'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
