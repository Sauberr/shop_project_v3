from django import forms
from payment.models import *


class ShippingForm(forms.ModelForm):

    class Meta:
        model = ShippingAddress
        fields = ['full_name', 'email', 'address1', 'address2',
                  'city', 'state', 'zipcode']

        exclude = ['user',]