# Generated by Django 2.2.4 on 2020-04-15 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('1', 'fruits'), ('2', 'vegetables')], max_length=1)),
                ('name', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('description', models.TextField()),
                ('image_url_1', models.CharField(max_length=2083)),
                ('image_url_2', models.CharField(max_length=2083)),
                ('image_url_3', models.CharField(max_length=2083)),
                ('quantity_left', models.IntegerField()),
                ('return_days', models.IntegerField()),
            ],
        ),
    ]
