from django.shortcuts import render, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

# Create your views here.
counter = 0

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    return render(request, "users/index.html")
    

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("users:index"))
        else:
            return render(request, "users/login.html", {
                "message": "Invalid Credentials."
            })
    return render(request, "users/login.html")


def logout_view(request):
    logout(request)
    
    return render(request, "users/login.html", {
        "message": "Logged out."
    })
    
def ban(request):
    return HttpResponse("<h1>You Are Banned<h2>")