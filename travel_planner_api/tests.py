from django.test import TestCase

from rest_framework.test import APIClient
from .models import CustomUser, Destination, TravelPlan, Activity, Comment
from django.urls import reverse
from rest_framework import status

from django.test.utils import override_settings

# ATTENTION!!!
# postgres increments primary keys while sqlite does not.
# means: when using postgres databases the setUp will create objects with
# different primary keys when having multiple tests in a TestCase, but when
# using the default sqlite3 database, the primary key for all setUp instances
# will be 1.
# For example:
# Use "kwargs={"pk": self.travel_plan.id}" instead of "kwargs={"pk":1}"


# Create your tests here.
class UserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.favourite = {
            "landmark": "Eiffel Tower",
            "country": "France",
        }

        favourite = Destination.objects.create(**self.favourite)
        self.test_user = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
            "bio": "This is a test bio that is sufficiently long.",
            "sex": "M",
            "birthdate": "2000-01-01",
            "favourite_destination": favourite,
        }
        user = CustomUser.objects.create_user(**self.test_user)

    def test_user_creation(self):
        self.favourite = Destination(pk=1)
        self.test_user1 = {
            "username": "testuser1",
            "email": "testuser@example.com",
            "password": "testpassword",
            "bio": "This is a test bio that is sufficiently long.",
            "sex": "M",
            "birthdate": "2000-01-01",
            "favourite_destination": self.favourite,
        }

        response = self.client.post(reverse("users-list"), self.test_user1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_get_all_users(self):
        response = self.client.get(reverse("users-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_login_user(self):
        response = self.client.post(
            reverse("user-login"),
            data={"username": "testuser", "password": "testpassword"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_logout_user(self):
        response = self.client.post(
            reverse("user-login"),
            data={"username": "testuser", "password": "testpassword"},
        )
        token = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        response = self.client.post(reverse("user-logout"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Logged out successfully")
        self.assertNotIn("token", response.data)


class TravelPlanTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.favourite = {
            "landmark": "Eiffel Tower",
            "country": "France",
        }

        favourite = Destination.objects.create(**self.favourite)

        self.test_user = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
            "bio": "This is a test bio that is sufficiently long.",
            "sex": "M",
            "birthdate": "2000-01-01",
            "favourite_destination": favourite,
        }
        self.user = CustomUser.objects.create_user(**self.test_user)

        self.activity = Activity.objects.create(
            activity_name="Bungee Jumping",
            description="Jumping from towers and bridges",
        )

        self.travel_plan = TravelPlan.objects.create(
            plan_name="Jumping into oblivion", user=self.user
        )
        self.assertTrue(
            TravelPlan.objects.filter(
                plan_name="Jumping into oblivion"
            ).exists(),
            "TravelPlan was not created successfully in setUp.",
        )

    def test_a_travel_plan_login(self):
        # Testing, whether the non-permission for changing the travel plan for non-logged inusers works
        travel_plan = TravelPlan.objects.get(pk=self.travel_plan.id)
        travel_plan_dict = {
            "plan_name": travel_plan.plan_name,
            "user": self.user,
        }

        response = self.client.post(
            reverse("travelplan-details", kwargs={"pk": self.travel_plan.id}),
            **travel_plan_dict
        )
        travel_plan_name = {
            "plan_name": "travelmecrazy",
        }
        response = self.client.patch(
            reverse("travelplan-details", kwargs={"pk": self.travel_plan.id}),
            data=travel_plan_name,
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_b_update_travel_plan(self):
        # Testing, wether updating a travel plan works for a loged in user

        travel_plan = TravelPlan.objects.get(pk=self.travel_plan.id)
        travel_plan_dict = {
            "plan_name": travel_plan.plan_name,
            "user": self.user,
        }
        response = self.client.post(
            reverse("travelplan-details", kwargs={"pk": self.travel_plan.id}),
            **travel_plan_dict
        )
        login_response = self.client.post(
            reverse("user-login"),
            {"username": "testuser", "password": "testpassword"},
        )
        token = login_response.data["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        travel_plan_name = {
            "plan_name": "travelmecrazy",
        }
        response = self.client.patch(
            reverse("travelplan-details", kwargs={"pk": self.travel_plan.id}),
            data=travel_plan_name,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_c_on_delete_cascade(self):

        travel_plan = TravelPlan.objects.get(pk=self.travel_plan.id)
        travel_plan_dict = {
            "plan_name": travel_plan.plan_name,
            "user": self.user,
        }
        user = CustomUser.objects.get(pk=self.travel_plan.id)
        user.delete()
        response = self.client.get(
            reverse("travelplan-details", kwargs={"pk": self.travel_plan.id}),
            **travel_plan_dict
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CustomUserSerializerTest(TestCase):
    def test_bio_profanity_filter(self):
        user = {
            "bio": "Fuck this shit and just everything.",
            "birthdate": "1999-03-12",
            "sex": "O",
            "username": "User_1",
            "password": "user_1s_password",
            "email": "user1@examplemail.com",
        }
        response = self.client.post(reverse("users-list"), user)
        response_dict = response.__dict__
        self.assertEqual(
            response_dict["_container"][0],
            b'{"bio":["Please remove any profanity/swear words."]}',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
