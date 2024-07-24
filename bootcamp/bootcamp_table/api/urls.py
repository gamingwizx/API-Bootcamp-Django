from django.urls import reverse, include, path
from bootcamp_table.api import views
from rest_framework.routers import DefaultRouter
app_name = "bootcamp_app"
# router.register(r'/list', views.BootcampVS, basename="bootcamp")
urlpatterns = [
    path('list/<int:pk>/', views.DestroyUpdateBootcampAV.as_view(), name="bootcamp"),
    path("list/", views.ListBootcampAV.as_view(), name="list_bootcamp"),
    path("create/", views.CreateBootcampAV.as_view(), name="create_bootcamp"),
    path("list/get/<int:pk>/", views.GetBootcampAV.as_view(), name="get_bootcamp"),
    path("<int:pk>/reviews/list/", views.ListReviewAV.as_view(), name="list_bootcamp_reviews"),
    path('<int:pk>/review', views.DestroyUpdateReviewAV.as_view(), name="bootcamp_review"),
    path("<int:pk>/reviews/create/", views.CreateReviewAV.as_view(), name="create_review"),
]
