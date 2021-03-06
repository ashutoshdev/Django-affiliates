# Generated by Django 2.2.2 on 2020-06-08 17:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myuserapp', '0017_leaddetail_referred'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeadCommission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent_lead_rate', models.TextField(default='0', verbose_name='parent_lead_rate')),
                ('child_lead_rate', models.TextField(default='0', verbose_name='child_lead_rate')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='LeadCommission_created_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='LeadCommission_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
