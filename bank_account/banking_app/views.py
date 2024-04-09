from django.http import HttpResponse

from .models import Account

def index(request):
    account_list  = Account.objects.all()
    output = ", ".join([account.first_name for account in account_list])
    return HttpResponse(output)

def balance(request, account_id):
    return HttpResponse("You're looking at account %s." % account_id)
