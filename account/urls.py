from django.urls import path

from .views import *

app_name = 'account'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('otp/', OtpView.as_view(), name='otp'),
    path('otp/<str:number>/', OtpSubmitView.as_view(), name='otp-submit'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pid>/', ProfileEditView.as_view(), name='profile-edit'),
    path('profile/invoice/', ProfileOrderView.as_view(), name='profile-order'),
]