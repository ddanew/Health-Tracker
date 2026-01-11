from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('weight/', views.WeightListView.as_view(), name='weight-list'),
    path('weight/add/', views.add_weight, name='add-weight'),
    path('weight/<int:pk>/edit/', views.WeightUpdateView.as_view(), name='weight-edit'),
    path('weight/<int:pk>/delete/', views.WeightDeleteView.as_view(), name='weight-delete'),
]