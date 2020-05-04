# Generated by Django 3.0.5 on 2020-04-29 13:57

import bboard.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0004_auto_20200425_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bb',
            name='price',
            field=models.FloatField(blank=True, null=True, validators=[bboard.validators.validate_even], verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='bb',
            name='title',
            field=models.CharField(error_messages={'invalid': 'Неправильное название товара'}, max_length=50, validators=[django.core.validators.RegexValidator(regex='[a-zA-Z0-9А-Яа-я_]')], verbose_name='Товары'),
        ),
    ]
