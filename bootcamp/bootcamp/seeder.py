from django_seed import Seed
from auth_app.models import User
from bootcamp_table.models import Bootcamp
from review_app.models import Review
from course_app.models import Course

seeder = Seed.Seeder()

seeder.add_entity(User, 10)
seeder.add_entity(Bootcamp, 10)
seeder.add_entity(Course, 10)
seeder.add_entity(Review, 10)