from django import forms
from account.models import UserProfile, UserInfo
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password do not match.')

        return cd['password2']


class UserProfileForm(forms.ModelForm):
    """
        用户账号信息
    """
    class Meta:
        model = UserProfile
        fields = ('country', 'birth')


class ResetForm(forms.Form):
    email = forms.EmailField()


class UserInfoForm(forms.ModelForm):

    class Meta:
        model = UserInfo
        fields = ('school', 'company', 'profession', 'address', 'aboutme')


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'username')
