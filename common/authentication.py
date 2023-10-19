from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from rest_framework_simplejwt.settings import api_settings
from django.utils.translation import gettext_lazy as _

from invite.models import Employee


class MyJWTAuthentication(JWTAuthentication):
    """丢，鸡儿复杂，还不如自己用PYJWT...算了，权当学习吧..."""

    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken(_("Token contained no recognizable user identification"))

        try:
            user = Employee.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except Employee.DoesNotExist:
            raise AuthenticationFailed(_("User not found"), code="user_not_found")

        return user
