# Generated by Django 3.0.3 on 2020-04-19 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retrievabl', '0003_auto_20200418_2347'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='score',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=15),
            preserve_default=False,
        ),
    ]
