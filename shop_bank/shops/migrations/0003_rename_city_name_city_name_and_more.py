# Generated by Django 4.2.7 on 2023-11-15 16:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0002_shop_city_alter_shop_street_alter_street_city'),
    ]

    operations = [
        migrations.RenameField(
            model_name='city',
            old_name='city_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='shop',
            old_name='shop_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='street',
            old_name='street_name',
            new_name='name',
        ),
    ]
