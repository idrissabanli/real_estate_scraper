# Generated by Django 2.0.1 on 2019-06-27 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('real_estate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchword',
            name='status',
            field=models.PositiveIntegerField(choices=[(1, 'In process'), (2, 'Failed'), (3, 'Done')], default=1),
        ),
    ]
