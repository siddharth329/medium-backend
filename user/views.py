from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserTokenObtainPairSerializer, UserSerializer
from .models import User
from api.models import Post


# Create your views here.


class UserProfile(APIView):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data, safe=False)


class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer
