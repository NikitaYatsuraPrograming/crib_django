# Generated by Django 3.0.5 on 2020-04-30 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0008_auto_20200429_1420'),
    ]

    operations = [
        migrations.CreateModel(
            name='Img',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='', verbose_name='Изображение')),
                ('desc', models.TextField()),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
            },
        ),
    ]
