from rest_framework.serializers import ModelSerializer
from .models import User
from django.contrib.auth.hashers import make_password


class UserRegistrationSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'firstName', 'lastName', 'fullName', 'password', 'email',
                  'mobileNo', 'profileImage', 'deviceType', 'genderType', 'lat', 'lng', 'zipCode',
                  'dateOfBirth']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        if "deviceToken" in validated_data:
            deviceToken = validated_data['deviceToken']
        else:
            deviceToken = None
        if "mobileNo" in validated_data:
            mobileNo = validated_data['mobileNo']
        else:
            mobileNo = None

        if "genderType" in validated_data:
            genderType = validated_data['genderType']
        else:
            genderType = None

        if "lat" in validated_data:
            lat = validated_data['lat']
        else:
            lat = None

        if "lng" in validated_data:
            lng = validated_data['lng']
        else:
            lng = None

        user = User.objects.create(
            firstName=validated_data['firstName'],
            lastName=validated_data['lastName'],
            fullName=validated_data["fullName"],
            email=validated_data['email'],
            password=make_password(validated_data['password']),
            mobileNo=mobileNo,
            deviceType=validated_data['deviceType'],
            genderType=genderType,
            lat=lat,
            lng=lng,
            zipCode=validated_data["zipCode"],
            dateOfBirth=validated_data['dateOfBirth']
        )
        return user
