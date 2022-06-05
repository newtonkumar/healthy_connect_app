# Generated by Django 3.2.8 on 2022-06-05 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DietaryPreferences',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preference', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'dietary_preferences',
            },
        ),
        migrations.CreateModel(
            name='GoalSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'goal_setting',
            },
        ),
        migrations.CreateModel(
            name='Hobbies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hobby', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'hobbies',
            },
        ),
        migrations.CreateModel(
            name='WorkoutPreferences',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preference', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'workout_preferences',
            },
        ),
    ]