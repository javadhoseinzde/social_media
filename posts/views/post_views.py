from rest_framework.views import APIView
from posts.serializers.post_serializer import *
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from Temp.message import result_message, duplicate_field_error_message

class PostApi(APIView):
    def get(self, request):
        try:
            if request.user.is_superuser:
                post = Post.objects.all()
                serializer = PostSerializer(post, many=True)
                result = result_message(
                    "OK",
                    status.HTTP_200_OK,
                    serializer.data
                )
                return Response(result, status=status.HTTP_200_OK)
            else:
                result = result_message("ERROR", status.HTTP_400_BAD_REQUEST, f"{e}")
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            result = result_message("ERROR", status.HTTP_400_BAD_REQUEST, f"{e}")
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            serializer = PostSerializer(data=request.data, context={'request': request})

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                result = result_message("CREATED",status.HTTP_201_CREATED,serializer.data)
                return Response(result, status=status.HTTP_201_CREATED)
            else:
                result = result_message("ERROR", status.HTTP_400_BAD_REQUEST, serializer.errors)
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            result = result_message("ERROR", status.HTTP_400_BAD_REQUEST, f"{e}")
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

class PostDetailApi(APIView):
    def get(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass