from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('weight/', views.WeightListView.as_view(), name='weight-list'),
]