# Generated by Django 5.0.3 on 2024-03-30 03:50

import django.db.models.deletion
from django.db import migrations, models


def create_roles(apps, schema_editor):
    Roles = apps.get_model('Account', 'role')
    datos = [
        {'role': 'ADMIN'},
        {'role': 'SUPERVISOR'},
        {'role': 'SISTEMAS'},
        {'role': 'SIN-ASIGNAR'},
    ]
    for dato in datos:
        Roles.objects.create(**dato)

class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="role",
            fields=[
                ("idrole", models.AutoField(primary_key=True, serialize=False)),
                ("role", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Account",
            fields=[
                ("idcuenta", models.AutoField(primary_key=True, serialize=False)),
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("cedula", models.CharField(max_length=10, unique=True)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("password", models.CharField(max_length=50)),
                ("last_login", models.DateTimeField(auto_now=True)),
                (
                    "role",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="Account.role"
                    ),
                ),
            ],
        ), migrations.RunPython(create_roles)
    ]
