from django.db import models
from users.models import CustomUser
from datetime import date

class WeightEntry(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='weight_entries')
    weight = models.FloatField(null=True, blank=True)  # Вес в килограммах
    date = models.DateField(default=date.today, editable=True)
    systolic_pressure = models.IntegerField(null=True, blank=True)  # Систолическое давление
    diastolic_pressure = models.IntegerField(null=True, blank=True)  # Диастолическое давление
    pulse = models.IntegerField(null=True, blank=True)  # Пульс

    def __str__(self):
        weight_str = f"{self.weight} kg" if self.weight else "без веса"
        return f"{self.user.username} - {weight_str} ({self.date})"

    def calculate_bmi(self):
        if self.weight and hasattr(self.user, 'profile') and self.user.profile.height:
            height_m = self.user.profile.height / 100  # Переводим рост в метры
            return round(self.weight / (height_m ** 2), 1)
        return None
