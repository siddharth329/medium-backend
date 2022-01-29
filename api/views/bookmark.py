from django.shortcuts import get_object_or_404
from django.http.response import JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..models import Post, Bookmark
from ..serializers.bookmark import BookmarkAllSerializer


class BookmarkHandlerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        user = request.user

        try:
            upvote = Bookmark.objects.filter(user=user, post=post).exists()
            if upvote:
                Bookmark.objects.get(user=user, post=post).delete()
                response = {'detail': 'Bookmark Deletion Success'}
            else:
                upvote = Bookmark(user=user, post=post)
                upvote.save()
                response = {'detail': 'Bookmark Creation Success'}
            return JsonResponse(response, safe=False)

        except:
            response = {'detail': 'Something went wrong!'}
            return JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserBookmarksListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookmarkAllSerializer

    def get_queryset(self):
        user = self.request.user
        query_set = Bookmark.objects.filter(user=user)
        return query_set

