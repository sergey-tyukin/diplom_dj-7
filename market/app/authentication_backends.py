from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from .models import User


class EmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        print('auth backend')
        user_model = get_user_model()

        try:
            user = user_model.objects.get(email=username)
        except user_model.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
