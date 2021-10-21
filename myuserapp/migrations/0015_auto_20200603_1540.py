# Generated by Django 2.2.2 on 2020-06-03 10:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myuserapp', '0014_auto_20200602_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaddetail',
            name='position',
            field=models.TextField(blank=True, choices=[('top', 'top'), ('side', 'side'), ('middle', 'middle'), ('bottom', 'bottom')], default='', null=True, verbose_name='banner_position'),
        ),
        migrations.CreateModel(
            name='GenerateForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='', verbose_name='name')),
                ('title', models.TextField(default='', verbose_name='title')),
                ('category', models.TextField(default='', verbose_name='category')),
                ('width', models.TextField(default='', verbose_name='width')),
                ('height', models.TextField(default='', verbose_name='height')),
                ('border', models.TextField(default='', verbose_name='border')),
                ('title_background', models.TextField(default='', verbose_name='title_background')),
                ('title_text_color', models.TextField(default='', verbose_name='title_text_color')),
                ('thank_you_url', models.TextField(default='', verbose_name='thank_you_url')),
                ('body_text_background', models.TextField(default='', verbose_name='body_text_background')),
                ('body_text_color', models.TextField(default='', verbose_name='body_text_color')),
                ('script', models.TextField(default='', verbose_name='script')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='GenerateForm_created_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='GenerateForm_updated_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('website', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myuserapp.Websites')),
            ],
        ),
    ]
