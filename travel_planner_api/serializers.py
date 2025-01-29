from rest_framework import serializers
from .models import CustomUser, Destination, TravelPlan, Activity, Comment
from profanity.validators import validate_is_profane


class CustomUserSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(validators=[validate_is_profane])

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "sex",
            "bio",
            "birthdate",
            "favourite_destination_id",
            "password",
        )

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate_bio(self, value):
        if len(value) < 20:
            raise serializers.ValidationError(
                "bio must be at least 20 characters"
            )
        return value
    


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ("landmark", "country")


class TravelPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelPlan
        fields = "__all__"


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = "__all__"


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
