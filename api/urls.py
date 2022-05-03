from django.urls import path
from api.views.post import (PostAllView,
                            PostView,
                            PostCreateView,
                            PostManagementView,
                            PostByUserAllView,
                            PostByFollowingUser,
                            PostTrending)
from api.views.comment import CommentAllView, CreateCommentView, DeleteCommentView
from api.views.upvote import UpvoteHandlerView
from api.views.bookmark import BookmarkHandlerView, UserBookmarksListView
from api.views.follower import FollowerHandlerView
from api.views.tag import TagAllView

urlpatterns = [
    path('posts/', PostAllView.as_view(), name='all_posts_view'),
    path('posts/<slug:slug>/', PostView.as_view(), name='post_view'),
    path('post/<slug:slug>/', PostManagementView.as_view({'put': 'update', 'delete': 'destroy'}), name='post_management_view'),
    path('post/', PostCreateView.as_view(), name='post_create_view'),
    path('post_by_user/', PostByUserAllView.as_view(), name='user_draft_posts'),
    path('post_by_following_user/', PostByFollowingUser.as_view(), name='following_posts'),
    path('post_trending/', PostTrending.as_view(), name='trending_posts'),

    path('upvote/<slug:slug>/', UpvoteHandlerView.as_view(), name='upvote_handler_view'),
    path('follower/<slug:slug>/', FollowerHandlerView.as_view(), name='follower_handler_view'),
    path('tags/', TagAllView.as_view(), name='all_tag_view'),

    path('bookmark/<slug:slug>/', BookmarkHandlerView.as_view(), name='bookmark_handler_view'),
    path('bookmarks/', UserBookmarksListView.as_view(), name='bookmark_list_view'),

    path('comments/<slug:slug>/', CommentAllView.as_view(), name='all_comments_view'),
    path('comment/delete/<int:id>/', DeleteCommentView.as_view(), name='comment_delete_view'),
    path('comment/<slug:slug>/', CreateCommentView.as_view(), name='comment_create_view'),
]
