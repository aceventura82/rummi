# Generated by Django 3.0.6 on 2020-05-17 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rummiApp', '0003_auto_20200517_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='code',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]