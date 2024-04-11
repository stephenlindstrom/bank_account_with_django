from django.http import HttpResponse
from django.template import loader

from .models import Account

def index(request):
    account_list  = Account.objects.all()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    template = loader.get_template("banking_app/index.html")
    context = {
                "account_list": account_list,
                "num_visits": num_visits,
               }

    return HttpResponse(template.render(context, request))

def balance(request, account_id):
    return HttpResponse("You're looking at account %s." % account_id)
