# Generated by Django 5.1.2 on 2024-11-01 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_user_first_name_user_last_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="canvas_api_key",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]