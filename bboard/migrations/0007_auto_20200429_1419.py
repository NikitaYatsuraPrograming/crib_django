# Generated by Django 3.0.5 on 2020-04-29 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0006_machine_spare'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Machine',
        ),
        migrations.DeleteModel(
            name='Spare',
        ),
    ]
