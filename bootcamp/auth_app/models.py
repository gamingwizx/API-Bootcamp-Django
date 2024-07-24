from django.db import models
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import Permission
from collections.abc import Iterable
from rest_framework_simplejwt.tokens import RefreshToken


class AccountManager(auth_models.BaseUserManager):
    def create_user(self, email, password, username, role='user') -> "User":
        if not email:
            raise ValueError('Email must be provided.')
        user = self.model(email=self.normalize_email(email))
        user.username = username
        user.role = role
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password, role="admin") -> "User":
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
            is_admin=True,
            is_superuser=True,
        )

        user.save()

        return user

class Role(models.Model):
    name = models.CharField(max_length=25, unique=True)

    class Meta:
        db_table = "auth_role"

class UserRolePermissions(models.Model):
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name="user_role_permission")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="user_role_role")

    class Meta:
        db_table = "auth_user_role_permissions"

class User(auth_models.AbstractUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(auto_now=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="user_role")
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    reset_password_token = models.CharField(max_length=40, default="", null=True)
    reset_password_expiry = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'role']

    class Meta:
        db_table = "auth_user"

    def __str__(self):
        return self.username

    def has_perms(self, perm_list, obj=None):
        """
        Return True if the user has each of the specified permissions. If
        object is passed, check if the user has all required perms for it.
        """
        has_perm_role = []
        has_perm_user = []
        role = Role.objects.get(id=self.role.id)

        for i in range(len(perm_list[1])):
            permission = Permission.objects.get(codename=perm_list[1][i])
            user_role_permissions = UserRolePermissions.objects.filter(permission=permission.id, role=role.id)
            has_perm_role.append(user_role_permissions.exists())
                
        for perm in perm_list[0]:
            has_perm_user.append(self.has_perm(perm, obj))

        if not isinstance(perm_list, Iterable) or isinstance(perm_list, str):
            raise ValueError("perm_list must be an iterable of permissions.")
        
        return all(has_perm_role) or all(has_perm_user)
    
    def has_module_perms(self, app_label):
        return True
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }
# class Permission(models.Model):
#     name = models.CharField(max_length=100)
#     method = models.CharField(max_length=20)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="permissions_users")

#     class Meta:
#         db_table = "auth_permission"