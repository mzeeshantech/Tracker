# Generated by Django 5.1.4 on 2025-01-12 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Breaker", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="alarm",
            name="location",
            field=models.CharField(blank=True, null=True),
        ),
    ]