# Generated by Django 2.2.4 on 2020-04-29 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_auto_20200429_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birth_date',
            field=models.DateField(default=0),
        ),
    ]
