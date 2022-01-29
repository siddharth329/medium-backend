from rest_framework import serializers
from ..models import Bookmark
from ..serializers.post import PostAllSerializer


class BookmarkAllSerializer(serializers.ModelSerializer):
    post = PostAllSerializer(read_only=True)

    class Meta:
        model = Bookmark
        fields = '__all__'
