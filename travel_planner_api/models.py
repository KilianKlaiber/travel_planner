from django.db import models
from django.contrib.auth.models import AbstractUser


class Destination(models.Model):
    landmark = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100, blank=True, null=True)


class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    SEX_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=True)

    favourite_destination = models.ForeignKey(
        Destination, on_delete=models.CASCADE, related_name="users", null=True, blank=True
    )

    def __str__(self):
        return self.username


class Activity(models.Model):
    activity_name = models.CharField(max_length=100)
    description = models.TextField()


class TravelPlan(models.Model):
    plan_name = models.CharField(max_length=100)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="travel_plans"
    )
    destinations = models.ManyToManyField(Destination)
    activities = models.ManyToManyField(Activity)


class Comment(models.Model):
    comment_name = models.CharField(max_length=100)
    text = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    travel_plan = models.ForeignKey(
        TravelPlan, on_delete=models.CASCADE, related_name="comments"
    )
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, related_name="comments"
    )
