# Generated by Django 3.0.6 on 2020-05-19 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rummiApp', '0010_auto_20200519_1658'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='chairPos',
        ),
        migrations.AddField(
            model_name='gameset',
            name='chairPos',
            field=models.IntegerField(default=1),
        ),
    ]
