from django.test import TestCase

from banking_app.forms import DepositForm

class DepositFormTest(TestCase):
    def test_deposit_form_decimal_field(self):
        form = DepositForm()
        self.assertTrue(form.fields['deposit_amount'].label is None or form.fields['deposit_amount'].label == 'Deposit amount')