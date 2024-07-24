from django_seeding import seeders
from django_seeding.seeder_registry import SeederRegistry
from auth_app.models import User

@SeedingRegistry.register
class M1Seeder(seeders.JSONFileModelSeeder):
    model = User
    json_file_path = 'auth_app/seeders_data/auth.json'