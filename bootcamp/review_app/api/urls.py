from rest_framework import urls
from review_app.api import views
urlpatterns = (
    urls.path('list/<int:pk>/', views.DestroyUpdateReviewAV.as_view(), name="Review"),
    urls.path("list/", views.ListReviewAV.as_view(), name="list_Review"),
    urls.path("create/", views.CreateReviewAV.as_view(), name="create_Review"),
    urls.path("list/get/<int:pk>/", views.GetReviewAV.as_view(), name="get_Review"),
)