from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import JSONParser
import io
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from auth_APIs.models import User, Hobbies, UserHobbies, GoalSettings, UserGoalSettings, \
    WorkoutPreferences, UserWorkoutPreferences, DietaryPreferences, UserDietaryPreferences
from .serializers import UserRegistrationSerializer, HobbiesSerializer, GoalSettingsSerializer, \
    WorkoutPreferencesSerializer, DietaryPreferencesSerializer, UserDetailsSerializer, UserSearchDetailsSerializer
import pgeocode
import math
from django.db.models import Q
from django.contrib.auth.models import update_last_login
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework import filters


class UserRegistrationView(CreateAPIView):
    UserRegistrationSerializer = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            pythonData = JSONParser().parse(io.BytesIO(request.body))
            deviceType = pythonData.get('deviceType', False)
            email = pythonData.get('email', False)
            mobileNo = pythonData.get('mobileNo', False)
            password = pythonData.get('password', False)
            zipCode = pythonData.get('zipCode')
            userHobbies = pythonData.get('hobbies')
            userGoals = pythonData.get('goals')
            userWorkoutPreferences = pythonData.get('workoutPreferences')
            userDietaryPreferences = pythonData.get('dietaryPreferences')

            userCheck = User.objects.filter(
                Q(email=email) | Q(mobileNo=mobileNo)).first()
            if userCheck:
                response = {
                    "error": {
                        "errorCode": 500,
                        "statusCode": status.HTTP_422_UNPROCESSABLE_ENTITY,
                        "errorMessage": "User email/mobile number already registered"
                    },
                    "response": None
                }
                return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            if not email:
                response = {
                    "error": {
                        "errorCode": 502,
                        "statusCode": status.HTTP_422_UNPROCESSABLE_ENTITY,
                        "errorMessage": "Email field is required!"
                    },
                    "response": None
                }
                return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            if not mobileNo:
                response = {
                    "error": {
                        "errorCode": 503,
                        "statusCode": status.HTTP_422_UNPROCESSABLE_ENTITY,
                        "errorMessage": "mobileNo field is required!"
                    },
                    "response": None
                }
                return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            if not password:
                response = {
                    "error": {
                        "errorCode": 504,
                        "statusCode": status.HTTP_422_UNPROCESSABLE_ENTITY,
                        "errorMessage": "password field is required!"
                    },
                    "response": None
                }
                return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            if deviceType != 1 and deviceType != 2:
                response = {
                    "error": {
                        "errorCode": 505,
                        "statusCode": status.HTTP_422_UNPROCESSABLE_ENTITY,
                        "errorMessage": "Invalid deviceType"
                    },
                    "response": None
                }
                return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            if not zipCode:
                response = {
                    "error": {
                        "errorCode": 506,
                        "statusCode": status.HTTP_422_UNPROCESSABLE_ENTITY,
                        "errorMessage": "Zip code field is required!"
                    },
                    "response": None
                }
                return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            pythonData["fullName"] = str(
                pythonData["firstName"] + " " + pythonData["lastName"])

            nomi = pgeocode.Nominatim('us')
            resData = nomi.query_postal_code(zipCode)
            if math.isnan(resData.latitude):
                response = {
                    "error": {
                        "errorCode": 505,
                        "statusCode": status.HTTP_422_UNPROCESSABLE_ENTITY,
                        "errorMessage": "Invalid zip code!"
                    },
                    "response": None
                }
                return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            pythonData["lat"] = resData.latitude
            pythonData['lng'] = resData.longitude

            serializer = UserRegistrationSerializer(data=pythonData)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                if user is not None:
                    for hobbyId in userHobbies:
                        userHobby = Hobbies.objects.filter(id=hobbyId).first()
                        UserHobbies.objects.create(userId=user, hobbyId=userHobby)

                    for goalId in userGoals:
                        userGoalSetting = GoalSettings.objects.filter(id=goalId).first()
                        UserGoalSettings.objects.create(userId=user, goalSettingsId=userGoalSetting)

                    for dietPreId in userDietaryPreferences:
                        userDietPre = DietaryPreferences.objects.filter(id=dietPreId).first()
                        UserDietaryPreferences.objects.create(userId=user, dietaryPreferencesId=userDietPre)

                    for workoutPreId in userWorkoutPreferences:
                        userWorkoutPre = WorkoutPreferences.objects.filter(id=workoutPreId).first()
                        UserWorkoutPreferences.objects.create(userId=user, workoutPreferencesId=userWorkoutPre)

                    data = {
                        "userId": user.id,
                        "firstName": user.firstName,
                        "lastName": user.lastName,
                        "mobileNo": user.mobileNo,
                        "email": user.email,
                        "gender": user.gender,
                        "token": str(RefreshToken.for_user(user).access_token)
                    }
                    response = {
                        "error": None,
                        "response": {
                            "data": data,
                            "message": {
                                'success': True,
                                "successCode": 101,
                                "statusCode": status.HTTP_200_OK,
                                "successMessage": "User registered successfully."
                            }
                        }
                    }
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    response = {
                        "error": {
                            "errorCode": 502,
                            "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,
                            "errorMessage": "Error while registering user. Please try again later."
                        },
                        "response": None
                    }
                return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                response = {
                    "error": {
                        "errorCode": 503,
                        "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,
                        "errorMessage": "Error while registering user. Please try again later."
                    },
                    "response": None
                }
                return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as exception:
            response = {
                "error": {
                    "errorCode": 504,
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "errorMessage": str(exception)
                },
                "response": None
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(RetrieveAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            pythonData = JSONParser().parse(io.BytesIO(request.body))
            email_mobileNo = pythonData.get(
                'mobileNo', False)
            password = pythonData.get('password', False)

            if not email_mobileNo:
                response = {
                    "error": {
                        "errorCode": 502,
                        "statusCode": status.HTTP_422_UNPROCESSABLE_ENTITY,
                        "errorMessage": "Please enter email / mobileNo / User ID and password to login!"
                    },
                    "response": None
                }
                return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            if not password:
                response = {
                    "error": {
                        "errorCode": 503,
                        "statusCode": status.HTTP_422_UNPROCESSABLE_ENTITY,
                        "errorMessage": "Please enter password to login!"
                    },
                    "response": None
                }
                return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            user = User.objects.filter(
                Q(mobileNo=email_mobileNo)).first()
            if user is None:
                response = {
                    "error": {
                        "errorCode": 504,
                        "statusCode": status.HTTP_404_NOT_FOUND,
                        "errorMessage": "User not found!"
                    },
                    "response": None
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)

            if not user.check_password(request.data['password']):
                response = {
                    "error": {
                        "errorCode": 506,
                        "statusCode": status.HTTP_401_UNAUTHORIZED,
                        "errorMessage": "Please enter correct email/mobileNo and password to login!"
                    },
                    "response": None
                }
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)

            if user.isDeleted == 1:
                response = {
                    "error": {
                        "errorCode": 507,
                        "statusCode": status.HTTP_401_UNAUTHORIZED,
                        "errorMessage": "Your account has been deleted. Please contact to admin for further assistance!"
                    },
                    "response": None
                }
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)

            if user.isActive == 0:
                response = {
                    "error": {
                        "errorCode": 508,
                        "statusCode": status.HTTP_401_UNAUTHORIZED,
                        "errorMessage": "Your account is rejected by admin, please contact to admin for futher assistance!"
                    },
                    "response": None
                }
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)

            if user.isApproved == 3:
                response = {
                    "error": {
                        "errorCode": 510,
                        "statusCode": status.HTTP_401_UNAUTHORIZED,
                        "errorMessage": "Your account is disapproved. Please contact to admin for further assistance!"
                    },
                    "response": None
                }
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)
            update_last_login(None, user)
            refresh = RefreshToken.for_user(user)
            data = {
                "userId": user.id,
                "firstName": user.firstName,
                "lastName": user.lastName,
                "mobileNo": user.mobileNo,
                "email": user.email,
                "token": str(refresh.access_token)
            }

            response = {
                "error": None,
                "response": {
                    "data": data,
                    "message": {
                        'success': True,
                        "successCode": 102,
                        "statusCode": status.HTTP_200_OK,
                        "successMessage": "Logged in successfully."
                    }
                }
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as exception:
            response = {
                "error": {
                    "errorCode": 511,
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "errorMessage": str(exception)
                },
                "response": None
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ForgetPasswordUpdate(UpdateAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            pythonData = JSONParser().parse(io.BytesIO(request.body))
            mobileNo = pythonData.get(
                'mobileNo', False)
            newPassword = pythonData.get('newPassword', False)
            if not mobileNo:
                response = {
                    "error": {
                        "errorCode": 502,
                        "statusCode": status.HTTP_422_UNPROCESSABLE_ENTITY,
                        "errorMessage": "Mobile no field is required"
                    },
                    "response": None
                }
                return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            if not newPassword:
                response = {
                    "error": {
                        "errorCode": 503,
                        "statusCode": status.HTTP_422_UNPROCESSABLE_ENTITY,
                        "errorMessage": "New password field required!"
                    },
                    "response": None
                }
                return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            user = User.objects.filter(
                Q(mobileNo=mobileNo)).first()
            if user is None:
                response = {
                    "error": {
                        "errorCode": 504,
                        "statusCode": status.HTTP_404_NOT_FOUND,
                        "errorMessage": "User not found!"
                    },
                    "response": None
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)

            if user.is_superuser == 1:
                response = {
                    "error": {
                        "errorCode": 505,
                        "statusCode": status.HTTP_404_NOT_FOUND,
                        "errorMessage": "This is admin user you can't change password"
                    },
                    "response": None
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
            user.password = make_password(newPassword)
            user.save()

            response = {
                "error": None,
                "response": {
                    "message": {
                        'success': True,
                        "successCode": 102,
                        "statusCode": status.HTTP_200_OK,
                        "successMessage": "Password changed successfully."
                    }
                }
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as exception:
            response = {
                "error": {
                    "errorCode": 511,
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "errorMessage": str(exception)
                },
                "response": None
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserDetailsView(RetrieveAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserDetailsSerializer(user)

        response = {
            "error": None,
            "response": {
                "data": serializer.data,
                "message": {
                    'success': True,
                    "successCode": 102,
                    "statusCode": status.HTTP_200_OK,
                    "successMessage": "User Detail successfully."
                }
            }
        }
        return Response(response, status=status.HTTP_200_OK)


class UserSearchDetailsView(ListCreateAPIView):
    permission_classes = (AllowAny,)

    filter_backends = (filters.SearchFilter,)
    queryset = User.objects.all()
    serializer_class = UserSearchDetailsSerializer

    def get(self, request):
        try:
            queryset = User.objects.all()
            firstName = self.request.query_params.get('firstName', None)
            lastName = self.request.query_params.get('lastName', None)
            email = self.request.query_params.get('email', None)

            if firstName is not None:
                queryset = queryset.filter(firstName=firstName)

            if lastName is not None:
                queryset = queryset.filter(lastName=lastName)

            if email is not None:
                queryset = queryset.filter(email=email)

            serializer = UserSearchDetailsSerializer(queryset, many=True)
            response = {
                    "error": None,
                    "response": {
                        "data": serializer.data,
                        "message": {
                            'success': True,
                            "successCode": 102,
                            "statusCode": status.HTTP_200_OK
                        }
                    }
                }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as exception:
            response = {
                "error": {
                    "errorCode": 511,
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "errorMessage": str(exception)
                },
                "response": None
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


