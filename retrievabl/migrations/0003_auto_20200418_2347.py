# Generated by Django 3.0.3 on 2020-04-19 04:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('retrievabl', '0002_auto_20200416_2308'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='search',
            name='article',
        ),
        migrations.RemoveField(
            model_name='search',
            name='rank',
        ),
    ]
