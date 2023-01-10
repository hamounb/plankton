from random import randint
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BaseModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    created_date = models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)
    modified_date = models.DateTimeField(verbose_name='تاریخ تغییرات', auto_now=True)

    class Meta:
        abstract = True


class HallModel(BaseModel):
    name = models.CharField(verbose_name='نام سالن', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'سالن'
        verbose_name_plural = 'سالن‌ها'


class MobileModel(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='کاربر')
    mobile = models.CharField(verbose_name='شماره موبایل', max_length=11, unique=True)
    otp = models.CharField(verbose_name='کد تصادفی', max_length=6, null=True, blank=True)
    is_active = models.BooleanField(verbose_name='فعال', default=False)
    
    def generate(self):
        v = randint(100000, 999999)
        self.otp = v
        return self.otp

    def __str__(self):
        return self.mobile
    
    class Meta:
        verbose_name = 'موبایل'
        verbose_name_plural = 'موبایل‌ها'


class ProfileModel(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='کاربر')
    mobile = models.OneToOneField(MobileModel, on_delete=models.CASCADE, blank=True, null=True, verbose_name='شماره موبایل')
    hall = models.ForeignKey(HallModel, on_delete=models.CASCADE, blank=True, null=True, verbose_name='نام سالن')
    booth_name = models.CharField(verbose_name='نام غرفه', max_length=80, null=True, blank=True)
    booth_number = models.CharField(verbose_name='شماره غرفه', max_length=3, null=True, blank=True)
    code = models.CharField(verbose_name='کد ملی', null=True, blank=True, max_length=10)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.mobile.mobile}"

    class Meta:
        verbose_name = 'حساب کاربری'
        verbose_name_plural = 'حساب‌های کاربری'
        