from django.urls import path, include, re_path
from auth_app.api import views
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token 
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView) 
from django.conf.urls.i18n import i18n_patterns

router = routers.SimpleRouter()

router.register(r'admin', views.AdminOperationUserView)

urlpatterns = [
    path(r'/test-security', views.test_security),
    path("/", include((router.urls))),    
    path('/register', views.UserRegistration.as_view(), name="register"),
    path('/register-jwt', views.UserRegistrationJWT.as_view(), name="register"),
    path('/login', obtain_auth_token, name="login"),
    path('/logout', views.LogoutAPIView.as_view(), name="logout"),
    path("/user-list", views.UserList.as_view(), name="user-list"),
    path("/create-role", views.CreateRole.as_view(), name="create-role"),
    path("/token", views.UserLogin.as_view(), name="token_obtain_pair"),
    path("/token-refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("/get-current-user", views.getCurrentUsersView.as_view(), name="get-current-user"),
    path("/request-reset-password", views.RequestResetPasswordView.as_view(), name="request-reset-password"),
    path("/reset-password/<str:token>", views.ResetPasswordView.as_view(), name="reset-password"),
    path("/update-user-info", views.UpdateUserInfoView.as_view(), name="update-user-info"),
]
