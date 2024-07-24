from rest_framework import permissions
from rest_framework import exceptions
from auth_app.models import UserRolePermissions
from django.contrib.auth.models import Permission 

class CustomPermission(permissions.DjangoObjectPermissions):
    perms_map = {
        'GET': [],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }
    
    perms_map1 = {
        'GET': [],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['add_%(model_name)s'],
        'PUT': ['change_%(model_name)s'],
        'PATCH': ['change_%(model_name)s'],
        'DELETE': ['delete_%(model_name)s'],
    }

    authenticated_users_only = True

    def get_required_permissions(self, method, model_cls):
        """
        Given a model and an HTTP method, return the list of permission
        codes that the user is required to have.
        """
        kwargs = {
            'app_label': model_cls._meta.app_label,
            'model_name': model_cls._meta.model_name
        }

        if method not in self.perms_map:
            raise exceptions.MethodNotAllowed(method)
        return [[perm % kwargs for perm in self.perms_map[method]], [perm % kwargs for perm in self.perms_map1[method]]]
    

    def has_permission(self, request, view):
        if not request.user or (
           not request.user.is_authenticated and self.authenticated_users_only):
            return False

        if getattr(view, '_ignore_model_permissions', False):
            return True
        
        
        
        # element = self.get_required_permissions(request.method, queryset.model)[1] 
        # print(element[0])
        # perms = Permission.objects.get(codename=element[0])
        
        # user_roles = UserRolePermissions.objects.filter(role_id=request.user.role)
        
        queryset = self._queryset(view)
        perms = self.get_required_permissions(request.method, queryset.model)
        return request.user.has_perms(perms)
    
    def has_object_permission(self, request, view, obj):
        if (obj.user.id == request.user.id):
            return True
        return False

class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        
        return True