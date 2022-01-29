from rest_framework import serializers
from ..models import Comment


class CommentSerializer(serializers.ModelSerializer):
    edited = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'post',
            'user',
            'description',
            'created_at',
            'edited'
        ]

    def get_edited(self, obj):
        return True if obj.created_at != obj.updated_at else False

    def get_created_at(self, obj):
        return obj.updated_at
