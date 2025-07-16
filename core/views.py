from utils.funcs import get_ip
from django.shortcuts import render
from django.http.request import HttpRequest
from .models import ArmyPerson, Rank, Branch
from django.http.response import HttpResponse

# Create your views here.

def home(request: HttpRequest) -> HttpResponse:
    saved_users = ArmyPerson.objects.all()
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
