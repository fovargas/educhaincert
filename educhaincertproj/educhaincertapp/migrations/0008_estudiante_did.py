# Generated by Django 4.2.6 on 2024-01-09 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('educhaincertapp', '0007_instructor_did'),
    ]

    operations = [
        migrations.AddField(
            model_name='estudiante',
            name='did',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
