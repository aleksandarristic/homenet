# Generated by Django 3.2.12 on 2022-03-11 12:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30)),
                ('description', models.TextField(blank=True)),
                ('type', models.CharField(default='DEVICE', max_length=20)),
                ('first_seen', models.DateTimeField(default=django.utils.timezone.now, verbose_name='First seen')),
                ('last_seen', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Last seen')),
                ('mac_address', models.CharField(max_length=17)),
                ('manufacturer', models.TextField(blank=True)),
                ('last_ip', models.GenericIPAddressField(verbose_name='Last known IP')),
            ],
            options={
                'ordering': ['-last_seen'],
            },
        ),
        migrations.CreateModel(
            name='Scan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(max_length=20)),
                ('output', models.TextField(blank=True, default=None, null=True)),
                ('command', models.CharField(max_length=255)),
                ('running', models.BooleanField(default=False)),
                ('devices', models.ManyToManyField(to='monitor.Device')),
            ],
            options={
                'ordering': ['-time'],
            },
        ),
    ]
