from django import forms

class CheckoutForm(forms.Form):
    delivery_name    = forms.CharField(max_length=100, label='Poora Naam')
    delivery_phone   = forms.CharField(max_length=20,  label='Phone Number')
    delivery_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label='Delivery Address')
    delivery_city    = forms.CharField(max_length=100, label='City')
