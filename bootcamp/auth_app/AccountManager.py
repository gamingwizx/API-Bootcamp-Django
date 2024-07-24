# from django.contrib.auth.models import (AbstractUser, BaseUserManager)
# from django.db import models

# class AccountManager(BaseUserManager):
#     def create_user(self, email, password, **extra_fields):
#         if not email:
#             raise ValueError('Email must be provided.')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
    
# class CustomUser(AbstractUser):
#     email = models.EmailField(verbose_name="email", max_length=60, unique=True)
#     username = models.CharField(max_length=30, unique=True)
#     date_joined = models.DateTimeField(auto_now=True)
#     role = models.CharField(max_length=20)
#     is_superuser = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)


#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['username', 'email', 'role']

#     def __str__(self):
#         return self.username
    
#     def has_perm(self, perm, obj=None):
#         return self.is_admin
    
#     def has_module_perms(self, app_label):
#         return True