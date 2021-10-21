# Generated by Django 2.2.2 on 2020-06-08 18:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myuserapp', '0018_leadcommission'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenerateFormOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.TextField(blank=True, default='0', null=True, verbose_name='source')),
                ('orderid', models.TextField(blank=True, default='0', null=True, verbose_name='orderid')),
                ('total_amount', models.TextField(blank=True, default='0', null=True, verbose_name='total_amount')),
                ('email', models.TextField(blank=True, default='0', null=True, verbose_name='email')),
                ('phone', models.TextField(blank=True, default='0', null=True, verbose_name='phone')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('aff_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='GenerateFormOrder_created_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='GenerateFormOrder_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
