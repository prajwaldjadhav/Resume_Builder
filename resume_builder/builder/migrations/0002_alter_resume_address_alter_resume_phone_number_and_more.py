# Generated by Django 5.0.4 on 2024-05-07 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("builder", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="resume",
            name="address",
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name="resume",
            name="phone_number",
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name="skill",
            name="level",
            field=models.CharField(max_length=50),
        ),
    ]
