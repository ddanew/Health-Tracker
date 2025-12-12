from django.core.management import execute_from_command_line
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_tracker.settings')
django.setup()

from users.models import CustomUser

def create_super_user():
    username = "DDA"
    email = "ddanew@yandex.ru"
    password = "DLSNdlsn0603!!!"
    
    # Проверяем, существует ли уже пользователь с таким именем
    if CustomUser.objects.filter(username=username).exists():
        print(f"Пользователь с именем {username} уже существует!")
        return
    
    # Создаем суперпользователя
    user = CustomUser.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    
    print(f"Суперпользователь {username} успешно создан!")

if __name__ == '__main__':
    create_super_user()