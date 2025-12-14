from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, UserProfile

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя')
    email = forms.EmailField(label='Email', required=True)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)
    first_name = forms.CharField(label='Имя', max_length=30, required=True)
    last_name = forms.CharField(label='Фамилия', max_length=30, required=False)
    date_of_birth = forms.DateField(
        label='Дата рождения',
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}))
    height = forms.IntegerField(
        label='Рост (см)',
        required=True,
        min_value=50,
        max_value=250,
        widget=forms.NumberInput(attrs={'placeholder': 'Введите рост в сантиметрах'}))
    gender = forms.ChoiceField(
        label='Пол',
        choices=[('M', 'Мужской'), ('F', 'Женский')],
        required=True)

    error_messages = {
        'password_mismatch': 'Пароли не совпадают.',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2',
                  'first_name', 'last_name', 'date_of_birth',
                  'height', 'gender')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        # Убираем фамилию из регистрации, оставляем только имя
        if commit:
            user.save()
            profile = UserProfile.objects.create(
                user=user,
                date_of_birth=self.cleaned_data['date_of_birth'],
                height=self.cleaned_data['height'],
                gender=self.cleaned_data['gender']
            )
        return user