# Generated by Django 3.0.3 on 2020-04-20 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retrievabl', '0005_delete_negwordslm'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='percentage',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='search',
            name='neg',
            field=models.IntegerField(choices=[(1, 'Neg. Filtering'), (0, 'Reg. BM25')], default=1),
        ),
        migrations.AlterField(
            model_name='article',
            name='score',
            field=models.DecimalField(decimal_places=3, max_digits=15),
        ),
    ]
