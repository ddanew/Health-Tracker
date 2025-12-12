from django.core.management import execute_from_command_line
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_tracker.settings')
django.setup()

from users.models import CustomUser

def delete_user_by_email():
    email = "ddanew@yandex.ru"
    
    try:
        user = CustomUser.objects.get(email=email)
        username = user.username
        user.delete()
        print(f"Пользователь {username} с email {email} успешно удален!")
    except CustomUser.DoesNotExist:
        print(f"Пользователь с email {email} не найден!")
        
if __name__ == '__main__':
    delete_user_by_email()