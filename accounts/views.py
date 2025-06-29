from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from Temp.message import result_message
from Temp.permissions import *
from .serializer import *
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, TokenError

class RegisterApi(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = InputRegisterSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                user = get_user_model().objects.create(
                    username=serializer.validated_data.get("username"),
                    name=serializer.validated_data.get("name"),
                    password=make_password(serializer.validated_data["password"]),
                    is_admin=serializer.validated_data.get("is_admin"),
                    is_superuser=serializer.validated_data.get("is_superuser"),
                    is_client_user=serializer.validated_data.get("is_client_user"),
                )

                result = result_message(
                    "CREATED",
                    status.HTTP_201_CREATED,
                    OutPutRegisterSerializer(user, context={"request": request}).data,
                )
                return Response(result, status=status.HTTP_201_CREATED)
            else:
                result = result_message(
                    "ERROR", status.HTTP_400_BAD_REQUEST, serializer.errors
                )
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            result = result_message("ERROR", status.HTTP_400_BAD_REQUEST, f"{e}")
            return Response(result, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        responses=LoginSerializer,
        request=LoginSerializer,
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
            )
            if user is not None:
                refresh = RefreshToken.for_user(user)
                message = {
                    "user_id": user.id,
                    "username": user.username,
                    "name": f'{user.name}',
                    "refresh": str(refresh),
                    "token": str(refresh.access_token),
                }
                result = result_message(
                    "OK",
                    status.HTTP_200_OK,
                    message,
                )
                return Response(result, status=status.HTTP_200_OK)
            else:
                result = result_message(
                    "نام کاربری یا رمز عبور اشتباه است.", status.HTTP_400_BAD_REQUEST, "error"
                )
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
        else:
            result = result_message(
                "error",
                status.HTTP_400_BAD_REQUEST,
                serializer.errors,
            )
            return Response(result, status=status.HTTP_400_BAD_REQUEST)