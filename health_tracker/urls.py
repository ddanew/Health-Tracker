from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from tracker import views as tracker_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register_view, name='register'),
    path('login/', user_views.login_view, name='login'),
    path('logout/', user_views.logout_view, name='logout'),
    path('profile/', user_views.profile_view, name='profile'),
    path('profile/edit/', user_views.ProfileUpdateView.as_view(), name='profile-edit'),
    path('weight/add/', tracker_views.add_weight, name='add-weight'),
    path('weight/', tracker_views.WeightListView.as_view(), name='weight-list'),
    path('weight/<int:pk>/edit/', tracker_views.WeightUpdateView.as_view(), name='weight-edit'),
    path('weight/<int:pk>/delete/', tracker_views.WeightDeleteView.as_view(), name='weight-delete'),
    path('statistics/', tracker_views.statistics_view, name='statistics'),
    path('', include('tracker.urls')),
]
