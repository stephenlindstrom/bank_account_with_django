from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .exceptions import InsufficientFundsException

from .forms import DepositForm, WithdrawForm, RegistrationForm, AccountForm

from .models import Account

from .token import account_activation_token




@login_required
def index(request):
    try:
        account  = Account.objects.get(owner=request.user)
    except Account.DoesNotExist:
        return HttpResponse('No account information available')
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
                "account": account,
                "num_visits": num_visits,
               }

    return render(request, "banking_app/index.html", context)


def balance(request, account_id):
    return HttpResponse("You're looking at account %s." % account_id)


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        if password != confirm_password:
            return HttpResponse("Passwords do not match.")
        else:
            User = get_user_model()
            user = User.objects.create_user(username, '', password)
            Account.objects.create(first_name=first_name, last_name=last_name, balance = 0, owner = user)
            messages.success(request, "New account registered.")
            return redirect('login')
    else:
        return render(request, "banking_app/register.html")
        
@login_required
def deposit(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            account = Account.objects.get(owner=request.user)
            account.balance = F("balance") + form.cleaned_data["deposit_amount"]
            account.save()
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
            
            try:
                if account.balance < 0:
                    raise InsufficientFundsException ("Insufficient funds")
                else:
                    account.save()
                    return redirect('index')
            
            except InsufficientFundsException:
                messages.error(request, "Insufficient funds")
    else:
        form = WithdrawForm()
        
    return render(request, "banking_app/withdraw.html", {"form": form})

def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email address'
            message = render_to_string('banking_app/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        registration_form = RegistrationForm()
        account_form = AccountForm()
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
        #Account.objects.create(first_name=first_name, last_name=last_name, balance = 0, owner = user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid')