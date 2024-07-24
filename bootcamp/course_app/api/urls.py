from django.urls import path
from course_app.api import views
urlpatterns = [
    path("list/<int:pk>", views.DestroyUpdateCourseVS.as_view(), name="destroy_update_course"),
    path("get/<int:pk>", views.GetCourseVS.as_view(), name="get_course"),
    path("list", views.GetListCourseVS.as_view(), name="list_course"),
    path("create", views.CreateCourseVS.as_view(), name="create_course")
]