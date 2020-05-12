# Generated by Django 2.2.4 on 2020-05-11 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0040_profile_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='status',
            field=models.CharField(blank=True, choices=[('none', 'none'), ('ordered', 'ordered'), ('shipped', 'shipped'), ('delivered', 'delivered'), ('returned', 'returned')], default='none', max_length=10, null=True),
        ),
    ]
