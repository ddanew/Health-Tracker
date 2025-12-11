from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import WeightEntry
from .forms import WeightEntryForm

def home_view(request):
    """Главная страница, доступная без аутентификации"""
    return render(request, 'tracker/home.html', {'user': request.user})

@login_required
def add_weight(request):
    if request.method == 'POST':
        form = WeightEntryForm(request.POST, user=request.user)
        if form.is_valid():
            # Проверяем, есть ли существующая запись для этой даты
            if hasattr(form, 'existing_entry') and form.existing_entry and 'confirm' not in request.POST:
                # Если запись уже существует и пользователь не подтвердил обновление, показываем страницу подтверждения
                existing_entry = form.existing_entry
                return render(request, 'tracker/weight_confirm_update.html', {
                    'object': existing_entry,
                    'old_weight': existing_entry.weight,
                    'new_weight': form.cleaned_data['weight'],
                    'form': form
                })
            elif hasattr(form, 'existing_entry') and form.existing_entry and 'confirm' in request.POST:
                # Если запись уже существует и пользователь подтвердил обновление
                existing_entry = form.existing_entry
                existing_entry.weight = form.cleaned_data['weight']
                existing_entry.save()
                return redirect('weight-list')
            else:
                # Создаем новую запись
                entry = form.save(commit=False)
                entry.user = request.user
                entry.save()
                return redirect('weight-list')
    else:
        form = WeightEntryForm(user=request.user)
    return render(request, 'tracker/add_weight.html', {'form': form})

class WeightListView(LoginRequiredMixin, ListView):
    model = WeightEntry
    template_name = 'tracker/weight_list.html'
    context_object_name = 'entries'

    def get_queryset(self):
        return WeightEntry.objects.filter(user=self.request.user).order_by('-date')

class WeightUpdateView(LoginRequiredMixin, UpdateView):
    model = WeightEntry
    form_class = WeightEntryForm
    template_name = 'tracker/weight_edit.html'
    success_url = reverse_lazy('weight-list')
    
    def post(self, request, *args, **kwargs):
        if 'confirm' in request.POST:
            return super().post(request, *args, **kwargs)
        else:
            self.object = self.get_object()
            form = self.get_form()
            old_weight = self.object.weight
            new_weight = form.data.get('weight')
            return render(request, 'tracker/weight_confirm_update.html', {
                'object': self.object,
                'old_weight': old_weight,
                'new_weight': new_weight,
                'form': form
            })

class WeightDeleteView(DeleteView):
    model = WeightEntry
    template_name = 'tracker/weight_confirm_delete.html'
    success_url = reverse_lazy('home')

@login_required
def update_or_create_weight(request):
    """
    Представление для обновления существующей записи или создания новой
    """
    if request.method == 'POST':
        form = WeightEntryForm(request.POST, user=request.user)
        if form.is_valid():
            date_value = form.cleaned_data['date']
            
            try:
                entry = WeightEntry.objects.get(user=request.user, date=date_value)
                entry.weight = form.cleaned_data['weight']
                entry.save()
            except WeightEntry.DoesNotExist:
                entry = form.save(commit=False)
                entry.user = request.user
                entry.save()
            
            return redirect('weight-list')
    else:
        form = WeightEntryForm(user=request.user)
    
    return render(request, 'tracker/add_weight.html', {'form': form})

@login_required
def statistics_view(request):
    entries = WeightEntry.objects.filter(user=request.user).order_by('date')
    latest_entry = entries.last()
    latest_bmi = None
    bmi_category = "Недостаточно данных"
    normal_weight_min = None
    normal_weight_max = None

    if latest_entry:
        latest_bmi = latest_entry.calculate_bmi()
        if latest_bmi:
            if latest_bmi < 18.5:
                bmi_category = "Недостаточная масса"
                # Рассчитываем нормальный вес при недостатке массы
                if hasattr(latest_entry.user, 'profile') and latest_entry.user.profile.height:
                    height_m = latest_entry.user.profile.height / 100
                    normal_weight_min = round(18.5 * (height_m ** 2), 1)
                    normal_weight_max = round(24.9 * (height_m ** 2), 1)
            elif 18.5 <= latest_bmi < 25:
                bmi_category = "Норма"
            elif 25 <= latest_bmi < 30:
                bmi_category = "Избыточный вес"
                # Рассчитываем нормальный вес при избыточной массе
                if hasattr(latest_entry.user, 'profile') and latest_entry.user.profile.height:
                    height_m = latest_entry.user.profile.height / 100
                    normal_weight_min = round(18.5 * (height_m ** 2), 1)
                    normal_weight_max = round(24.9 * (height_m ** 2), 1)
            else:
                bmi_category = "Ожирение"
                # Рассчитываем нормальный вес при ожирении
                if hasattr(latest_entry.user, 'profile') and latest_entry.user.profile.height:
                    height_m = latest_entry.user.profile.height / 100
                    normal_weight_min = round(18.5 * (height_m ** 2), 1)
                    normal_weight_max = round(24.9 * (height_m ** 2), 1)

    return render(request, 'tracker/statistics.html', {
        'entries': entries,
        'latest_entry': latest_entry,
        'latest_bmi': latest_bmi,
        'bmi_category': bmi_category,
        'normal_weight_min': normal_weight_min,
        'normal_weight_max': normal_weight_max,
        'weight_data': [entry.weight for entry in entries],
        'dates': [entry.date.isoformat() for entry in entries],
        'bmi_data': [entry.calculate_bmi() or 0 for entry in entries]
    })
