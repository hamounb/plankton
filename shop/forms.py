from django import forms
from django.forms import ModelForm
from .models import OfflineInvoiceModel



class QuantityForm(forms.Form):
    quantity = forms.IntegerField()


class OfflineInvoiceForm(ModelForm):

    class Meta:
        model = OfflineInvoiceModel
        fields = ['pay_id', 'state', 'table']