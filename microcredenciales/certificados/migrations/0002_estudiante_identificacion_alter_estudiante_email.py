# Generated by Django 4.2.6 on 2024-01-09 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificados', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='estudiante',
            name='identificacion',
            field=models.CharField(default=1, max_length=255, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]