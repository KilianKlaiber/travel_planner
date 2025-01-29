from .models import CustomUser, Destination, Activity, Comment, TravelPlan
import django_filters.rest_framework as filters

SEX_CHOICES = [
    ("M", "Male"),
    ("F", "Female"),
    ("O", "Other"),
]


class CustomUserFilter(filters.FilterSet):
    dob_gte = filters.DateFilter(field_name="birthdate", lookup_expr="gte")
    dob_lte = filters.DateFilter(field_name="birthdate", lookup_expr="lte")
    sex = filters.TypedChoiceFilter(field_name="sex", choices=SEX_CHOICES)
    favourite_landmark = filters.CharFilter(
        field_name="favourite_destination__landmark", lookup_expr="contains"
    )
    favourite_country = filters.CharFilter(
        field_name="favourite_destination__country", lookup_expr="contains"
    )

    class Meta:
        model = CustomUser
        fields = {
            "username": ["exact", "contains", "startswith"],
            "bio": ["exact", "contains", "startswith"],
        }


class DestinationFilter(filters.FilterSet):
    class Meta:
        model = Destination
        fields = {
            "landmark": ["exact", "contains", "startswith"],
            "country": ["exact", "contains", "startswith"],
        }


class ActivityFilter(filters.FilterSet):
    class Meta:
        model = Activity
        fields = {
            "activity_name": ["exact", "contains", "startswith"],
            "description": ["exact", "contains", "startswith"],
        }


class CommentFilter(filters.FilterSet):
    author = filters.CharFilter(
        field_name="user__username", lookup_expr="contains"
    )
    landmark = filters.CharFilter(
        field_name="destination__landmark", lookup_expr="contains"
    )
    country = filters.CharFilter(
        field_name="destination__country", lookup_expr="contains"
    )
    travel_plan = filters.CharFilter(
        field_name="travel_plan__plan_name", lookup_expr="contains"
    )
    activity = filters.CharFilter(
        field_name="activity__activity_name", lookup_expr="contains"
    )

    class Meta:
        model = Comment
        fields = {"comment_name": ["exact", "contains", "startswith"]}


class TravelPlanFilter(filters.FilterSet):
    author = filters.CharFilter(
        field_name="user__username", lookup_expr="contains"
    )
