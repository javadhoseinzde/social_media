from rest_framework.views import APIView
from posts.serializers.post_serializer import PostSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from Temp.message import result_message, duplicate_field_error_message

class PostApi(APIView):
    def get(self):
        pass

    def post(self):
        pass

class PostDetailApi(APIView):
    def get(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass