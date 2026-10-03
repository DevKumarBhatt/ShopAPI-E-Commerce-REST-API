# from django.contrib.auth import get_user_model
# from rest_framework import serializers

# User = get_user_model()


# class RegisterSerializer(serializers.ModelSerializer):

#     password = serializers.CharField(
#         write_only=True,
#         min_length=8
#     )

#     class Meta:
#         model = User
#         fields = [
#             "username",
#             "email",
#             "password",
#             "first_name",
#             "last_name",
#         ]

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data["username"],
#             email=validated_data["email"],
#             password=validated_data["password"],
#             first_name=validated_data.get("first_name", ""),
#             last_name=validated_data.get("last_name", ""),
#         )

#         return user
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
        ]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )

        return user