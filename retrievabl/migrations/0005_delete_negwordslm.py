# Generated by Django 3.0.3 on 2020-04-19 20:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('retrievabl', '0004_article_score'),
    ]

    operations = [
        migrations.DeleteModel(
            name='NegWordsLM',
        ),
    ]
