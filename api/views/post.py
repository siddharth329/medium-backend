from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter

from user.models import User
from user.permissions import IsOwner
from ..models import Post, Follower, View
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

    def get_serializer_context(self):
        context = super(PostAllView, self).get_serializer_context()
        context.update({"request": self.request})
        return context


class PostView(generics.RetrieveAPIView):
    lookup_field = 'slug'
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get_queryset(self):
        post = Post.objects.get(slug=self.kwargs['slug'])
        print(post)
        if post:
            View.objects.create(post=post)
        queryset = Post.objects.all()
        return queryset

    def get_serializer_context(self):
        context = super(PostView, self).get_serializer_context()
        context.update({"request": self.request})
        return context


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
    serializer_class = PostSerializer
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


class PostByUserAllView(generics.ListAPIView):
    """
    All posts by authenticated user view
    This route is configured to provide list of all posts by authenticated user
    excluding the non published ones with pagination
    /api/posts
    /api/post_by_user?published=boolean
    /api/post_by_user?title=query
    /api/post_by_user?subtitle=query
    """
    serializer_class = PostAllSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['published']
    search_fields = ['title', 'subtitle']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Post.objects.filter(user=self.request.user)
        return queryset


class PostByFollowingUser(generics.ListAPIView):
    """
    All posts by users whom the request user follows
    /api/post_by_following_user
    """
    serializer_class = PostAllSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        following = Follower.objects.filter(follower=self.request.user)
        users = User.objects.filter(user__in=following)
        queryset = Post.objects.filter(user__in=users, published=True)
        return queryset


class PostTrending(generics.ListAPIView):
    """
    All posts which are trending
    /api/post_by_following_user
    """
    serializer_class = PostAllSerializer

    def get_queryset(self):
        views = View.objects \
            .filter(time__gte=(timezone.now() - timezone.timedelta(days=7))) \
            .values('post__slug') \
            .annotate(count=Count('post__slug'))

        views_array = [x['post__slug'] for x in views]
        print(views_array)
        queryset = Post.objects.filter(published=True).filter(slug__in=views_array)
        return queryset
        # views = View.objects \
        #     .filter(time__gte=(timezone.now() - timezone.timedelta(days=7))) \
        #     .values('post__slug') \
        #     .annotate(count=Count('post__slug')) \
        #     .order_by('-count')
        #
        # views_array = [x['post__slug'] for x in views]

        # return queryset
