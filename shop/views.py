from django.shortcuts import render, get_object_or_404, redirect
from django import views
from django.http.response import HttpResponseForbidden
from account.models import ProfileModel
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import OfflineInvoiceForm
from zeep import Client
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from account.models import ProfileModel
from django.contrib import messages

# Create your views here.
class IndexView(views.View):
    
    def get(self, request):
        return render(request, "shop/index.html")


class ContactUsView(views.View):

    def get(self, request):
        return render(request, 'shop/contact_us.html')


class ProductsView(views.View):

    def get(self, request):
        products = ProductModel.objects.all()
        category = CategoryModel.objects.all()
        return render(request, "shop/products.html", {"products":products, "category":category})


class ProductsFilterView(views.View):

    def get(self, request, cid):
        products = ProductModel.objects.filter(category=cid)
        category = CategoryModel.objects.all()
        return render(request, "shop/products_filter.html", {"products":products, "category":category})


class ProductDetailsView(views.View):

    def get(self, request, pid):
        product = get_object_or_404(ProductModel, id=pid)
        return render(request, "shop/productdetails.html", {"product":product})


class CartAddView(views.View):

    def get(self, request, pid):
        ref = request.META['HTTP_REFERER']
        product = get_object_or_404(ProductModel, id=pid)
        cart = request.session.get('cart', {})
        k = str(product.id)
        if product.available:
            if k in cart:
                cart[k] += 1    
            else:
                cart[k] = 1
        else:
            pass
        request.session['cart'] = cart
        return redirect(ref)


class CartPopupView(views.View):

    def get(self, request, pid):
        ref = request.META['HTTP_REFERER']
        product = get_object_or_404(ProductModel, id=pid)
        cart = request.session.get('cart', {})
        k = str(product.id)
        if product.available:
            if k in cart and cart[k]>1:
                cart[k] -= 1    
            else:
                cart[k] = 1
        else:
            pass
        request.session['cart'] = cart
        return redirect(ref)


class CartDetailsView(views.View):

    def get(self, request):
        cart = request.session.get('cart', {})
        products = ProductModel.objects.filter(id__in=[int(id) for id in cart.keys()])
        c = {}
        total = 0
        for k,v in cart.items():
            product = products.get(id=int(k))
            total += product.price * v
            c[k] = {'product': product, 'count': v}
        return render(request, 'shop/cartdetails.html', {'cart': c, "total":total})


class CheckingView(LoginRequiredMixin, views.View):
    login_url = "login"

    def get(self, request):
        user = request.user
        check = get_object_or_404(ProfileModel, user=user)
        if check:
            if check.hall and check.booth_name and check.booth_number:
                return redirect("shop:invoice_create")
            else:
                return render(request, 'shop/checking.html')
        else:
            return redirect("account:profile")


class CartRemoveView(views.View):

    def get(self, request, pid):
        cart = request.session.get('cart', {})
        id = str(pid)
        if id in cart:
            cart.pop(id)
        request.session['cart'] = cart
        ref = request.META['HTTP_REFERER']
        return redirect(ref)


class InvoiceCreateView(LoginRequiredMixin, views.View):
    login_url = "login"

    def get(self, request):
        cart = request.session.get('cart', {})
        if not cart:
            return redirect('shop:index')
        products = ProductModel.objects.filter(id__in=[int(id) for id in cart.keys()])
        invoice = InvoiceModel(user=request.user)
        invoice.save()
        total = 0
        for k,v in cart.items():
            product = products.get(pk=k)
            count = v
            total += product.price * count
            item = InvoiceItemModel(name=product.name, price=product.price, 
                               count=count, invoice=invoice, product=product)
            item.save()
        invoice.total = total 
        invoice.save()
        return redirect('shop:invoice', id=invoice.pk)


class InvoiceDeleteView(LoginRequiredMixin, views.View):
    login_url = "login"

    def get(self, request, idid):
        invoice = get_object_or_404(InvoiceModel, id=idid)
        item = InvoiceItemModel.objects.filter(invoice=invoice)
        user = get_object_or_404(User, id=request.user.id)
        if invoice.user == user:
            for i in item:
                i.delete()
            invoice.delete()
            ref = request.META['HTTP_REFERER']
            return redirect(ref)
        ref = request.META['HTTP_REFERER']
        return redirect(ref)


class InvoiceView(LoginRequiredMixin, views.View):
    login_url = "login"

    def get(self, request, id):
        invoice = get_object_or_404(InvoiceModel, pk=id)
        item = InvoiceItemModel.objects.filter(invoice=id)
        return render(request, 'shop/invoice.html', {'invoice': invoice, 'item':item})


class OfflineView(LoginRequiredMixin, views.View):
    login_url = "login"

    def get(self, request):
        user_id = request.user
        user = get_object_or_404(User, id=user_id.id)
        if user.is_staff:
            invoice = OfflineInvoiceModel.objects.all().order_by("-created_date")
            return render(request, 'shop/offline_order.html', {"invoice":invoice})
        else:
            return render(request, 'shop/access_denied.html')


class OnlineOrderView(LoginRequiredMixin, views.View):
    login_url = "login"

    def get(self, request):
        user_id = request.user
        user = get_object_or_404(User, id=user_id.id)
        if user.is_staff:
            payment = PaymentModel.objects.filter(state="done").order_by("-created_date")
            return render(request, 'shop/online_order.html', {"payment":payment})
        else:
            return render(request, 'shop/access_denied.html')


class OnlineOrderDetailsView(LoginRequiredMixin, views.View):
    login_url = "login"

    def get(self, request, iid):
        user_id = request.user
        user = get_object_or_404(User, id=user_id.id)
        if user.is_staff:
            item = InvoiceItemModel.objects.filter(invoice=iid)
            invoice = get_object_or_404(InvoiceModel, id=iid)
            customer = get_object_or_404(ProfileModel, user=invoice.user)
            return render(request, 'shop/online_order_details.html', {"item":item, "customer":customer, "invoice":invoice})
        else:
            return render(request, 'shop/access_denied.html')



class OrderCreateView(LoginRequiredMixin, views.View):
    login_url = "login"

    def get(self, request):
        user_id = request.user
        user = get_object_or_404(User, id=user_id.id)
        if user.is_staff:
            order = OfflineInvoiceModel(user=user_id)
            order.save()
            return redirect("shop:order",oid=order.pk)
        else:
            return render(request, 'shop/access_denied.html')


class OrderView(LoginRequiredMixin, views.View):
    login_url = "login"

    def get(self, request, oid):
        user_id = request.user
        user = get_object_or_404(User, id=user_id.id)
        if user.is_staff:
            invoice = get_object_or_404(OfflineInvoiceModel, id=oid)
            form = OfflineInvoiceForm(instance=invoice)
            items = OfflineInvoiceItemModel.objects.filter(invoice=invoice.id)
            category = CategoryModel.objects.all()
            products = ProductModel.objects.filter(available=True)
            if invoice.state == "done" :
                message = "این سفارش ثبت شده است"
                return render(request, 'shop/order.html', {"invoice":invoice, "items":items, 'category':category, "products":products, "form":form, "message":message})
            return render(request, 'shop/order.html', {"invoice":invoice, "items":items, 'category':category, "products":products, "form":form})
        else:
            return render(request, 'shop/access_denied.html')

    def post(self, request, oid):
        invoice = get_object_or_404(OfflineInvoiceModel, id=oid)
        form = OfflineInvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
        ref = request.META['HTTP_REFERER']
        return redirect(ref)
        



class OrderItemAddView(LoginRequiredMixin, views.View):
    login_url = "login"

    def get(self, request, pid, oid):
        user_id = request.user
        user = get_object_or_404(User, id=user_id.id)
        if user.is_staff:
            invoice = get_object_or_404(OfflineInvoiceModel, id=oid)
            product = get_object_or_404(ProductModel, id=pid)
            if invoice.state == "done":
                return redirect('shop:order', oid=invoice.pk)
            try:
                item = OfflineInvoiceItemModel.objects.get(invoice=invoice, product=product)
                item.count += 1
                item.save()
                invoice.total += item.price
                invoice.save()
                return redirect('shop:order', oid=invoice.pk)
            except OfflineInvoiceItemModel.DoesNotExist:
                item = OfflineInvoiceItemModel(name=product.name, price=product.price, product=product, invoice=invoice, count=1)
                item.save()
                invoice.total += item.price
                invoice.save()
                return redirect('shop:order', oid=invoice.pk)
        else:
            return render(request, 'shop/access_denied.html')


class OrderItemRemoveView(LoginRequiredMixin, views.View):
    login_url = "login"

    def get(self, request, oid, pid):
        user_id = request.user
        user = get_object_or_404(User, id=user_id.id)
        if user.is_staff:
            invoice = get_object_or_404(OfflineInvoiceModel,id=oid)
            if invoice.state != "done":
                item = get_object_or_404(OfflineInvoiceItemModel, id=pid)
                if item and item.count > 1:
                    item.count -= 1
                    item.save()
                    invoice.total -= item.price
                    invoice.save()
                    return redirect('shop:order', oid=invoice.pk)
                else:
                    return redirect('shop:order', oid=invoice.pk)
            else:
                return redirect('shop:order', oid=invoice.pk)
        else:
            return render(request, 'shop/access_denied.html')


class OrderItemDeleteView(LoginRequiredMixin, views.View):
    login_url = "login"

    def get(self, request, pid, oid):
        user_id = request.user
        user = get_object_or_404(User, id=user_id.id)
        if user.is_staff:
            invoice = get_object_or_404(OfflineInvoiceModel,id=oid)
            if invoice.state != "done":
                item = get_object_or_404(OfflineInvoiceItemModel, id=pid)
                invoice.save()
                invoice.total -= item.price * item.count
                item.delete()
                return redirect('shop:order', oid=invoice.pk)
            else:
                return redirect('shop:order', oid=invoice.pk)
        else:
            return render(request, 'shop/access_denied.html')


psp_page = 'https://sandbox.zarinpal.com/pg/StartPay/'
merchant = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'

class PaymentView(LoginRequiredMixin, views.View):
    login_url = "login"
    
    def get(self, request, invoice_id):
        invoice = get_object_or_404(InvoiceModel, pk=invoice_id)
        if invoice.user != request.user:
            return HttpResponseForbidden()
        
        if invoice.state != InvoiceModel.STATE_PENDING:
            return HttpResponseForbidden()

        payment = PaymentModel(invoice=invoice, amount=invoice.total,
                          description=f'فاکتور #{invoice.id}')
        site = get_current_site(request)
        
        callback = f"http://{site!s}" + reverse('shop:payverify')
        client = Client('https://sandbox.zarinpal.com/pg/services/WebGate/wsdl')
        result = client.service.PaymentRequest(MerchantID=merchant, Amount=payment.amount, 
                                               Description=payment.description, 
                                               CallbackURL=callback)
        payment.status = result.Status
        if result.Status == 100:
            payment.authority = result.Authority
            payment.save()
            return redirect(psp_page+payment.authority)
        else:
            payment.state = PaymentModel.STATE_ERROR
            self.save()
            return render(request, 'shop/pay_error.html')


class PaymentVerifyView(LoginRequiredMixin, views.View):
    login_url = "login"

    def get(self, request):
        authority = request.GET.get('Authority')
        status = request.GET.get('Status')
        if not authority or not status:
            return HttpResponseForbidden()

        payment = get_object_or_404(PaymentModel, authority=authority, state=PaymentModel.STATE_PENDING)

        if status == "OK":
            client = Client('https://sandbox.zarinpal.com/pg/services/WebGate/wsdl')
            result = client.service.PaymentVerification(merchant, payment.authority, payment.amount)
            payment.status = result.Status
            payment.ref_id = result.RefID
            if result.Status == 100:
                payment.state = PaymentModel.STATE_DONE
                payment.invoice.state = InvoiceModel.STATE_DONE
                payment.save()
                payment.invoice.save()
                request.session['cart'] = {}
                request.session['cart_total'] = 0
                return render(request, 'shop/pay_ok.html', {'payment': payment})
            else:
                payment.state = PaymentModel.STATE_ERROR
                payment.save()
                return render(request, 'shop/pay_error.html')


        else:
            payment.state = PaymentModel.STATE_ERROR
            payment.save()
            return render(request, 'shop/pay_error.html')


class UserOrderView(LoginRequiredMixin, views.View):
    login_url = "login"

    def get(self, request):
        user = request.user
        invoice = InvoiceModel.objects.filter(user=user, state="done")
        profile = get_object_or_404(ProfileModel, user=user)
        return render(request, 'account/profile_order.html', {"invoice":invoice, "profile":profile})


class UserOrderDetailsView(LoginRequiredMixin, views.View):
    login_url = "login"

    def get(self, request, iid):
        user = request.user
        profile = get_object_or_404(ProfileModel, user=user)
        products = InvoiceItemModel.objects.filter(invoice=iid)
        payment = get_object_or_404(PaymentModel, invoice=iid)
        return render(request, "account/profile_order_details.html", {"product":products, "payment":payment, "profile":profile})