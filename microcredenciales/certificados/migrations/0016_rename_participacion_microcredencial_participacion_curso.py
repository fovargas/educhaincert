# Generated by Django 4.2.6 on 2024-01-11 02:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('certificados', '0015_microcredencial_fecha_firma'),
    ]

    operations = [
        migrations.RenameField(
            model_name='microcredencial',
            old_name='participacion',
            new_name='participacion_curso',
        ),
    ]
