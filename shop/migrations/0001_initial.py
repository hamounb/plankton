# Generated by Django 4.1.1 on 2023-01-06 08:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shop.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ تغییرات')),
                ('name', models.CharField(max_length=100, verbose_name='نام دسته\u200cبندی')),
                ('cover', models.ImageField(blank=True, null=True, upload_to=shop.models.get_cover_path, verbose_name='تصویر کاور')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'دسته\u200cبندی',
                'verbose_name_plural': 'دسته\u200cبندی\u200cها',
            },
        ),
        migrations.CreateModel(
            name='InvoiceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('total', models.PositiveIntegerField(default=0, verbose_name='مبلغ کل')),
                ('state', models.CharField(choices=[('pending', 'در انتظار پرداخت'), ('done', 'پرداخت شده')], default='pending', max_length=10, verbose_name='وضعیت پرداخت')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'فاکتور',
                'verbose_name_plural': 'فاکتورها',
            },
        ),
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ تغییرات')),
                ('name', models.CharField(max_length=100, verbose_name='نام محصول')),
                ('description', models.TextField(blank=True, max_length=200, null=True, verbose_name='توضیحات')),
                ('cover', models.ImageField(blank=True, null=True, upload_to=shop.models.get_cover_path, verbose_name='تصویر کاور')),
                ('available', models.BooleanField(default=True, verbose_name='موجود در انبار')),
                ('price', models.PositiveIntegerField(default=0, verbose_name='قیمت')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.categorymodel', verbose_name='دسته\u200cبندی')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'محصول',
                'verbose_name_plural': 'محصولات',
            },
        ),
        migrations.CreateModel(
            name='PaymentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.IntegerField(verbose_name='مبلغ کل پرداخت')),
                ('description', models.CharField(max_length=255, verbose_name='توضیحات')),
                ('state', models.CharField(choices=[('pending', 'در انتظار پرداخت'), ('done', 'پرداخت موفق'), ('error', 'پرداخت ناموفق')], default='pending', max_length=10, verbose_name='وضعیت پرداخت')),
                ('authority', models.CharField(max_length=36, null=True, verbose_name='کد دریافت')),
                ('ref_id', models.CharField(max_length=100, null=True, verbose_name='شماره پیگیری')),
                ('status', models.IntegerField(null=True, verbose_name='کد وضعیت')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.invoicemodel', verbose_name='فاکتور')),
            ],
            options={
                'verbose_name': 'پرداخت',
                'verbose_name_plural': 'پرداخت\u200cها',
            },
        ),
        migrations.CreateModel(
            name='OfflineInvoiceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('pending', 'در انتظار پرداخت'), ('done', 'پرداخت شده')], default='pending', max_length=10, verbose_name='وضعیت پرداخت')),
                ('table', models.CharField(choices=[('one', 'یک'), ('two', 'دو'), ('three', 'سه'), ('four', 'چهار'), ('five', 'پنج'), ('six', 'شش'), ('seven', 'هفت'), ('eight', 'هشت'), ('nine', 'نه'), ('out', 'بیرون بر')], default='out', max_length=10, verbose_name='شماره میز')),
                ('total', models.IntegerField(default=0, verbose_name='جمع کل')),
                ('pay_id', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='شماره پیگیری')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'فاکتور دستی',
                'verbose_name_plural': 'فاکتورهای دستی',
            },
        ),
        migrations.CreateModel(
            name='OfflineInvoiceItemModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, verbose_name='نام محصول')),
                ('price', models.IntegerField(verbose_name='قیمت واحد')),
                ('count', models.IntegerField(default=0, verbose_name='تعداد سفارش')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.offlineinvoicemodel', verbose_name='فاکتور')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.productmodel', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'محصول فاکتور دستی',
                'verbose_name_plural': 'محصولات فاکتورهای دستی',
            },
        ),
        migrations.CreateModel(
            name='InvoiceItemModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, verbose_name='نام محصول')),
                ('price', models.PositiveIntegerField(verbose_name='قیمت واحد')),
                ('count', models.IntegerField(default=1, verbose_name='تعداد سفارش')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.invoicemodel', verbose_name='فاکتور')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.productmodel', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'محصول فاکتور',
                'verbose_name_plural': 'محصولات فاکتورها',
            },
        ),
    ]
