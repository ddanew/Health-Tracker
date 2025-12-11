import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_tracker.settings')
django.setup()

from django.contrib.auth.models import User

# Поиск суперпользователя
def find_super_user():
    superusers = User.objects.filter(is_superuser=True)
    if superusers.exists():
        for user in superusers:
            print(f'Имя суперпользователя: {user.username}')
            print(f'ID: {user.id}')
            print(f'Email: {user.email}')
            print(f'Дата создания: {user.date_joined}')
    else:
        print('Суперпользователь не найден')

if __name__ == '__main__':
    find_super_user()