from django.urls import path
from web.views import MainPage, Logout, ProfilePage,ApplicationsPage,ApplyPage,ApplyFloorPage, GenData,ListCampusPage


urlpatterns = [
    path("", MainPage.as_view(), name="main"),
    path("logout/", Logout.as_view(), name="logout"),
    path("admin-lite/profile/", ProfilePage.as_view(), name="profile"),
    path("admin-lite/applications/", ApplicationsPage.as_view(), name="application"),
    path("admin-lite/apply/", ApplyPage.as_view(), name="apply"),
    path("admin-lite/apply_rooms/campus/<int:pk>/", ApplyFloorPage.as_view(), name="floor"),
    path("admin-lite/apply/campuses", ListCampusPage.as_view(), name="campus")
    # path("gen/",GenData.as_view(), name="gen")
]