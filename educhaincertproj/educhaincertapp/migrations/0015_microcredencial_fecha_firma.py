# Generated by Django 4.2.6 on 2024-01-10 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('educhaincertapp', '0014_rename_inscripcion_microcredencial_participacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='microcredencial',
            name='fecha_firma',
            field=models.DateField(blank=True, null=True),
        ),
    ]
