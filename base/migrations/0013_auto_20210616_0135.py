# Generated by Django 3.2 on 2021-06-15 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_auto_20210615_1005'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tag',
            new_name='Topic',
        ),
        migrations.RemoveField(
            model_name='example',
            name='tag',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='tag',
        ),
        migrations.RemoveField(
            model_name='phrase',
            name='tag',
        ),
        migrations.RemoveField(
            model_name='word',
            name='tag',
        ),
        migrations.AddField(
            model_name='example',
            name='topic',
            field=models.ManyToManyField(blank=True, null=True, to='base.Topic'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='topic',
            field=models.ManyToManyField(blank=True, null=True, to='base.Topic'),
        ),
        migrations.AddField(
            model_name='phrase',
            name='topic',
            field=models.ManyToManyField(blank=True, null=True, to='base.Topic'),
        ),
        migrations.AddField(
            model_name='word',
            name='topic',
            field=models.ManyToManyField(blank=True, null=True, to='base.Topic'),
        ),
        migrations.AlterField(
            model_name='exptracker',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='date_created',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='phrasescore',
            name='last_practiced',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='wordscore',
            name='last_practiced',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
