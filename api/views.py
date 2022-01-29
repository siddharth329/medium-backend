from django.http.response import HttpResponse
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from .models import Post
# from .serializers import PostSerializer
# Create your views here.


# class PostsView(APIView, LimitOffsetPagination):
#     permission_classes = [IsAuthenticated]

#
# class PostView(generics.ListAPIView):
#     queryset = Post.objects.select_related('user').all()
#     serializer_class = PostSerializer
