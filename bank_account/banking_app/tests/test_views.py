from banking_app.forms import DepositForm
from banking_app.models import Account, Transaction, Organization, Membership


from django.contrib.auth import get_user_model
from django.test import TestCase, TransactionTestCase
from django.urls import reverse

User = get_user_model()

class DepositViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        Account.objects.create(first_name='Test', last_name='User1', balance=0, owner=test_user1)
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('deposit'))
        self.assertRedirects(response, '/accounts/login/?next=/banking_app/deposit/')
    
    def test_get_deposit_if_logged_in(self):
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
    
    def test_deposits_amount_in_account(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        self.client.post(reverse('deposit'), {'deposit_amount': 12.50})
        user = User.objects.get(username='testuser1')
        account = Account.objects.get(owner=user)
        self.assertEqual(account.balance, 12.50)


class WithdrawViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='rfg5Hiu&Eq')
        Account.objects.create(first_name='Test', last_name='User', balance=100, owner=test_user)

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
        response = self.client.post(reverse('withdraw'), {"withdraw_amount": 50})
        self.assertRedirects(response, reverse('index'))

    def test_invalid_withdraw_amount(self):
        self.client.login(username='testuser', password='rfg5Hiu&Eq')
        response = self.client.post(reverse('withdraw'), {"withdraw_amount": 200})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'banking_app/withdraw.html')
    
    def test_amount_withdrawn_from_account(self):
        self.client.login(username='testuser', password='rfg5Hiu&Eq')
        self.client.post(reverse('withdraw'), {'withdraw_amount': 75})
        user = User.objects.get(username='testuser')
        account = Account.objects.get(owner=user)
        self.assertEqual(account.balance, 25)

class IndexViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='rfg5Hiu&Eq')

    def test_account_does_not_exist(self):
        self.client.login(username='testuser', password='rfg5Hiu&Eq')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'No account information available')

    def test_account_does_exist(self):
        test_user = User.objects.get(username='testuser')
        Account.objects.create(first_name='Test', last_name='User', balance=0, owner=test_user)
        self.client.login(username='testuser', password='rfg5Hiu&Eq')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'banking_app/index.html')
    
    def test_organization_list_passed(self):
        user = User.objects.get(username='testuser')
        Account.objects.create(first_name='Test', last_name='User', balance=0, owner=user)
        organization = Organization.objects.create(name='Test Organization')
        Membership.objects.create(member=user, organization=organization, status='member', invited_email_address='test@email.com')
        self.client.login(username='testuser', password='rfg5Hiu&Eq')
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'Test Organization')

class SignupViewTest(TestCase):
    def setUp(self):
        pass

    def test_successful_registration(self):
        response = self.client.post(reverse('signup'), {'account_form-first_name': 'Test', 'account_form-last_name': 'User', 'registration_form-username': 'testuser', 'registration_form-email': 'testuser@email.com', 'registration_form-password1': 'rfg5Hiu&Eq', 'registration_form-password2': 'rfg5Hiu&Eq'})
        user = User.objects.get(username='testuser')
        account = Account.objects.get(owner=user)

        self.assertEqual(response.status_code, 302)
        
        self.assertEqual(account.first_name, 'Test')
        self.assertEqual(account.last_name, 'User')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@email.com')
        self.assertTrue(user.check_password('rfg5Hiu&Eq'))


class TransactionViewTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testcase', password='rfg5Hiu&Eq')
        Account.objects.create(first_name='Test', last_name='User', owner=user)

    def test_transactions_template_used_logged_in_user(self):
        self.client.login(username='testcase', password='rfg5Hiu&Eq')
        user = User.objects.get(username='testcase')
        account = Account.objects.get(owner=user)
        transactions = Transaction.objects.filter(account=account)
        response = self.client.get(reverse('transactions'), {'transactions': transactions})
        self.assertTemplateUsed(response, 'banking_app/transactions.html')
        self.assertEqual(response.status_code, 200)


class GroupCreationViewTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='testcase', password='rfg5Hiu&Eq')
    
    def test_successful_get_request(self):
        self.client.login(username='testcase', password='rfg5Hiu&Eq')
        response = self.client.get(reverse('create_group'))
        self.assertEqual(response.status_code, 200)

    def test_successful_post_request(self):
        self.client.login(username='testcase', password='rfg5Hiu&Eq')
        response = self.client.post(reverse('create_group'), {'name': 'Test Group'})
        self.assertRedirects(response, reverse('index'))

    def test_add_group_to_user(self):
        self.client.login(username='testcase', password='rfg5Hiu&Eq')
        self.client.post(reverse('create_group'), {'name': 'Test Group'})
        user = User.objects.get(username='testcase')
        organization = Organization.objects.get(name='Test Group')
        self.assertTrue(Membership.objects.filter(member=user, organization=organization).exists())


class InviteMemberViewTest(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        user = User.objects.create_user(username='testcase', password='rfg5Hiu&Eq')
        Account.objects.create(first_name='Test', last_name='User', owner=user)

    def test_group_does_not_exist(self):
        self.client.login(username='testcase', password='rfg5Hiu&Eq')
        response = self.client.get(reverse('invite_member', args=[1, 'Test Group']))
        self.assertEqual(response.status_code, 404)
    
    def test_user_not_admin(self):
        user = User.objects.get(username='testcase')
        organization = Organization.objects.create(name='Test Group')
        Membership.objects.create(member=user, organization=organization, status='member', invited_email_address='test@email.com')
        self.client.login(username='testcase', password='rfg5Hiu&Eq')
        response = self.client.post(reverse('invite_member', args=[1, 'Test Group']), {'invite': 'testinvitee'})
        self.assertContains(response, 'Only admin can invite members', status_code=200)
    
    def test_get_method(self):
        Organization.objects.create(name='Test Group')
        self.client.login(username='testcase', password='rfg5Hiu&Eq')
        response = self.client.get(reverse('invite_member', args=[1, 'Test Group']))
        self.assertContains(response, 'Must go to group page to invite members', status_code=200)

    def test_invalid_invitee_username(self):
        user = User.objects.get(username='testcase')
        organization = Organization.objects.create(name='Test Group')
        Membership.objects.create(member=user, organization=organization, status='admin', invited_email_address='test@email.com')
        self.client.login(username='testcase', password='rfg5Hiu&Eq')
        response = self.client.post(reverse('invite_member', args=[1, 'Test Group']), {'invitee_username': 'testinvitee'})
        self.assertRedirects(response, reverse('view_group', args=[1, 'Test Group']))
    
    def test_valid_invitee_username(self):
        invitee = User.objects.create_user(username='testinvitee', password='tyU&e3Fdew')
        Account.objects.create(first_name='Test', last_name='Invitee', owner=invitee)
        user = User.objects.get(username='testcase')
        organization = Organization.objects.create(name='Test Group')
        Membership.objects.create(member=user, organization=organization, status='admin', invited_email_address='test@email.com')
        self.client.login(username='testcase', password='rfg5Hiu&Eq')
        response = self.client.post(reverse('invite_member', args=[1, 'Test Group']), {'invitee_username': 'testinvitee'})
        self.assertRedirects(response, reverse('view_group', args=[1, 'Test Group']))


class ViewGroupViewTest(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        user = User.objects.create_user(username='testcase', password='rfg5Hiu&Eq')
        Account.objects.create(first_name='Test', last_name='User', owner=user)
    
    def test_group_does_not_exist(self):
        self.client.login(username='testcase', password='rfg5Hiu&Eq')
        response = self.client.get(reverse('view_group', args=[1, 'Test_Group']))
        self.assertEqual(response.status_code, 404)
    
    def test_group_exists_uninvited_user(self):
        Organization.objects.create(name='Test_Group')
        self.client.login(username='testcase', password='rfg5Hiu&Eq')
        response = self.client.get(reverse('view_group', args=[1, 'Test_Group']))
        self.assertContains(response, 'Access denied', status_code=200)
    
    def test_group_exists_invited_user(self):
        user = User.objects.get(username='testcase')
        organization = Organization.objects.create(name='Test_Group')
        Membership.objects.create(member=user, organization=organization, status='invited')
        self.client.login(username='testcase', password='rfg5Hiu&Eq')
        response = self.client.get(reverse('view_group', args=[1, 'Test_Group']))
        self.assertContains(response, 'Access denied', status_code=200)

    def test_group_exists_admin_user(self):
        user = User.objects.get(username='testcase')
        organization = Organization.objects.create(name='Test_Group')
        Membership.objects.create(member=user, organization=organization, status='admin')
        self.client.login(username='testcase', password='rfg5Hiu&Eq')
        response = self.client.get(reverse('view_group', args=[1, 'Test_Group']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'banking_app/view_group.html')

    def test_group_exists_member_user(self):
        user = User.objects.get(username='testcase')
        organization = Organization.objects.create(name='Test_Group')
        Membership.objects.create(member=user, organization=organization, status='member')
        self.client.login(username='testcase', password='rfg5Hiu&Eq')
        response = self.client.get(reverse('view_group', args=[1, 'Test_Group']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'banking_app/view_group.html')

    def test_view_group_displays_members(self):
        user = User.objects.get(username='testcase')
        organization = Organization.objects.create(name='Test Group')
        Membership.objects.create(member=user, organization=organization, status='member')
        self.client.login(username='testcase', password='rfg5Hiu&Eq')
        response = self.client.get(reverse('view_group', args=[1, 'Test Group']))
        self.assertContains(response, 'Test User', status_code=200)

    def test_view_group_displays_admins(self):        
        user = User.objects.get(username='testcase')
        organization = Organization.objects.create(name='Test Group')
        Membership.objects.create(member=user, organization=organization, status='admin')
        self.client.login(username='testcase', password='rfg5Hiu&Eq')
        response = self.client.get(reverse('view_group', args=[1, 'Test Group']))
        self.assertContains(response, 'Test User', status_code=200)

    def test_view_group_does_not_display_invited(self):
        user = User.objects.get(username='testcase')
        organization = Organization.objects.create(name='Test Group')
        Membership.objects.create(member=user, organization=organization, status='invited')
        self.client.login(username='testcase', password='rfg5Hiu&Eq')
        response = self.client.get(reverse('view_group', args=[1, 'Test Group']))
        self.assertNotContains(response, 'Test User', status_code=200)

    def test_displays_invite_members_form_if_admin(self):
        user = User.objects.get(username='testcase')
        organization = Organization.objects.create(name='Test Group')
        Membership.objects.create(member=user, organization=organization, status='admin')
        self.client.login(username='testcase', password='rfg5Hiu&Eq')
        response = self.client.get(reverse('view_group', args=[1, 'Test Group']))      
        self.assertContains(response, 'Invite member', status_code=200)  
    
    def test_does_not_display_invite_members_if_member(self):
        user = User.objects.get(username='testcase')
        organization = Organization.objects.create(name='Test Group')
        Membership.objects.create(member=user, organization=organization, status='member')
        self.client.login(username='testcase', password='rfg5Hiu&Eq')
        response = self.client.get(reverse('view_group', args=[1, 'Test Group']))      
        self.assertNotContains(response, 'Invite member', status_code=200)
    
    def test_does_not_display_invite_members_if_invited(self):
        user = User.objects.get(username='testcase')
        organization = Organization.objects.create(name='Test Group')
        Membership.objects.create(member=user, organization=organization, status='invited')
        self.client.login(username='testcase', password='rfg5Hiu&Eq')
        response = self.client.get(reverse('view_group', args=[1, 'Test Group']))      
        self.assertNotContains(response, 'Invite member', status_code=200)



