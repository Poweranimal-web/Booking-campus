from django.urls import path
from web.views import MainPage, Logout, ProfilePage,ApplicationsPage


urlpatterns = [
    path("", MainPage.as_view(), name="main"),
    path("logout/", Logout.as_view(), name="logout"),
    path("admin-lite/profile/", ProfilePage.as_view(), name="profile"),
    path("admin-lite/applications/", ApplicationsPage.as_view(), name="application"),
]