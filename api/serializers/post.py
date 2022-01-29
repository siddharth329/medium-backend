from django.db.models import Q
from rest_framework import serializers
from user.models import User, FULL_USER_PROFILE
from ..models import Post, Upvote
from ..serializers.tag import TagSerializer


class PostAllSerializer(serializers.ModelSerializer):
    class PostAllProfileSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['name', 'email', 'profile_image']

    tags = TagSerializer(many=True, read_only=True)
    user = PostAllProfileSerializer(read_only=True)
    api_by = serializers.SerializerMethodField()

    class Meta:
        model = Post
        # fields = '__all__'
        exclude = ['updated_at', 'created_at']
        read_only_fields = [
            'user',
            'slug',
            'upvote_count',
            'comment_count',
            'read_time',
            'published_at',
        ]

    def get_api_by(self, obj):
        return 'Siddharth Agrawal'


class PostSerializer(serializers.ModelSerializer):
    class PostProfileSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = FULL_USER_PROFILE

    tags = TagSerializer(many=True, read_only=True)
    user = PostProfileSerializer(read_only=True)
    meta = serializers.SerializerMethodField()

    class Meta:
        model = Post
        exclude = ['updated_at', 'created_at']
        read_only_fields = [
            'user',
            'slug',
            'upvote_count',
            'comment_count',
            'read_time',
            'published_at',
        ]

    def get_meta(self, obj):
        meta = {
            'user': False,
            'upvote': False
        }

        if self.context['request'] and self.context['request'].user:
            current_user = self.context['request'].user

            if obj.user.id == current_user.id:
                meta['user'] = True
            if Upvote.objects.filter(Q(post_id=obj.id) & Q(user_id=current_user.id)).exists():
                meta['upvote'] = True

        return meta

    # def create(self, validated_data):
    #     data = validated_data
    #     data['user'] = self.context['request'].user
    #     return Post(**validated_data)

# class PostCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         read_only_fields = ()
