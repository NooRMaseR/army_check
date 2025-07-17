from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from utils.funcs import get_ip, superuser_requierd
from .models import ArmyPerson, PendingRequest, Rank, Branch, RequestStatus

# Create your views here.

def home(request: HttpRequest) -> HttpResponse:
    saved_users = ArmyPerson.objects.prefetch_related("request").order_by("request__accepted")
    ranks = Rank.objects.all()
    branches = Branch.objects.all()
    return render(
        request, 
        "home.html", 
        {
            "local_ip": get_ip(), 
            "users": saved_users,
            "ranks": ranks,
            "branches": branches
        }
    )

@superuser_requierd
def manager(request: HttpRequest) -> HttpResponse:
    requests = PendingRequest.objects.select_related("user").filter(accepted = RequestStatus.PENDING)
    return render(
        request, 
        "manager.html", 
        {
            "local_ip": get_ip(), 
            "requests": requests,
        }
    )

