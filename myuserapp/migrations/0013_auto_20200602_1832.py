# Generated by Django 2.2.2 on 2020-06-02 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myuserapp', '0012_banners_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='business_type',
            field=models.TextField(max_length=5000),
        ),
    ]
