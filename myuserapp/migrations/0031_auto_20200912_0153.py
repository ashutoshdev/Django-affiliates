# Generated by Django 2.2.2 on 2020-09-11 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myuserapp', '0030_generatequeryform_lead_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generatequeryform',
            name='name',
            field=models.TextField(blank=True, default='', null=True, verbose_name='name'),
        ),
    ]