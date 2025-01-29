from django.shortcuts import render

from rest_framework import status

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    GenericAPIView,
)

from .models import CustomUser, Activity, Destination, TravelPlan, Comment

from .serializers import (
    CustomUserSerializer,
    ActivitySerializer,
    DestinationSerializer,
    TravelPlanSerializer,
    CommentsSerializer,
)

from .artificial_intelligence import find_country

from rest_framework.response import Response

from rest_framework.authtoken.models import Token

from rest_framework.authentication import TokenAuthentication

from django.contrib.auth import login, logout

from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly

from django_filters.rest_framework import DjangoFilterBackend

from .filters import (
    CustomUserFilter,
    ActivityFilter,
    CommentFilter,
    DestinationFilter,
    TravelPlanFilter,
)

# Imports for Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# API views for DB interaction
class CustomUserListView(ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CustomUserFilter

    @swagger_auto_schema(
        operation_description="Get the list of all users",
        responses={"200": CustomUserSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new user according to validation",
        responses={
            "201": "New User was added",
            "400": "Bad request get out of here",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomUserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    @swagger_auto_schema(
        operation_description="Get a single user by his id",
        responses={"200": CustomUserSerializer, "404": "No user found"},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a user",
        responses={
            "200": CustomUserSerializer,
            "400": "Bad request get out of here",
            "401": "Unauthorized",
            "403": "You are forbidden to do this",
        },
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a user",
        responses={
            "204": "User was deleted and there is no content",
            "401": "Unauthorized",
            "403": "You are forbidden to do this",
        },
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ActivityListView(ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ActivityFilter

    @swagger_auto_schema(
        operation_description="Get the list of all activities.",
        responses={"200": ActivitySerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new activity according to validation",
        responses={
            "201": "New Activity was added",
            "400": "Bad request get out of here",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ActivityDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    @swagger_auto_schema(
        operation_description="Get a single activity by its id",
        responses={"200": ActivitySerializer, "404": "No activity found"},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a user",
        responses={
            "200": ActivitySerializer,
            "400": "Bad request get out of here",
            "401": "Unauthorized",
            "403": "You are forbidden to do this",
        },
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete an activity",
        responses={
            "204": "Activity was deleted and there is no content.",
            "401": "Unauthorized",
            "403": "You are forbidden to do this",
        },
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class DestinationListView(ListCreateAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = DestinationFilter

    def perform_create(self, serializer):
        landmark = self.request.data["landmark"]
        country = find_country(landmark)
        serializer.save(country=country)

    @swagger_auto_schema(
        operation_description="Get the list of all destinations.",
        responses={"200": DestinationSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new destination according to validation",
        responses={
            "201": "New destination was added",
            "400": "Bad request get out of here",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DestinationDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    @swagger_auto_schema(
        operation_description="Get a single destination by his id",
        responses={
            "200": DestinationSerializer,
            "404": "No destination found",
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a destination",
        responses={
            "200": DestinationSerializer,
            "400": "Bad request get out of here",
            "401": "Unauthorized",
            "403": "You are forbidden to do this",
        },
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a destination",
        responses={
            "204": "Destination was deleted and there is no content",
            "401": "Unauthorized",
            "403": "You are forbidden to do this",
        },
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class TravelPlanListView(ListCreateAPIView):
    queryset = TravelPlan.objects.all()
    serializer_class = TravelPlanSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TravelPlanFilter

    @swagger_auto_schema(
        operation_description="Get the list of all travel plans.",
        responses={"200": TravelPlanSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new travel plan according to validation",
        responses={
            "201": "New travel plan was added",
            "400": "Bad request get out of here",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TravelPlanDetailView(RetrieveUpdateDestroyAPIView):
    queryset = TravelPlan.objects.all()
    serializer_class = TravelPlanSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    @swagger_auto_schema(
        operation_description="Get a single travel plan by its id",
        responses={"200": TravelPlanSerializer, "404": "No travel plan found"},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a user",
        responses={
            "200": TravelPlanSerializer,
            "400": "Bad request get out of here",
            "401": "Unauthorized",
            "403": "You are forbidden to do this",
        },
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a travel plan",
        responses={
            "204": "Travel plan was deleted and there is no content",
            "401": "Unauthorized",
            "403": "You are forbidden to do this",
        },
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class CommentListView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CommentFilter
    @swagger_auto_schema(
        operation_description="Get the list of all comments.",
        responses={"200": CommentsSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new comment according to validation",
        responses={
            "201": "New comment was added",
            "400": "Bad request get out of here",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CommentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    @swagger_auto_schema(
        operation_description="Get a single comment by its id",
        responses={"200": CommentsSerializer, "404": "No comment found"},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a comment",
        responses={
            "200": CommentsSerializer,
            "400": "Bad request get out of here",
            "401": "Unauthorized",
            "403": "You are forbidden to do this",
        },
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a comment",
        responses={
            "204": "Comment was deleted and there is no content",
            "401": "Unauthorized",
            "403": "You are forbidden to do this",
        },
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# login/logout views for authentication
class LoginView(GenericAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Login and generate a new token",
        responses={
            "200": "User logged in",
            "400": "Invalid credentials",
        },
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = CustomUser.objects.filter(username=username).first()
        if user and user.check_password(password):
            login(request, user)
            token = Token.objects.create(user=user)
            return Response(
                {"message": "user logged in", "token": token.key},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class LogoutView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer

    @swagger_auto_schema(
        operation_description="Logout and the token will be deleted",
        responses={"200": "User logged out"},
    )
    def post(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response(
            {"message": "Logged out successfully"}, status=status.HTTP_200_OK
        )
