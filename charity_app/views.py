# from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import Donation, Institution


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['total_donations'] = Donation.objects.all().count()
        context['total_institutions'] = Institution.objects.all().count()
        return context

class UserRegisterView(TemplateView):
    template_name = 'register.html'

class UserLoginView(TemplateView):
    template_name = 'login.html'

class AddDonationView(TemplateView):
    template_name = 'form.html'

class DonationConfirmationView(TemplateView):
    template_name = 'form-confirmation.html'
