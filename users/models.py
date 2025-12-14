from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)  # Оставляем только имя
    last_name = models.CharField(max_length=30, blank=True)   # Убираем фамилию из обязательных полей
    
    def __str__(self):
        return self.username

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)  # Рост в сантиметрах
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"