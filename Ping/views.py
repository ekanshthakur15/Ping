from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Pings
from .forms import PingForm
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse

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

def ping_view(request, pk):
    post = get_object_or_404(Pings, pk = pk)
    total_likes = post.total_likes()
    liked = False
    if post.likes.filter(id = request.user.id).exists():
        liked = True
    if request.method == "POST":
        if('delete' in request.POST):
            post.delete()
            return redirect('dashboard')
        if ('delete_comment' in request.POST):
            comment_id = int(request.POST['delete_comment'])
            post.children.filter(id = comment_id).delete()
            return redirect('ping_detail', pk = pk)
        form = PingForm(request.POST or None)
        if form.is_valid():
            comment = form.save(commit= False)
            comment.user = request.user
            comment.parent = post
            comment.save()
            return redirect("ping_detail", pk = post.pk)
    else:
        form = PingForm()
    context = {
        "post" : post,
        "form" : form,
        "total_likes" : total_likes,
        "liked" : liked,
        }
    return render(request, "ping_detail.html", context)

def like_view(request, pk):
    post = get_object_or_404( Pings, id = request.POST.get('ping_id'))
    liked = False
    if post.likes.filter(id = request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('ping_detail', args=[str(pk)]))
