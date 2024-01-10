# Generated by Django 4.2.6 on 2024-01-09 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='NivelDeMaestria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ResultadoDeAprendizaje',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Universidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('did', models.CharField(blank=True, max_length=255, null=True)),
                ('logo', models.ImageField(upload_to='logos_universidades/')),
            ],
        ),
        migrations.CreateModel(
            name='UnidadOrganizativa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('did', models.CharField(blank=True, max_length=255, null=True)),
                ('universidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='certificados.universidad')),
            ],
        ),
        migrations.CreateModel(
            name='OfertaAcademica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('periodo', models.CharField(max_length=255)),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='certificados.curso')),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='certificados.instructor')),
            ],
        ),
        migrations.CreateModel(
            name='Microcredencial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_emision', models.DateField()),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='certificados.estudiante')),
                ('oferta_academica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='certificados.ofertaacademica')),
                ('universidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='certificados.universidad')),
            ],
        ),
        migrations.AddField(
            model_name='curso',
            name='nivel_maestria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='certificados.niveldemaestria'),
        ),
        migrations.AddField(
            model_name='curso',
            name='resultado_aprendizaje',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='certificados.resultadodeaprendizaje'),
        ),
        migrations.AddField(
            model_name='curso',
            name='unidad_organizativa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='certificados.unidadorganizativa'),
        ),
    ]
