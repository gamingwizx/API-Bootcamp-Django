from django.contrib import admin

from bootcamp_table.models import Bootcamp
from bootcamp_table.models import Review
from auth_app.models import (User, Role, UserRolePermissions)
from course_app.models import Course

# Register your models here.
admin.site.register(Bootcamp)
admin.site.register(Review)
admin.site.register(User)
admin.site.register(Role)
admin.site.register(UserRolePermissions)
admin.site.register(Course)