# Generated by Django 3.0.6 on 2020-05-19 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rummiApp', '0009_auto_20200519_0832'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='chairPos',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='game',
            name='currentPlayerPos',
            field=models.IntegerField(default=0),
        ),
    ]
