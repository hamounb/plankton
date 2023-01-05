from django.urls import path

from .views import *

app_name = 'account'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('otp/', OtpView.as_view(), name='otp'),
    path('otp/<str:number>/', OtpSubmitView.as_view(), name='otp-submit'),
]