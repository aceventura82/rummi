# Generated by Django 3.0.6 on 2020-05-17 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rummiApp', '0002_tmppin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameset',
            name='fullDraw',
            field=models.BooleanField(default=False),
        ),
    ]
