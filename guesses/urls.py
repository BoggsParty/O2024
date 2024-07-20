from django.urls import path
from . import views

urlpatterns = [
    path('all/<str:sport>/', views.everyones_guesses, name='everyones_guesses'),
    path('all/', views.all_guesses, name='all_guesses'),
    path('edit/<str:sport>/', views.edit, name='edit'),
    path('edit/all/<str:sport>/', views.quick_guess, name='quick_guess'),
    path('calculate/', views.calculate, name='calculate'),
]