from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from .forms import *
from laoqi.settings import SECRET_KEY, SITE_NAME, DEFAULT_FROM_EMAIL
import time
import base64
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from account.models import UserProfile, UserInfo
from django.contrib.auth.models import User


def user_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:
                login(request, user)
                return JsonResponse({"code": 200, "msg": "Ok", 'url': reverse('blog:blog_list')})
            else:
                return JsonResponse({"code": 400, "msg": "Either username or password is not right."})
        else:
            return JsonResponse({"code": 400, "msg": "Invalid request"})
    elif request.method == 'GET':
        login_form = LoginForm()
        return render(request, 'account/login.html', {'form': login_form})


def user_logout(request):
    logout(request)
    return redirect(reverse('account:user_login'))


def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        user_profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and user_profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user_profile = user_profile_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_user_profile.user = new_user
            new_user_profile.save()
            UserInfo.objects.create(user=new_user)
            return JsonResponse({'code': 200, 'msg': 'Thanks for registering our site.'})
        else:
            return JsonResponse({'code': 200, 'msg': 'Invalid Data: ' + str(user_form.errors)})

    elif request.method == "GET":
        user_form = RegistrationForm()
        user_profile_form = UserProfileForm()
        return render(request, 'account/register.html', {'form': user_form, 'profile': user_profile_form})


def reset_password(request):
    if request.method == "POST":
        reset_form = ResetForm(request.POST)
        if reset_form.is_valid():
            cd = reset_form.cleaned_data
            user = User.objects.get(email=cd['email'])

            if user:
                # 生成改密token链接
                user_email = user.email
                token = base64.b64encode((SECRET_KEY + '###' + user_email).encode(encoding='utf-8')).decode('ascii')
                url = request.META['HTTP_HOST'] + reverse('backend:reset_password') + '?reset_token=' + token
                subject = 'Reset your password -- from ' + SITE_NAME.upper()
                message = "Hello there,\r\n\r\nPlease click the link below to retrieve your password.\r\n\r\n" + url + \
                          "\r\n\r\nPlease note that the link will be invalid in 30 minutes.\r\n\r\n" + \
                          SITE_NAME.upper() + " Team \r\n" + time.strftime('%Y-%m-%d')

                send_mail(subject, message, DEFAULT_FROM_EMAIL, [user_email], fail_silently=False)
                return JsonResponse({
                    'code': 200, "url": reverse('backend:login'),
                    'msg': "We have sent you email to reset your password, please check your inbox."})
        else:
            return JsonResponse({'code': 403, 'msg': "Invalid request"})
    elif request.method == "GET":
        token = request.GET.get('reset_token')
        if token:
            param = base64.b64decode(token.encode(encoding='utf-8')).decode('ascii').partition('###')
            user = User.objects.get(email=param[2])
            secret_key_from_user = param[0]
            if (secret_key_from_user == SECRET_KEY) and user.email:
                return render(request, 'backend/usere/change_password.html', {"email": user.email})
        else:
            return render(request, "backend/user/reset.html")


@login_required(login_url='/account/login/')
def change_password(request):
    if request.method == 'POST':
        if ResetForm(request.POST).is_valid:
            user = User.objects.get(email=request.POST.get('email'))
            user.set_password(request.POST.get('password'))
            user.save()
            return JsonResponse({"code": 200, 'msg': "Your password has been resst", "url": reverse('backend:login')})
        else:
            return JsonResponse({"code": 403, 'msg': "Error"})


@login_required(login_url='/account/login/')
def myself(request):
    user = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user=user)
    user_info = UserInfo.objects.get(user=user)

    data = {'user': user, 'user_info': user_info, 'user_profile': user_profile}
    return render(request, 'account/myself.html', data)


@login_required(login_url='/account/login/')
def edit_myself(request):
    user = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user=user)
    user_info = UserInfo.objects.get(user=user)
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        user_info_form = UserInfoForm(request.POST, instance=user_info)
        user_profile_form = UserProfileForm(request.POST, instance=user_info)

        if user_form.is_valid() and user_info_form.is_valid() and user_profile_form.is_valid():
            user_cd = user_form.cleaned_data
            user_info_cd = user_info_form.cleaned_data
            user_profile_cd = user_profile_form.cleaned_data

            user.email = user_cd['email']
            user_profile.country = user_profile_cd['country']
            user_profile.birth = user_profile_cd['birth']
            user_info.school = user_info_cd['school']
            user_info.company = user_info_cd['company']
            user_info.profession = user_info_cd['profession']
            user_info.address = user_info_cd['address']
            user_info.aboutme = user_info_cd['aboutme']
            user.save()
            user_info.save()
            user_profile.save()

            return redirect(reverse('account:account_info'))
        else:
            return JsonResponse({"code": 400, "msg": str(user_form.errors)
                                                     + str(user_profile_form.errors)
                                                     + str(user_info_form.errors)})

    elif request.method == 'GET':

        user_form = UserForm(instance=request.user)
        user_profile_form = UserProfileForm(initial={'birth': user_profile.birth, 'country': user_profile.country})
        user_info_form = UserInfoForm(initial={
            'school': user_info.school,
            'profession': user_info.profession,
            'company': user_info.company,
            'aboutme': user_info.aboutme,
            'address': user_info.address
        })

        data = {'user_info_form': user_info_form, 'user_form': user_form, 'user_profile_form': user_profile_form}
        return render(request, 'account/edit_myself.html', data)


def my_image(request):
    return render(request, 'account/imagecrop.html')





