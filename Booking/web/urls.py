from django.urls import path
from web.views import MainPage, Logout


urlpatterns = [
    path("", MainPage.as_view(), name="main"),
    path("logout/", Logout.as_view(), name="logout")
]