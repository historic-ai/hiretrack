from django.urls import path
from . import views

urlpatterns = [

    # Auth URLs
    path('auth/register/', views.register),
    path('auth/login/', views.login),
    path('auth/logout/', views.logout),

    # Job Application URLs
    path('applications/', views.get_all_applications),
    path('applications/create/', views.create_application),
    path('applications/<int:pk>/', views.get_single_application),
    path('applications/<int:pk>/update/', views.update_application),
    path('applications/<int:pk>/delete/', views.delete_application),
]