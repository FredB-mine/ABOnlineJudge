# Generated by Django 4.2.3 on 2023-07-25 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0012_auto_20180501_0436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='info',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='submission',
            name='statistic_info',
            field=models.JSONField(default=dict),
        ),
    ]
