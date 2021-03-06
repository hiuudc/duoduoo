# Generated by Django 3.2 on 2021-06-15 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_delete_exp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='phrasescore',
            name='point',
        ),
        migrations.RemoveField(
            model_name='wordscore',
            name='point',
        ),
        migrations.AddField(
            model_name='phrasescore',
            name='listening',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='phrasescore',
            name='reading',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='phrasescore',
            name='speaking',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='phrasescore',
            name='writing',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='wordscore',
            name='listening',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='wordscore',
            name='reading',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='wordscore',
            name='speaking',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='wordscore',
            name='writing',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='wordtranslation',
            name='part_of_speech',
            field=models.CharField(choices=[('noun', 'noun'), ('pronoun', 'pronoun'), ('adjective', 'adjective'), ('verb', 'verb'), ('adverb', 'adverb'), ('preposition', 'preposition'), ('conjunction', 'conjunction'), ('article', 'article'), ('exclamation', 'exclamation'), ('prefix', 'prefix'), ('abbreviation', 'abbreviation')], max_length=12, null=True),
        ),
    ]
