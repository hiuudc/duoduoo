# Generated by Django 3.2 on 2021-05-19 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='id',
            field=models.CharField(max_length=3, primary_key=True, serialize=False),
        ),
    ]
