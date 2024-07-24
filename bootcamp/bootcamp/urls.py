
from rest_framework import routers 
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from auth_app.api import views

router = routers.SimpleRouter()

router.register(r'admin', views.AdminOperationUserView)

urlpatterns = [
    path('admins/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/auth', include("auth_app.api.urls"),),
    path("api/v1/bootcamps/", include("bootcamp_table.api.urls")),
    path("api/v1/courses/", include("course_app.api.urls")),
    path("api/v1/reviews/", include("review_app.api.urls")),
    path(r"", views.homepage),
    path("admin", include(router.urls))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
