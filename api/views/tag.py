from rest_framework import generics
from rest_framework.filters import SearchFilter
from ..models import Tag
from ..serializers.tag import TagSerializer
# Create your views here.


class TagAllView(generics.ListAPIView):
    """
    All posts view
    This route is configured to provide list of all posts excluding the non published ones with pagination
    /api/tags
    /api/tags?search=query
    """
    serializer_class = TagSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        queryset = Tag.objects.all()
        return queryset