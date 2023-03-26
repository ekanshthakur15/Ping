from django.urls import path
from .views import dashboard, profile_list, profile, search, ping_view, like_view


urlpatterns = [
    path('',dashboard, name = "dashboard"),
    path('profile_list/', profile_list, name = "profile_list"),
    path('profile/<int:pk>', profile, name = 'profile'),
    path('search/', search, name = 'search'),
    path("ping_detail/<int:pk>", ping_view, name = 'ping_detail'),
    path('like/<int:pk>', like_view, name = 'ping_liked')
]