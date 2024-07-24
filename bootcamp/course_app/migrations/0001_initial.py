# Generated by Django 5.1b1 on 2024-07-23 09:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bootcamp_table', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('description', models.CharField(max_length=255)),
                ('weeks', models.CharField(max_length=255)),
                ('tuition', models.FloatField()),
                ('minimumSkill', models.CharField(max_length=255)),
                ('scholarhipsAvailable', models.BooleanField(default=False)),
                ('bootcamp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bootcamp_course', to='bootcamp_table.bootcamp')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]