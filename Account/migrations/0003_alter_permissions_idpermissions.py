# Generated by Django 5.0.3 on 2024-04-17 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "Account",
            "0002_remove_permissions_operation_permissions_can_modify_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="permissions",
            name="idPermissions",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
