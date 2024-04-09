from django.http import HttpResponse

def index(request):
    return HttpResponse("You're at the banking app index.")

def balance(request, account_id):
    return HttpResponse("You're looking at account %s." % account_id)
