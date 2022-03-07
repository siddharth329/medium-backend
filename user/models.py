from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.admin import ModelAdmin
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


FULL_USER_PROFILE = [
    'name',
    'email',
    'slug',
    'description',
    'posts_count',
    'followers_count',
    'following_count',
    'background_image',
    'profile_image',
    'github_link',
    'linkedin_link',
    'twitter_link',
    'user_type'
]


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('user_type', 2)

        self.create_user(email=email, name=name, password=password, **other_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE = [
        (0, 'REGULAR_USER'),
        (1, 'ADMIN'),
        (2, 'SUPER_ADMIN')
    ]

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, null=True, blank=True)
    description = models.TextField(max_length=500, blank=True)
    profile_image = models.URLField(null=True, blank=True)
    background_image = models.URLField(null=True, blank=True)

    posts_count = models.PositiveIntegerField(default=0)
    followers_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    github_link = models.URLField(null=True, blank=True)
    linkedin_link = models.URLField(null=True, blank=True)
    twitter_link = models.URLField(null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    user_type = models.IntegerField(default=0, choices=USER_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


class UserAdmin(ModelAdmin):
    search_fields = ('email', 'name')
    list_filter = ('is_active', 'is_staff')
    ordering = ('is_staff', '-created_at')
    list_display = ('email', 'name', 'user_type', 'is_active', 'is_staff')
    fieldsets = (
        ('Required', {'fields': ('email', 'name', 'password')}),
        ('About', {'fields': [
            'slug',
            'description',
            'github_link',
            'linkedin_link',
            'twitter_link',
            'profile_image',
            'background_image',
            'posts_count',
            'followers_count',
            'following_count',
        ]}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'user_permissions', 'groups')}),
        ('App Level Critical', {'fields': ('user_type', 'is_superuser')}),
        ('Metrics', {'fields': ('last_login', 'created_at', 'updated_at')})
    )
    readonly_fields = ('last_login', 'created_at', 'updated_at')

#
#
# class UserManager(models.Manager):
#     use_in_migrations = True
#
#     def get_by_natural_key(self, email):
#         return self.get(**{f'{self.model.USERNAME_FIELD}__iexact': email})
#
#
# class User(AbstractBaseUser):
#     email = models.EmailField(unique=True)
#     date_joined = models.DateTimeField(auto_now_add=True)
#     user_type = models.TextField(default=UserType.REGULAR_USER)
#     problem_permission = models.TextField(default=ProblemPermission.NONE)
#     reset_password_token = models.TextField(null=True)
#     reset_password_token_expire_time = models.DateTimeField(null=True)
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['email']
