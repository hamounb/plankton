from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import HallModel, ProfileModel


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


def is_number(value):
    if str(value).isnumeric():
        raise forms.ValidationError('لطفا فقط شماره وارد کنید!')


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')


class OtpForm(forms.Form):
    mobile = forms.CharField(max_length=11,validators=[is_mobile, count_mobile])


class OtpSubmitForm(forms.Form):
    otp = forms.CharField(max_length=6, validators=[count_otp])


class ProfileEditForm(forms.ModelForm):
    # code = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    hall = forms.ModelChoiceField(queryset=HallModel.objects.all(), label='سالن', widget=forms.Select(attrs={'class':'form-control'}))
    # booth_name = forms.CharField(max_length=80, label='نام غرفه', widget=forms.widgets.Input(attrs={'class':'form-control'}))
    # booth_number = forms.CharField(max_length=3, validators=[is_number], label='شماره غرفه', widget=forms.widgets.Input(attrs={'class':'form-control'}))

    class Meta:
        model = ProfileModel
        exclude = ['user', 'created_date', 'modified_date', 'mobile']
        widgets = {
            'code': forms.TextInput(attrs={'class':'form-control'}),
            'booth_name': forms.TextInput(attrs={'class':'form-control'}),
            'booth_number': forms.TextInput(attrs={'class':'form-control'}),
        }
    