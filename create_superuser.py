import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_tracker.settings')
django.setup()

from django.contrib.auth.models import User

# Создание суперпользователя
def create_super_user():
    # Удаляем старого суперпользователя, если существует
    User.objects.filter(is_superuser=True).delete()
    
    # Создаем нового суперпользователя
    user = User.objects.create_user(
        username='DAD',
        password='dlsn0603'
    )
    user.is_superuser = True
    user.is_staff = True
    user.save()
    
    print(f'Суперпользователь {user.username} успешно создан')

if __name__ == '__main__':
    create_super_user()