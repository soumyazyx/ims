# Generated by Django 3.0.4 on 2020-03-29 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0002_auto_20200329_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='greeting',
            name='latest_stats_value',
            field=models.IntegerField(default=0),
        ),
    ]
