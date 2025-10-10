from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from Temp.message import result_message, duplicate_field_error_message
from .serializer import *
from django.db.models import Q

# Create your views here.

class ProfileApi(APIView):
    permissions = [IsAdminUser]
    def get(self, request):
        try:
            if request.user.is_superuser:
                profile =  Profile.objects.all()
                serializer = ProfileSerializer(profile, many=True)
                result = result_message(
                    "OK",
                    status.HTTP_200_OK,
                    serializer.data
                )
                return Response(result, status=status.HTTP_200_OK)
            else:
                result = result_message("ERROR", status.HTTP_400_BAD_REQUEST, "you do not have access")
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            result = result_message("ERROR", status.HTTP_400_BAD_REQUEST, f"{e}")
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        user = request.user.id
        try:
            serializer = ProfileSerializer(data=request.data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                if Profile.objects.filter(user=user):
                    result = duplicate_field_error_message(
                        "DUPLOCATED",
                        status.HTTP_400_BAD_REQUEST,
                        "A profile for this user already exists",
                    )
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)
                serializer.save()
                result = result_message("CREATED",status.HTTP_201_CREATED,serializer.data)
                return Response(result, status=status.HTTP_201_CREATED)
            else:
                result = result_message("ERROR", status.HTTP_400_BAD_REQUEST, serializer.errors)
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            result = result_message("ERROR", status.HTTP_400_BAD_REQUEST, f"{e}")
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

class ProfileDetailApi(APIView):
    def get(self, request, id):
        user = request.user.id
        try:
            profile =  Profile.objects.get(id=id)
            serializer = ProfileSerializer(profile)
            result = result_message(
                "OK",
                status.HTTP_200_OK,
                serializer.data
            )
            return Response(result, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            result = result_message(
                "NOT_FOUND",
                status.HTTP_404_NOT_FOUND,
                "Profile not found for this user."
            )
            return Response(result, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            result = result_message("ERROR", status.HTTP_400_BAD_REQUEST, f"{e}")
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        user = request.user.id

        try:
            profile = Profile.objects.get(id=id, user=user)

            serializer = ProfileSerializer(profile, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                result = result_message(
                    "UPDATED",
                    status.HTTP_200_OK,
                    serializer.data
                )
                return Response(result, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            result = result_message(
                "NOT_FOUND",
                status.HTTP_404_NOT_FOUND,
                "Profile not found."
            )
            return Response(result, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            result = result_message(
                "ERROR",
                status.HTTP_400_BAD_REQUEST,
                f"{e}"
            )
            return Response(result, status=status.HTTP_400_BAD_REQUEST)


class FollowApi(APIView):
    def post(self, request):
        user = self.request.user
        try:
            serializer = FollowSerializer(data=request.data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save(from_user=user)
            else:
                result = result_message("ERROR", status.HTTP_400_BAD_REQUEST, serializer.errors)
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            result = result_message(
                "ERROR",
                status.HTTP_400_BAD_REQUEST,
                f"{e}"
            )
            return Response(result, status=status.HTTP_400_BAD_REQUEST)



class FollowDetailView(APIView):
    def get(self, request, id):
        user = request.user
        try:
            follower = Follower.objects.filter(
                Q(id=id) & (Q(to_user=request.user) | Q(from_user=request.user))
            )
            serializer = FollowerSerializer(follower, many=True, context={'request': request}).data
            result = result_message(
                "OK",
                status.HTTP_200_OK,
                {
                    "result": serializer,
                }
            )
            return Response(result, status=status.HTTP_200_OK)
        except Follower.DoesNotExist:
            result = result_message(
                "NOT_FOUND",
                status.HTTP_404_NOT_FOUND,
                "Follower not found."
            )
            return Response(result, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            result = result_message(
                "ERROR",
                status.HTTP_400_BAD_REQUEST,
                f"{e}"
            )
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            follower = Follower.objects.get(id=id)
            serializer = FollowerSerializer(follower, context={'request': request}).data
            follower.delete()

            result = result_message(
                "OK",
                status.HTTP_200_OK,
                {
                    "message": "Follower deleted successfully.",
                    "deleted_data": serializer
                }
            )
            return Response(result, status=status.HTTP_200_OK)
        except Follower.DoesNotExist:
            result = result_message(
                "NOT_FOUND",
                status.HTTP_404_NOT_FOUND,
                "Follower not found."
            )
            return Response(result, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            result = result_message(
                "ERROR",
                status.HTTP_400_BAD_REQUEST,
                f"{e}"
            )
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
class FollowListApi(APIView):
    def get(self, request):
        user = request.user
        try:
            followers = user.followers.all()
            followings = user.following.all()

            followers_serialized = FollowerSerializer(followers, many=True, context={'request': request}).data
            followings_serialized = FollowerSerializer(followings, many=True, context={'request': request}).data

            result = result_message(
                "OK",
                status.HTTP_200_OK,
                {
                    "followers": followers_serialized,
                    "followings": followings_serialized
                }
            )
            return Response(result, status=status.HTTP_200_OK)


        except Follower.DoesNotExist:
            result = result_message(
                "NOT_FOUND",
                status.HTTP_404_NOT_FOUND,
                "Follower not found."
            )
            return Response(result, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            result = result_message(
                "ERROR",
                status.HTTP_400_BAD_REQUEST,
                f"{e}"
            )
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
