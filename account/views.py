from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django import views
from .forms import *
from django.contrib import messages
from shop.models import InvoiceModel
import requests

# Create your views here.

class SignUpView(views.View):

    def get(self, request):
        form = SignUpForm()
        return render(request, 'account/signup.html', {'form':form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('account:otp')
        return render(request, 'account/signup.html', {'form':form})


class OtpView(LoginRequiredMixin, views.View):
    login_url = 'login'

    def get(self, request):
        form = OtpForm()
        return render(request, 'account/otp.html', {'form':form})

    def post(self, request):
        form = OtpForm(request.POST)
        user = get_object_or_404(User, id=request.user.id)
        if form.is_valid():
            number = form.cleaned_data['mobile']
            try:
                mobile = MobileModel.objects.get(mobile=number)
                if mobile.user != user.pk:
                    messages.error(request, 'این شماره موبایل قبلا در سیستم ثبت شده است!')
                    return render(request, 'account/otp.html', {'form':form})
            except MobileModel.DoesNotExist:
                mobile = MobileModel(user=user, mobile=number)
            if mobile.is_active:
                return render(request, 'account/otp-success.html') 
            mobile.generate()
            mobile.save()
            new_line = '\n'
            text_sms = f"کافه پلانکتون نمایشگاه {new_line}رمز فعال‌سازی حساب: {str(mobile.otp)}"
            data = {'from': '50004001896361', 'to': str(number), 'text': text_sms, 'domain':'127.0.0.1'}
            sms = requests.post('https://console.melipayamak.com/api/send/simple/8265f04cef6145c3be077c6f34e656c1', json=data)
            print(sms.json())
            return redirect('account:otp-submit', number=number)
        return render(request, 'account/otp.html', {'form':form})


class OtpSubmitView(LoginRequiredMixin ,views.View):
    login_url = 'login'

    def get(self, request, number):
        mobile = get_object_or_404(MobileModel, mobile=number)
        form = OtpSubmitForm()
        if mobile.is_active:
             return render(request, 'account/otp-success.html')
        return render(request, 'account/otp-submit.html', {'number':mobile.mobile, 'form':form})

    def post(self, request, number):
        form = OtpSubmitForm(request.POST)
        mobile = get_object_or_404(MobileModel, mobile=number)
        if form.is_valid():
            code = form.cleaned_data['otp']
            if mobile.otp == code:
                mobile.is_active = True
                mobile.save()
                profile = ProfileModel(user_id=request.user.id, mobile_id=mobile.pk)
                profile.save()
                return render(request, 'account/otp-success.html')
            return render(request, 'account/otp-submit.html', {'number':mobile.mobile, 'form':form, 'message':'رمز وارد شده صحیح نمی‌باشد!'})
        return render(request, 'account/otp-submit.html', {'number':mobile.mobile, 'form':form})
            

class ProfileView(LoginRequiredMixin, views.View):
    login_url = 'login'

    def get(self, request):
        user = request.user
        try:
            profile = ProfileModel.objects.get(user=user.id)
        except ProfileModel.DoesNotExist:
            return redirect('account:otp')
        if profile.mobile.is_active:
            return render(request, 'account/profile.html', {'profile':profile})
        return redirect('account:otp')


class ProfileEditView(LoginRequiredMixin, views.View):
    login_url = 'login'

    def get(self, request, pid):
        profile = get_object_or_404(ProfileModel, pk=pid)
        form = ProfileEditForm(instance=profile)
        try:
            profile = ProfileModel.objects.get(pk=pid)
        except ProfileModel.DoesNotExist:
            return redirect('account:otp')
        if profile.mobile.is_active:
            return render(request, 'account/profile-edit.html', {'profile':profile, 'form':form})
        return redirect('account:otp')

    def post(self, request, pid):
        profile = get_object_or_404(ProfileModel, pk=pid)
        form = ProfileEditForm(request.POST, instance=profile)
        if profile.mobile.is_active:
            if form.is_valid():
                form.save()
                return redirect('account:profile')
            return render(request, 'account/profile-edit.html', {'profile':profile, 'form':form})
        return redirect('account:otp')


class ProfileOrderView(LoginRequiredMixin, views.View):
    login_url = 'login'

    def get(self, request):
        user = get_object_or_404(User, id=request.user.id)
        order = InvoiceModel.objects.filter(user=user).order_by("-created_date")
        return render(request, 'account/profile-order.html', {'order':order})
        