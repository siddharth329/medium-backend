from django.db.models import Q
from rest_framework import serializers
from user.models import User, FULL_USER_PROFILE
from ..models import Post, Upvote, Tag, Bookmark
from ..serializers.tag import TagSerializer


class PostAllSerializer(serializers.ModelSerializer):
    class PostAllProfileSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['name', 'email', 'slug', 'profile_image']

    tags = TagSerializer(many=True, read_only=True)
    user = PostAllProfileSerializer(read_only=True)
    meta = serializers.SerializerMethodField()
    api_by = serializers.SerializerMethodField()

    class Meta:
        model = Post
        # fields = '__all__'
        exclude = ['content', 'created_at']
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
            'upvote': False,
            'bookmark': False
        }

        if self.context['request'] and self.context['request'].user:
            current_user = self.context['request'].user

            if obj.user.id == current_user.id:
                meta['user'] = True
            if Upvote.objects.filter(Q(post_id=obj.id) & Q(user_id=current_user.id)).exists():
                meta['upvote'] = True
            if Bookmark.objects.filter(Q(post_id=obj.id) & Q(user_id=current_user.id)).exists():
                meta['bookmark'] = True

        return meta


    def get_api_by(self, obj):
        return 'Siddharth Agrawal'


class PostSerializer(serializers.ModelSerializer):
    class PostProfileSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = FULL_USER_PROFILE

    tags = TagSerializer(many=True)
    user = PostProfileSerializer(read_only=True)
    meta = serializers.SerializerMethodField()
    related = serializers.SerializerMethodField(read_only=True)

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
            'upvote': False,
            'bookmark': False
        }

        if self.context['request'] and self.context['request'].user:
            current_user = self.context['request'].user

            if obj.user.id == current_user.id:
                meta['user'] = True
            if Upvote.objects.filter(Q(post_id=obj.id) & Q(user_id=current_user.id)).exists():
                meta['upvote'] = True
            if Bookmark.objects.filter(Q(post_id=obj.id) & Q(user_id=current_user.id)).exists():
                meta['bookmark'] = True

        return meta

    def get_related(self, obj):
        related_posts = Post.objects \
                            .filter(Q(tags__in=obj.tags.all()) & ~Q(slug=obj.slug)) \
                            .distinct() \
                            .order_by('-upvote_count')[:7]
        serializer = PostAllSerializer(related_posts, many=True, context=self.context)
        return serializer.data

    def validate(self, attrs):
        for tag in attrs['tags']:
            if not tag['name']:
                raise serializers.ValidationError('Invalid values for field interest')
        return attrs

    def create(self, validated_data):
        if self.context['request'] and self.context['request'].user:
            current_user = self.context['request'].user

            title = validated_data['title']
            subtitle = validated_data['subtitle']
            content = validated_data['content']
            tags = validated_data['tags']
            published = validated_data['published']
            cover_image = validated_data['cover_image']

            # unsplash = requests.get('https://api.unsplash.com/?client_id=mdgXUj6qE4VlEuU-OREGkIsCql8NH2PdkR4EFLC1evQ')
            # if unsplash.status_code == 200:
            #     pass

            post = Post(
                title=title,
                subtitle=subtitle,
                content=content,
                published=published,
                user=current_user,
                cover_image=cover_image
            )
            post.save()

            for tag in tags:
                tag = Tag.objects.get(name=tag['name'])
                post.tags.add(tag.id)

            return post

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.subtitle = validated_data.get('subtitle', instance.title)
        instance.cover_image = validated_data.get('cover_image', instance.cover_image)
        instance.published = validated_data.get('published')
        instance.content = validated_data.get('content')

        new_tags = validated_data.get('tags', instance.tags)
        instance.tags.clear()
        if new_tags:
            for tag in new_tags:
                tag = Tag.objects.get(name=tag['name'])
                instance.tags.add(tag.id)
        instance.save()
        return instance

# class PostCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         read_only_fields = ()
