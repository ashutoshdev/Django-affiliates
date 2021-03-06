# Generated by Django 2.2.2 on 2020-06-20 17:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myuserapp', '0022_generateform_isdeleted'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenerateButton',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website', models.TextField(default='', verbose_name='website')),
                ('name', models.TextField(default='', verbose_name='name')),
                ('title', models.TextField(default='', verbose_name='title')),
                ('category', models.TextField(default='', verbose_name='category')),
                ('locations', models.TextField(default='', verbose_name='locations')),
                ('width', models.TextField(default='', verbose_name='width')),
                ('height', models.TextField(default='', verbose_name='height')),
                ('border', models.TextField(default='', verbose_name='border')),
                ('title_background', models.TextField(default='', verbose_name='title_background')),
                ('title_text_color', models.TextField(default='', verbose_name='title_text_color')),
                ('css', models.TextField(default='', verbose_name='script')),
                ('isDeleted', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='GenerateButton_created_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='GenerateButton_updated_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
