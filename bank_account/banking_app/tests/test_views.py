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
    
    def test_redirect_if_not_logged_in(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('deposit'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check that we used correct template
        self.assertTemplateUsed(response, 'banking_app/deposit.html')

