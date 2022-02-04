from django.shortcuts import get_object_or_404
from django.http.response import JsonResponse, Http404

from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..models import Follower
from user.models import User


class FollowerHandlerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        followed_user = get_object_or_404(User, slug=slug)
        following_user = request.user

        if followed_user.id == following_user.id:
            raise Http404

        try:
            follower = Follower.objects.filter(user=followed_user, follower=following_user).exists()
            if follower:
                Follower.objects.get(user=followed_user, follower=following_user).delete()
                followed_user.followers_count -= 1
                followed_user.save()
                following_user.following_count -= 1
                following_user.save()
                response = {'detail': False}

            else:
                follower = Follower(user=followed_user, follower=following_user)
                follower.save()
                followed_user.followers_count += 1
                followed_user.save()
                following_user.following_count += 1
                following_user.save()

                response = {'detail': True}

            return JsonResponse(response, safe=False)

        except:
            response = {'detail': 'Something went wrong!'}
            return JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class FollowerAllView(ListAPIView):
#     lookup_field = 'slug'
#     queryset = Follower.objects.all()
#     serializer_class = FollowerAllSerializer
