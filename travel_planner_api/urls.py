from django.urls import path
from .views import *

urlpatterns = [
    path("users/", CustomUserListView.as_view(), name="users-list"),
    path(
        "users/<int:pk>/", CustomUserDetailView.as_view(), name="user-details"
    ),
    path("activities/", ActivityListView.as_view(), name="activities-list"),
    path(
        "activities/<int:pk>/",
        ActivityDetailView.as_view(),
        name="activity-details",
    ),
    path(
        "destinations/",
        DestinationListView.as_view(),
        name="destinations-list",
    ),
    path(
        "destinations/<int:pk>/",
        DestinationDetailView.as_view(),
        name="destination-details",
    ),
    path(
        "travelplans/", TravelPlanListView.as_view(), name="travelplans-list"
    ),
    path(
        "travelplans/<int:pk>/",
        TravelPlanDetailView.as_view(),
        name="travelplan-details",
    ),
    path("comments/", CommentListView.as_view(), name="comments-list"),
    path(
        "comments/<int:pk>/",
        CommentDetailView.as_view(),
        name="comment-details",
    ),
    path("login/", LoginView.as_view(), name="user-login"),
    path("logout/", LogoutView.as_view(), name="user-logout"),
]
