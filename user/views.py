from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserTokenObtainPairSerializer, UserSerializer
from .models import User
from api.models import Post


# Create your views here.


class CurrentUserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data, safe=False)


class UserProfile(APIView):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data, safe=False)


class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer
