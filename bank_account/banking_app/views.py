from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

from .models import Account

@login_required
def index(request):
    account  = Account.objects.get(owner=request.user)

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    template = loader.get_template("banking_app/index.html")
    context = {
                "account": account,
                "num_visits": num_visits,
               }

    return HttpResponse(template.render(context, request))

def balance(request, account_id):
    return HttpResponse("You're looking at account %s." % account_id)
