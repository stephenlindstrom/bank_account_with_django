from django.test import TestCase

from banking_app.forms import DepositForm, WithdrawForm, RegistrationForm, AccountForm

class DepositFormTest(TestCase):
    def test_deposit_form_decimal_field(self):
        form = DepositForm()
        self.assertTrue(form.fields['deposit_amount'].label is None or form.fields['deposit_amount'].label == 'Deposit amount')


class WithdrawFormTest(TestCase):
    def test_withdraw_form_decimal_field(self):
        form = WithdrawForm()
        self.assertTrue(form.fields['withdraw_amount'].label is None or form.fields['withdraw_amount'].label == 'Withdraw amount')


class RegistrationFormTest(TestCase):
    def test_registration_form_field_labels(self):
        form = RegistrationForm()
        self.assertTrue(form.fields['username'].label is None or form.fields['username'].label == 'Username')
        self.assertTrue(form.fields['email'].label is None or form.fields['email'].label == 'Email')
        self.assertTrue(form.fields['password1'].label is None or form.fields['password1'].label == 'Password')
        self.assertTrue(form.fields['password2'].label is None or form.fields['password2'].label == 'Password confirmation')


class AccountFormTest(TestCase):
    def test_account_form_field_labels(self):
        form = AccountForm()
        self.assertTrue(form.fields['first_name'].label is None or form.fields['first_name'].label == 'First name')
        self.assertTrue(form.fields['last_name'].label is None or form.fields['last_name'].label == 'Last name')