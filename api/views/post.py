from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.views import APIView
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter

from user.permissions import IsOwner
from ..models import Post
from ..serializers.post import PostAllSerializer, PostSerializer
# Create your views here.


class PostAllView(generics.ListAPIView):
    """
    All posts view
    This route is configured to provide list of all posts excluding the non published ones with pagination
    /api/posts
    /api/posts?search=query
    /api/posts?tags=id
    """
    serializer_class = PostAllSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['tags']
    search_fields = ['title', 'subtitle']

    def get_queryset(self):
        queryset = Post.objects.select_related('user').filter(published=True)
        return queryset


class PostView(generics.RetrieveAPIView):
    lookup_field = 'slug'
    queryset = Post.objects.filter(published=True)
    serializer_class = PostSerializer


class PostCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostManagementView(viewsets.ModelViewSet):
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Post.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)

# class PostManagementView(APIView):
#     permission_classes = [IsAuthenticated, IsOwner]
#
#     @staticmethod
#     def custom_get_object_or_404(self, slug):
#         try:
#             return Post.objects.get(slug=slug)
#         except Post.DoesNotExist:
#             raise Http404
#
#     def put(self, request, slug):
#         post = self.custom_get_object_or_404(self, slug=slug)
#         serializer = PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, slug):
#         post = self.custom_get_object_or_404(self, slug=slug)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
