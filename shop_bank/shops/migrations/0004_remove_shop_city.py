# Generated by Django 4.2.7 on 2023-11-15 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0003_rename_city_name_city_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='city',
        ),
    ]