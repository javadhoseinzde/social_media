from rest_framework.views import APIView
from Temp.permissions import IsSuperUser
from posts.serializers.post_serializer import *
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from Temp.message import result_message, duplicate_field_error_message

class PostApi(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if not request.user.is_superuser:
            result = result_message(
                "ERROR",
                status.HTTP_403_FORBIDDEN,
                "You do not have access"
            )
            return Response(result, status=status.HTTP_403_FORBIDDEN)

        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True, context={"request": request})
        result = result_message(
            "OK",
            status.HTTP_200_OK,
            serializer.data
        )
        return Response(result, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = PostSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        result = result_message("CREATED", status.HTTP_201_CREATED, serializer.data)
        return Response(result, status=status.HTTP_201_CREATED)

class PostDetailApi(APIView):
    def get(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass