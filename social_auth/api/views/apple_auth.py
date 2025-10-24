import requests
import jwt
import json
import time
from django.conf import settings
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from social_auth.models import User, SocialAccount
from social_auth.api.serializer.serializers import UserProfileSerializer


class AppleLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            id_token = request.data.get("id_token")
            if not id_token:
                return Response({"error": "id_token is required"}, status=400)

            apple_user_info = self.verify_apple_token(id_token)
            if not apple_user_info:
                return Response({"error": "Invalid Apple ID token"}, status=400)

            email = apple_user_info.get("email")
            sub = apple_user_info.get("sub")
            name = request.data.get("name", "")

            if not email:
                return Response({"error": "Email not provided by Apple"}, status=400)

            user, created = self.get_or_create_user(email, name, sub, apple_user_info)

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
                "user": UserProfileSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "created": created,
                "message": "Apple login successful"
            }, status=200)

        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({"error": str(e)}, status=400)

    # ---------------------------- Helpers ---------------------------- #

    def get_or_create_user(self, email, name, sub, apple_user_info):
        created = False
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            base_username = email.split("@")[0]
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
            provider="apple",
            defaults={"uid": sub, "extra_data": apple_user_info}
        )
        if not social_created:
            social.uid = sub
            social.extra_data = apple_user_info
            social.save()

        return user, created

    def verify_apple_token(self, id_token):
        """Decode Apple identity token"""
        try:
            apple_keys = requests.get("https://appleid.apple.com/auth/keys", timeout=10).json()
            header = jwt.get_unverified_header(id_token)
            key = next((k for k in apple_keys["keys"] if k["kid"] == header["kid"]), None)
            if not key:
                return None

            # Directly decode using the public key
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))
            decoded = jwt.decode(
                id_token,
                key=public_key,
                audience=settings.APPLE_CLIENT_ID,
                algorithms=["RS256"],
            )

            if decoded.get("exp") < time.time():
                return None

            return decoded
        except Exception as e:
            print(f"Apple token verification failed: {e}")
            return None
