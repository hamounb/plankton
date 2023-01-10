from django.urls import path

from .views import *

app_name = 'shop'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contact-us/', ContactUsView.as_view(), name='contact_us'),
    path('products/', ProductsView.as_view(), name='products'),
    path('products/<int:cid>/', ProductsFilterView.as_view(), name='products_filter'),
    path('products/details/<int:pid>/', ProductDetailsView.as_view(), name='productdetails'),
    path('cart/add/<int:pid>/', CartAddView.as_view(), name="cartadd"),
    path('cart/popup/<int:pid>/', CartPopupView.as_view(), name="cartpopup"),
    path('cart/remove/<int:pid>/', CartRemoveView.as_view(), name="cartremove"),
    path('cart/details/', CartDetailsView.as_view(), name="cartdetails"),
    path('invoice/create/', InvoiceCreateView.as_view(), name='invoice_create'),
    path('invoice/<int:id>', InvoiceView.as_view(), name='invoice'),
    path('invoice/delete/<int:idid>', InvoiceDeleteView.as_view(), name='invoice-delete'),
    path('check/', CheckingView.as_view(), name='checking'),
    path('invoice/<int:invoice_id>/pay/', PaymentView.as_view(), name='pay'),
    path('payment/verify/', PaymentVerifyView.as_view(), name='payverify'),
    path('order/home/', OfflineView.as_view(), name='offline'),
    path('order/home/online/', OnlineOrderView.as_view(), name='online'),
    path('order/home/online/<int:iid>/', OnlineOrderDetailsView.as_view(), name='online_order_details'),
    path('order/create/', OrderCreateView.as_view(), name='order_create'),
    path('order/details/<int:oid>/', OrderView.as_view(), name='order'),
    path('order/item/add/<int:oid>/<int:pid>/', OrderItemAddView.as_view(), name='order_item_add'),
    path('order/item/remove/<int:oid>/<int:pid>/', OrderItemRemoveView.as_view(), name='order_item_remove'),
    path('order/item/delete/<int:oid>/<int:pid>/', OrderItemDeleteView.as_view(), name='order_item_delete'),
 ]