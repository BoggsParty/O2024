from django.urls import path, include
from django.contrib.auth import views as auth_views
from magic_link import urls as magic_link_urls
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('settings/',views.settings, name='settings'),
    path('settings/success/',views.settings_success, name='settings_success'),
    path('email-settings/', views.email_settings, name='email_settings'),
    path('register/', views.register, name='register'),
    path('register/account-found/', views.existing_account, name='existing_account'),
    path('two-accounts/', views.two_accounts, name='two_accounts'),
    path('logout/', views.logout, name='logout'),
    path('about/', views.about, name='about'),
    path('sports/all/', views.sports_menu, name='sports_menu'),
    path('magic_link/', include(magic_link_urls)),
    path('login-link/', views.request_link, name='request_link'),
    path('3480980284/daily_email/', views.email, name='email'),
    #path('test/', views.test, name='test'),
]