# Generated by Django 3.2.12 on 2022-03-17 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='is_trusted',
            field=models.BooleanField(default=False),
        ),
    ]