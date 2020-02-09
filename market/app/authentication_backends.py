from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from .models import User


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()

        try:
            user = user_model.objects.get(email=username)
            print(user)
        except user_model.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                print('good')
                return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
