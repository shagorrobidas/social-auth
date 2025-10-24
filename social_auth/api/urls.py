from django.urls import path
from social_auth.api.views.google_auth import GoogleLoginView
from social_auth.api.views.apple_auth import AppleLoginView

urlpatterns = [
    path('auth/social/google/', GoogleLoginView.as_view(), name='google_login'),
    path('auth/social/apple/', AppleLoginView.as_view(), name='apple_login'),
]
