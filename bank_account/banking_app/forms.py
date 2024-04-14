from django import forms

class DepositForm(forms.Form):
    deposit_amount = forms.DecimalField(min_value=0, decimal_places=2)