from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from .models import UserProfile

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            next_url = request.GET.get('next', 'profile')
            return redirect(next_url)
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    error_message = None
    if request.method == 'POST':
        username_or_email = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        # Используем кастомный бэкенд для аутентификации по email или username
        user = authenticate(request, username=username_or_email, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'profile')
            return redirect(next_url)
        else:
            error_message = "Неверное имя пользователя или пароль"
    return render(request, 'users/login.html', {'error_message': error_message})

@login_required
def profile_view(request):
    return render(request, 'users/profile.html')

@login_required
def logout_view(request):
    logout(request)
    # Используем LOGOUT_REDIRECT_URL из настроек
    from django.conf import settings
    redirect_url = getattr(settings, 'LOGOUT_REDIRECT_URL', 'home')
    return redirect(redirect_url)

class ProfileUpdateView(UpdateView):
    model = UserProfile
    fields = ['date_of_birth', 'height', 'gender']
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        # Создаем профиль, если его нет
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

    def post(self, request, *args, **kwargs):
        # Обработка изменения имени пользователя
        first_name = request.POST.get('first_name', '')
        if first_name:
            request.user.first_name = first_name
            request.user.save()
        
        # Вызов родительского метода для обработки остальных полей
        return super().post(request, *args, **kwargs)

@login_required
def update_user_info(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        request.user.first_name = first_name
        request.user.save()
        return redirect('profile')
    return redirect('profile')