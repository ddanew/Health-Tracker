from django.db import models
from users.models import CustomUser
from datetime import date

class WeightEntry(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='weight_entries')
    weight = models.FloatField()  # Вес в килограммах
    date = models.DateField(default=date.today, editable=True)

    def __str__(self):
        return f"{self.user.username} - {self.weight} kg ({self.date})"

    def calculate_bmi(self):
        if hasattr(self.user, 'profile') and self.user.profile.height:
            height_m = self.user.profile.height / 100  # Переводим рост в метры
            return round(self.weight / (height_m ** 2), 1)
        return None
