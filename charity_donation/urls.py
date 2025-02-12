"""
URL configuration for charity_donation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from charity_app.views import (HomeView, UserLoginView, UserRegisterView, AddDonationView, DonationConfirmationView,)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('rejestracja/', UserRegisterView.as_view(), name='register'),
    path('przekaz-dary/', AddDonationView.as_view(), name='add-donation'),
    path('potwierdzenie-darowizny/', DonationConfirmationView.as_view(), name='donation-confirmation'),
    path('wyloguj/', LogoutView.as_view(), name='logout'),
]
