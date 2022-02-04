from django.db import models
from user.models import User
from ckeditor.fields import RichTextField
from django_editorjs_fields import EditorJsJSONField
from .utils import EDITORJS_PLUGINS
# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    subtitle = models.CharField(max_length=150, null=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    cover_image = models.URLField(null=True, blank=True)
    # content = RichTextField()
    upvote_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    read_time = models.PositiveIntegerField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    content = EditorJsJSONField(
        plugins=EDITORJS_PLUGINS,
        tools={
            'Gist': {'class': 'Gist'},
            'Image': {'config': {'endpoint': {'byFile': '/editorjs/image_upload/'}}}
        }
    )

    def __str__(self):
        return f'{self.id} - {self.title}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = RichTextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     unique_together = (('post', 'user'), )


class Upvote(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('post', 'user'), )

    def __str__(self):
        return f'{self.user.name} - {self.post.title}'


class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')

    class Meta:
        unique_together = (('user', 'follower'), )

    def __str__(self):
        return f'{self.user.name} - {self.follower.name}'


class Bookmark(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('post', 'user'), )

    def __str__(self):
        return f'{self.user.name} - {self.post.title}'

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=50)
#     email = models.EmailField(unique=True)
#     posts_count = models.PositiveIntegerField(default=0)
#     followers_count = models.PositiveIntegerField(default=0)
#     following_count = models.PositiveIntegerField(default=0)
#     background_image = models.ImageField(upload_to='', null=True, blank=True)
#     profile_image = models.ImageField(upload_to='', null=True, blank=True)
#     description = models.TextField(max_length=1000)
#     github_link = models.URLField(null=True)
#     linked_link = models.URLField(null=True)
#     twitter_link = models.URLField(null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return f'{self.email} - {self.name}'
#
#
# class Post(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=100, unique=True)
#     slug = models.SlugField(max_length=100, unique=True)
#     cover_image = models.ImageField(upload_to='', null=True, blank=True)
#     content = models.TextField()
#     upvote_count = models.PositiveIntegerField(default=0)
#     comment_count = models.PositiveIntegerField(default=0)
#     read_time = models.PositiveIntegerField()
#     tags = models.ManyToManyField(Tag)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return f'{self.id} - {self.title}'
#
#
# class Comment(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     description = models.TextField(max_length=1000)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         unique_together = (('post', 'user'), )