# Generated by Django 4.2.6 on 2024-01-10 22:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('educhaincertapp', '0013_remove_microcredencial_estudiante_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='microcredencial',
            old_name='inscripcion',
            new_name='participacion',
        ),
    ]
