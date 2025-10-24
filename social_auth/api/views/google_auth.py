import requests
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from social_auth.models import User, SocialAccount
from social_auth.api.serializer.serializers import UserProfileSerializer


class GoogleLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            access_token = request.data.get('access_token')
            if not access_token:
                return Response({'error': 'Access token is required'}, status=400)

            google_user_info = self.get_google_user_info(access_token)
            if not google_user_info:
                return Response({'error': 'Invalid or expired Google token'}, status=400)

            email = google_user_info.get('email')
            google_id = google_user_info.get('id')
            name = google_user_info.get('name', '')

            if not email:
                return Response({'error': 'Email not provided by Google'}, status=400)

            user, created = self.get_or_create_user(email, name, google_id, google_user_info)

            # Invalidate old refresh
            if user.current_refresh_token:
                try:
                    old_refresh = RefreshToken(user.current_refresh_token)
                    old_refresh.blacklist()
                    user.force_logout_required = True
                    user.save()
                except Exception:
                    pass

            refresh = RefreshToken.for_user(user)
            user.current_refresh_token = str(refresh)
            user.save()

            return Response({
                'user': UserProfileSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'created': created,
                'message': 'Google login successful'
            }, status=200)

        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=400)

    def get_google_user_info(self, access_token):
        try:
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(
                'https://www.googleapis.com/oauth2/v2/userinfo',
                headers=headers, timeout=10
            )
            if response.status_code != 200:
                return None
            data = response.json()
            if not data.get('email'):
                return None
            return data
        except Exception:
            return None

    def get_or_create_user(self, email, name, google_id, google_user_info):
        created = False
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            base_username = email.split('@')[0]
            username = base_username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

            user = User.objects.create_user(
                username=username, email=email, name=name, is_active=True
            )
            created = True

        social, social_created = SocialAccount.objects.get_or_create(
            user=user,
            provider='google',
            defaults={'uid': google_id, 'extra_data': google_user_info}
        )
        if not social_created:
            social.uid = google_id
            social.extra_data = google_user_info
            social.save()
        return user, created
