# Generated by Django 2.2.2 on 2020-06-03 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myuserapp', '0015_auto_20200603_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generateform',
            name='website',
            field=models.TextField(default='', verbose_name='website'),
        ),
    ]
