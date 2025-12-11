from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from .models import WeightEntry

class WeightEntryForm(forms.ModelForm):
    class Meta:
        model = WeightEntry
        fields = ['weight', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if not self.instance.pk:
            self.fields['date'].initial = date.today()
    
    def clean_date(self):
        date_value = self.cleaned_data['date']
        if date_value > date.today():
            raise ValidationError('Дата не может быть в будущем.')
        return date_value
    
    def clean(self):
        cleaned_data = super().clean()
        date_value = cleaned_data.get('date')
        
        if self.user and date_value:
            if self.instance.pk:
                if self.instance.date != date_value:
                    existing_entry = WeightEntry.objects.filter(
                        user=self.user, date=date_value
                    ).exclude(pk=self.instance.pk).first()
                    if existing_entry:
                        # Вместо ошибки устанавливаем флаг, чтобы обработать в представлении
                        self.existing_entry = existing_entry
            else:
                existing_entry = WeightEntry.objects.filter(
                    user=self.user, date=date_value
                ).first()
                if existing_entry:
                    # Вместо ошибки устанавливаем флаг, чтобы обработать в представлении
                    self.existing_entry = existing_entry
        
        return cleaned_data