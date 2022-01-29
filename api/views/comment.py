from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..serializers.comment import CommentSerializer
from ..models import Comment, Post


class CommentAllView(ListAPIView):
    lookup_field = 'slug'
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_slug = self.kwargs['slug']
        queryset = Comment.objects.filter(post__slug=post_slug)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response({'detail': 'Something went wrong!'})


class CreateCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        post_id = get_object_or_404(Post, slug=slug).id
        user = request.user
        description = request.POST.get('description')

        try:
            comment = Comment(user=user, post_id=post_id, description=description)
            comment.save()
            return JsonResponse(comment, safe=False)
        except:
            response = {'detail': 'Something went wrong!'}
            return JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        comment = get_object_or_404(Comment, id=id, user=request.user)
        comment.delete()
        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)
