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
                    email=serializer.validated_data.get("email"),
                    phone_number=serializer.validated_data.get("phone_number"),
                    picture=serializer.validated_data.get("picture"),
                    is_admin=serializer.validated_data.get("is_admin"),
                    is_superuser=serializer.validated_data.get("is_superuser"),
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
