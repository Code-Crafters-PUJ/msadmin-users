# Generated by Django 5.0.3 on 2024-04-17 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Account", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="permissions",
            name="Operation",
        ),
        migrations.AddField(
            model_name="permissions",
            name="can_modify",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="permissions",
            name="can_view",
            field=models.BooleanField(default=False),
        ),
    ]