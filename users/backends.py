from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Ищем пользователя по username или email
            user = UserModel.objects.get(
                Q(username__iexact=username) |
                Q(email__iexact=username)
            )
        except UserModel.DoesNotExist:
            return None
        except UserModel.MultipleObjectsReturned:
            # Если найдено несколько пользователей, возвращаем первого
            user = UserModel.objects.filter(
                Q(username__iexact=username) |
                Q(email__iexact=username)
            ).first()

        # Проверяем пароль и возможность аутентификации
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
