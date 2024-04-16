from banking_app.forms import DepositForm
from banking_app.models import Account


from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()

class DepositViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        
        test_account1 = Account.objects.create(first_name='Test', last_name='User1', balance=0, owner=test_user1)
        test_account2 = Account.objects.create(first_name='Test', last_name='User2', balance=0, owner=test_user2)
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('deposit'))
        self.assertRedirects(response, '/accounts/login/?next=/banking_app/deposit/')
    
    def test_redirect_if_logged_in(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('deposit'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check that we used correct template
        self.assertTemplateUsed(response, 'banking_app/deposit.html')

    def test_redirects_to_index_on_success(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.post(reverse('deposit'), {'deposit_amount': 12.50})
        self.assertRedirects(response, reverse('index'))

    def test_form_invalid_deposit(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.post(reverse('deposit'), {'deposit_amount': 'ten'})
        self.assertFormError(response.context['form'], 'deposit_amount', 'Enter a number.')

class WithdrawViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='rfg5Hiu&Eq')
        Account.objects.create(first_name='Test', last_name='User', balance=0, owner=test_user)

    def test_user_not_logged_in(self):
        response = self.client.get(reverse('withdraw'))
        self.assertRedirects(response, "/accounts/login/?next=/banking_app/withdraw/")

    def test_user_logged_in(self):
        self.client.login(username='testuser', password='rfg5Hiu&Eq')
        response = self.client.get(reverse('withdraw'))

        self.assertEqual(str(response.context['user']), 'testuser')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "banking_app/withdraw.html")

    def test_redirect_to_index_on_success(self):
        self.client.login(username='testuser', password='rfg5Hiu&Eq')
        response = self.client.post(reverse('withdraw'), {"withdraw_amount": 0})
        self.assertRedirects(response, reverse('index'))




