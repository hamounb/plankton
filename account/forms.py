from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


def is_mobile(value):
    if value[0] != '0':
        raise forms.ValidationError('شماره وارد شده صحیح نمی‌باشد!')
    if value[1] != '9':
        raise forms.ValidationError('شماره وارد شده صحیح نمی‌باشد!')

def count_mobile(value):
    if len(value) < 11:
        raise forms.ValidationError('شماره وارد شده باید 11 رقم باشد!')

def count_otp(value):
    if len(value) < 6:
        raise forms.ValidationError('رمز وارد شده باید 6 رقم باشد!')


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')


class OtpForm(forms.Form):
    mobile = forms.CharField(max_length=11,validators=[is_mobile, count_mobile])


class OtpSubmitForm(forms.Form):
    otp = forms.CharField(max_length=6, validators=[count_otp])