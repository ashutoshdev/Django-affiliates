# Generated by Django 2.2.2 on 2020-05-30 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myuserapp', '0002_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.TextField(blank=True),
        ),
    ]
