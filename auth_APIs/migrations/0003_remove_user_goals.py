# Generated by Django 3.2.8 on 2022-06-05 08:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_APIs', '0002_auto_20220605_1346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='goals',
        ),
    ]