from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

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
    return render(request, "banking_app/register.html")

def registered(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        return HttpResponse(username)
