from django.urls import path, re_path
from account import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView


app_name = "account"
urlpatterns = [
    re_path('^login/$', views.user_login, name='user_login'),
    re_path('^logout/$', views.user_logout, name='user_logout'),
    re_path('^register/$', views.register, name='user_register'),
    re_path('^password_change/$', views.change_password, name='password_change'),
    re_path('^password_reset/$', views.reset_password, name='password_reset'),
    re_path('^info/$', views.myself, name='account_info'),
    re_path('^edit_info/$', views.edit_myself, name='edit_account_info'),
    re_path('^my_image/$', views.my_image, name='edit_my_image'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
