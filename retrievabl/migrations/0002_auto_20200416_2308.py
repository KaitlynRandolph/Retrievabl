# Generated by Django 3.0.3 on 2020-04-17 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retrievabl', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='source',
            field=models.CharField(default=0, max_length=75),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='url',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]
