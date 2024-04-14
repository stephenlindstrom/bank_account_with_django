from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader

from .forms import DepositForm

from .models import Account


@login_required
def index(request):
    account  = Account.objects.get(owner=request.user)

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