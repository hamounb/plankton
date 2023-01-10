from datetime import datetime
import os
import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def get_cover_path(obj, fn):
    ex = os.path.splitext(fn)[1]
    uid = uuid.uuid5(uuid.NAMESPACE_URL, f"store-carpet-{obj.pk}")
    path = datetime.now().strftime(f"uifshop-covers/%Y/%m/%d/{uid}{ex}")
    return path

def get_image_path(obj, fn):
    ex = os.path.splitext(fn)[1]
    uid = uuid.uuid5(uuid.NAMESPACE_URL, f"store-carpet-{obj.pk}")
    path = datetime.now().strftime(f"uifshop-images/%Y/%m/%d/{uid}{ex}")
    return path



class BaseModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="کاربر")
    created_date = models.DateTimeField(verbose_name="تاریخ ایجاد", auto_now_add=True)
    modified_date = models.DateTimeField(verbose_name="تاریخ تغییرات", auto_now=True)

    class Meta:
        abstract = True

class CategoryModel(BaseModel):
    name = models.CharField(verbose_name="نام دسته‌بندی", max_length=100)
    cover = models.ImageField(verbose_name="تصویر کاور", upload_to=get_cover_path, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"


class ProductModel(BaseModel):
    name = models.CharField(verbose_name="نام محصول", max_length=100)
    category = models.ForeignKey(CategoryModel, on_delete=models.SET_NULL, verbose_name="دسته‌بندی", null=True, blank=True)
    description = models.TextField(verbose_name="توضیحات", max_length=200, null=True, blank=True)
    cover = models.ImageField(verbose_name="تصویر کاور", upload_to=get_cover_path, null=True, blank=True)
    available = models.BooleanField(verbose_name="موجود در انبار", default=True)
    price = models.PositiveIntegerField(verbose_name="قیمت", default=0)
        
    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return self.name


class InvoiceModel(models.Model):
    STATE_PENDING = 'pending'
    STATE_DONE = 'done'

    STATE_CHOICES = ((STATE_PENDING, 'در انتظار پرداخت'),
                     (STATE_DONE, 'پرداخت شده'))

    created_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="کاربر")
    total = models.PositiveIntegerField(verbose_name="مبلغ کل", default=0)
    state = models.CharField(verbose_name="وضعیت پرداخت", max_length=10, choices=STATE_CHOICES, default=STATE_PENDING)

    class Meta:
        verbose_name = "فاکتور"
        verbose_name_plural = "فاکتورها"

    def __str__(self):
        return f"{self.user.username} - {self.state}"


class InvoiceItemModel(models.Model):
    invoice = models.ForeignKey(InvoiceModel, on_delete=models.PROTECT, verbose_name="فاکتور") 
    product = models.ForeignKey(ProductModel, on_delete=models.PROTECT, verbose_name="محصول")
    name = models.CharField(verbose_name="نام محصول", max_length=25)
    price = models.PositiveIntegerField(verbose_name="قیمت واحد")
    count = models.IntegerField(default=1, verbose_name="تعداد سفارش")

    class Meta:
        verbose_name = "محصول فاکتور"
        verbose_name_plural = "محصولات فاکتورها"

    def __str__(self):
        return f"{self.product.name} - {self.invoice.created_date} - {self.invoice.state}"


class OfflineInvoiceModel(models.Model):
    STATE_PENDING = 'pending'
    STATE_DONE = 'done'
    STATE_CHOICES = ((STATE_PENDING, 'در انتظار پرداخت'),
                     (STATE_DONE, 'پرداخت شده'))
    TABLE_CHOICES = (("one", "یک"),("two", "دو"),("three", "سه"),("four", "چهار"),("five", "پنج"),
                    ("six", "شش"),("seven", "هفت"),("eight", "هشت"),("nine", "نه"),("out", "بیرون بر"))

    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="کاربر")
    state = models.CharField(verbose_name="وضعیت پرداخت", max_length=10, choices=STATE_CHOICES, default=STATE_PENDING)
    table = models.CharField(verbose_name="شماره میز", max_length=10, choices=TABLE_CHOICES, default="out")
    total = models.IntegerField(verbose_name="جمع کل", default=0)
    pay_id = models.CharField(verbose_name="شماره پیگیری", null=True, blank=True,max_length=50)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "فاکتور دستی"
        verbose_name_plural = "فاکتورهای دستی"

    def __str__(self):
        return f"{self.state} - {self.pay_id} - {self.total}"


class OfflineInvoiceItemModel(models.Model):
    invoice = models.ForeignKey(OfflineInvoiceModel, on_delete=models.CASCADE, verbose_name="فاکتور") 
    product = models.ForeignKey(ProductModel, on_delete=models.PROTECT, verbose_name="محصول")
    name = models.CharField(verbose_name="نام محصول", max_length=25)
    price = models.IntegerField(verbose_name="قیمت واحد")
    count = models.IntegerField(default=0, verbose_name="تعداد سفارش")

    class Meta:
        verbose_name = "محصول فاکتور دستی"
        verbose_name_plural = "محصولات فاکتورهای دستی"

    def __str__(self):
        return f"{self.product.name} - {self.invoice.created_date} - {self.invoice.state}"


class PaymentModel(models.Model):
    STATE_PENDING = 'pending'
    STATE_DONE = 'done'
    STATE_ERROR = 'error'

    STATE_CHOICES = ((STATE_PENDING, 'در انتظار پرداخت'),
                     (STATE_DONE, 'پرداخت موفق'),
                     (STATE_ERROR, 'پرداخت ناموفق'))

    created_date = models.DateTimeField(auto_now_add=True)
    invoice = models.ForeignKey(InvoiceModel, on_delete=models.PROTECT, verbose_name='فاکتور')
    amount = models.IntegerField(verbose_name='مبلغ کل پرداخت')
    description = models.CharField(max_length=255, verbose_name='توضیحات')
    state = models.CharField(max_length=10, choices=STATE_CHOICES,
                             default=STATE_PENDING, verbose_name='وضعیت پرداخت')
    authority = models.CharField(max_length=36, null=True, verbose_name='کد دریافت')
    ref_id = models.CharField(max_length=100, null=True, verbose_name='شماره پیگیری')
    status = models.IntegerField(null=True, verbose_name='کد وضعیت')

    class Meta:
        verbose_name = "پرداخت"
        verbose_name_plural = "پرداخت‌ها"

    def __str__(self):
        return f"{self.invoice.pk} - {self.created_date} - {self.ref_id}"