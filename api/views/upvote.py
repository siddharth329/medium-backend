from django.shortcuts import get_object_or_404
from django.http.response import JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..models import Post, Upvote


class UpvoteHandlerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        user = request.user

        try:
            upvote = Upvote.objects.filter(user=user, post=post).exists()
            if upvote:
                Upvote.objects.get(user=user, post=post).delete()
                response = {'detail': 'Upvote Delete Success'}
            else:
                upvote = Upvote(user=user, post=post)
                upvote.save()
                response = {'detail': 'Upvote Success'}
            return JsonResponse(response, safe=False)

        except:
            response = {'detail': 'Something went wrong!'}
            return JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
