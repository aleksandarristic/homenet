# Generated by Django 3.2.16 on 2022-11-17 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_menuurl_post_request'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuurl',
            name='post_warning',
            field=models.CharField(default='', max_length=1024, null=True),
        ),
    ]
