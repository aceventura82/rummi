# Generated by Django 3.0.6 on 2020-05-18 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rummiApp', '0007_auto_20200518_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='started',
            field=models.BooleanField(default=False),
        ),
    ]
