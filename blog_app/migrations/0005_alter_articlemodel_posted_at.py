# Generated by Django 4.0.3 on 2022-04-17 00:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0004_alter_articlemodel_posted_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlemodel',
            name='posted_at',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
