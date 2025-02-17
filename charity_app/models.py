from django.db import models
from django.apps import apps
from django.contrib import auth
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.core.exceptions import PermissionDenied


class UserManager(UserManager):
    use_in_migrations = True #co to

    def _create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name) #a to wgl potrzebne?
        email = GlobalUserModel.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        # user.password = make_password(password) tutaj też
        user.save(using=self.db)
        return user

    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, first_name, last_name, password, **extra_fields)

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, first_name, last_name, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

INSTITUTION_CHOICES = (
    (0, "fundacja"),
    (1, "organizacja pozarządowa"),
    (2, "zbiórka lokalna")
)

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Institution(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    type = models.IntegerField(choices=INSTITUTION_CHOICES, default=0)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    pick_up_date = models.DateTimeField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)

    def __str__(self):
        return f'Who: {self.user} - Bags: {self.quantity} - For: {self.institution.name} - When: {self.pick_up_date} - {self.pick_up_time}'
