from django.shortcuts import render, redirect
from .models import Profile, Pings
from .forms import PingForm
from django.db.models import Q

# Create your views here.
def dashboard(request):
    form = PingForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            pings = form.save(commit=False)
            pings.user = request.user
            pings.save()
            return redirect("dashboard")
    return render(request, "dashboard.html", {"form" : form})

def profile_list(request):
    profiles = Profile.objects.exclude(user = request.user)
    return render(request, "profile_list.html", {"profiles" : profiles})

def profile(request,pk ):

    if not hasattr(request.user , 'profile'):
        missing_profile = Profile(user = request.user)
        missing_profile.save()


    profile = Profile.objects.get(pk=pk)
    #profile.followed_by.count
    if request.method == 'POST':
        current_user_profile = request.user.profile
        action = request.POST.get("follows")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow" :
            current_user_profile.follows.remove(profile)
        current_user_profile.save()

    return render(request, 'profile.html', {"profile" : profile})

def search(request):
    result = []
    if request.method == 'GET':
        query = request.GET.get('searched')
        if query == '':
            query =  None
        result = Profile.objects.filter(Q(user__username__icontains = "" if query is None else query))
    return render(request, "search.html", {"query" :query , "result" :
                                           result})