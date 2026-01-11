from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from .models import WeightEntry

class WeightEntryForm(forms.ModelForm):
    class Meta:
        model = WeightEntry
        fields = ['weight', 'date', 'systolic_pressure', 'diastolic_pressure', 'pulse']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['weight'].initial = self.instance.weight
            self.fields['date'].initial = self.instance.date
            self.fields['systolic_pressure'].initial = self.instance.systolic_pressure
            self.fields['diastolic_pressure'].initial = self.instance.diastolic_pressure
            self.fields['pulse'].initial = self.instance.pulse
        elif not self.instance.pk:
            self.fields['date'].initial = date.today()
    
    def clean_date(self):
        date_value = self.cleaned_data['date']
        if date_value > date.today():
            raise ValidationError('Дата не может быть в будущем.')
        return date_value

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight == '' or weight is None:
            return None
        try:
            return float(weight)
        except (ValueError, TypeError):
            raise ValidationError('Введите корректное значение веса.')

    def clean_systolic_pressure(self):
        systolic = self.cleaned_data.get('systolic_pressure')
        if systolic == '' or systolic is None:
            return None
        try:
            return int(systolic)
        except (ValueError, TypeError):
            raise ValidationError('Введите корректное значение систолического давления.')

    def clean_diastolic_pressure(self):
        diastolic = self.cleaned_data.get('diastolic_pressure')
        if diastolic == '' or diastolic is None:
            return None
        try:
            return int(diastolic)
        except (ValueError, TypeError):
            raise ValidationError('Введите корректное значение диастолического давления.')

    def clean_pulse(self):
        pulse = self.cleaned_data.get('pulse')
        if pulse == '' or pulse is None:
            return None
        try:
            return int(pulse)
        except (ValueError, TypeError):
            raise ValidationError('Введите корректное значение пульса.')

    def clean(self):
        cleaned_data = super().clean()
        weight = cleaned_data.get('weight')
        systolic = cleaned_data.get('systolic_pressure')
        diastolic = cleaned_data.get('diastolic_pressure')
        pulse = cleaned_data.get('pulse')

        # Проверяем, что если заполнено одно поле давления, то заполнено и второе
        if (systolic is not None and diastolic is None) or (diastolic is not None and systolic is None):
            raise ValidationError('Необходимо заполнить оба значения артериального давления (систолическое и диастолическое).')

        # Проверяем, что хотя бы одно поле заполнено
        if weight is None and systolic is None and diastolic is None and pulse is None:
            raise ValidationError('Необходимо заполнить хотя бы одно поле: вес, давление или пульс.')

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