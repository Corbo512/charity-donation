from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView

class HomeView(TemplateView):
    template_name = 'index.html'

class UserRegisterView(TemplateView):
    template_name = 'register.html'

class UserLoginView(TemplateView):
    template_name = 'login.html'

class DonationFormView(TemplateView):
    template_name = 'form.html'
