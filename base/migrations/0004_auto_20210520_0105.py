# Generated by Django 3.2 on 2021-05-19 18:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20210520_0050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phrasescore',
            name='last_practiced',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='wordscore',
            name='last_practiced',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
