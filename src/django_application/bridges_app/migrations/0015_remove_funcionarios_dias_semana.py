# Generated by Django 3.0.6 on 2020-07-01 03:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bridges_app', '0014_auto_20200701_0000'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='funcionarios',
            name='dias_semana',
        ),
    ]
