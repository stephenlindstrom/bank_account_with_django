from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db import transaction
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import DepositForm, WithdrawForm, RegistrationForm, AccountForm

from .models import Account, Transaction

from .token import account_activation_token




@login_required
def index(request):
    try:
        account  = Account.objects.get(owner=request.user)
    
    except Account.DoesNotExist:
        return HttpResponse('No account information available')

    return render(request, "banking_app/index.html", {"account": account})

        
@login_required
def deposit(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            account = Account.objects.get(owner=request.user)
            account.balance = F("balance") + form.cleaned_data["deposit_amount"]
            with transaction.atomic():
                account.save()
                Transaction.objects.create(type='deposit', amount=form.cleaned_data["deposit_amount"], account=account)
            return redirect('index')

    else:
        form = DepositForm()
        
    return render(request, "banking_app/deposit.html", {"form": form})


@login_required
def withdraw(request):
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            account = Account.objects.get(owner=request.user)
            account.balance = account.balance - form.cleaned_data["withdraw_amount"]
            
            if account.balance < 0:
                messages.error(request, "Insufficient funds")
            
            else:
                with transaction.atomic():
                    account.save()
                    Transaction.objects.create(type='withdraw', amount=form.cleaned_data["withdraw_amount"], account=account)
                return redirect('index')
    
    else:
        form = WithdrawForm()
        
    return render(request, "banking_app/withdraw.html", {"form": form})


def signup(request):
    if request.method == 'POST':
        account_form = AccountForm(request.POST, prefix='account_form')
        registration_form = RegistrationForm(request.POST, prefix='registration_form')
        if all([account_form.is_valid(), registration_form.is_valid()]):
            user = registration_form.save(commit=False)
            user.is_active = False
            user.save()
            account = account_form.save(commit=False)
            account.owner = user
            account.save()
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email address'
            message = render_to_string('banking_app/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = registration_form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'banking_app/signup_complete.html')
    else:
        registration_form = RegistrationForm(prefix='registration_form')
        account_form = AccountForm(prefix='account_form')
    return render(request, 'banking_app/signup.html', {'registration_form': registration_form, 'account_form': account_form})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login to your account.')
    else:
        return HttpResponse('Activation link is invalid')