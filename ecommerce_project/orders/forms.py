from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['province','district','ward','shipping_address','payment_method']
        widgets = {
            'province': forms.Select(attrs={'id':'province','class':'form-select'}),
            'district': forms.Select(attrs={'id':'district','class':'form-select','disabled':True}),
            'ward':     forms.Select(attrs={'id':'ward','class':'form-select','disabled':True}),
            'shipping_address': forms.Textarea(attrs={'class':'form-control','rows':3}),
            'payment_method':   forms.Select(attrs={'class':'form-select'}),
        }
