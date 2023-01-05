# Generated by Django 4.1.1 on 2023-01-03 18:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HallModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ تغییرات')),
                ('name', models.CharField(max_length=50, verbose_name='نام سالن')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'سالن',
                'verbose_name_plural': 'سالن\u200cها',
            },
        ),
        migrations.CreateModel(
            name='MobileModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ تغییرات')),
                ('mobile', models.CharField(max_length=11, unique=True, verbose_name='شماره موبایل')),
                ('otp', models.CharField(blank=True, max_length=6, null=True, verbose_name='کد تصادفی')),
                ('is_active', models.BooleanField(default=False, verbose_name='فعال')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProfileModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ تغییرات')),
                ('booth_name', models.CharField(blank=True, max_length=80, null=True, verbose_name='نام غرفه')),
                ('booth_number', models.CharField(blank=True, max_length=3, null=True, verbose_name='شماره غرفه')),
                ('code', models.CharField(blank=True, max_length=10, null=True, verbose_name='کد ملی')),
                ('hall', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.hallmodel', verbose_name='نام سالن')),
                ('mobile', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.mobilemodel', verbose_name='شماره موبایل')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
