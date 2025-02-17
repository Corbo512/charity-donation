from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from django.views.generic.edit import CreateView
from .forms import UserRegisterForm, UserLoginForm, DonationForm
from .models import Donation, Institution, Category


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['donations'] = Donation.objects.all()
        context['institutions'] = Institution.objects.all()
        context['total_donations'] = Donation.objects.count()
        context['total_institutions'] = Institution.objects.count()
        return context

class UserRegisterView(CreateView):
    template_name = 'register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)

class UserLoginView(FormView):
    template_name = 'login.html'
    form_class = UserLoginForm

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('home')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        user = authenticate(
            email=email,
            password=password
        )

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            return redirect('register')

class AddDonationView(LoginRequiredMixin, TemplateView):
    template_name = 'form.html'
    form_class = DonationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.objects.all()
        context['institutions'] = Institution.objects.all()
        context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.user = self.request.user
            donation.save()
            form.save_m2m()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

class DonationConfirmationView(LoginRequiredMixin, TemplateView):
    template_name = 'form-confirmation.html'

class UserLogoutView(LogoutView):
    next_page = 'home'

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'user-profile.html'
