# Generated by Django 4.2.6 on 2024-01-09 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificados', '0006_instructor_identificacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='did',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
