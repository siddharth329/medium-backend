from django.urls import path, include
from .views import UserProfile, CurrentUserProfile, GoogleLoginView
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView, ConfirmEmailView
from dj_rest_auth.views import LoginView, LogoutView


urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('register/', RegisterView.as_view()),
    path('verify-email/', VerifyEmailView.as_view()),
    path('account-confirm-email/', VerifyEmailView.as_view()),
    path('account-confirm-email/<str:key>/', ConfirmEmailView.as_view()),
    path('profile/', CurrentUserProfile.as_view()),
    path('google/login/', GoogleLoginView.as_view()),
    path('<int:pk>/', UserProfile.as_view()),

    path('accounts/', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
]
