# Generated by Django 3.0.6 on 2020-05-17 18:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('private', models.BooleanField(db_index=True, default=False)),
                ('fullDraw', models.CharField(default='', max_length=6)),
                ('speed', models.IntegerField(default=5)),
                ('maxPlayers', models.IntegerField(default=4)),
                ('code', models.CharField(max_length=5, unique=True)),
                ('current_set', models.IntegerField(default=1)),
                ('current_stack', models.CharField(default='', max_length=500)),
                ('current_discarted', models.CharField(default='', max_length=500)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('lastname', models.CharField(blank=True, max_length=50, null=True)),
                ('nickname', models.CharField(blank=True, max_length=20, null=True)),
                ('gender', models.CharField(blank=True, db_index=True, max_length=1, null=True)),
                ('city', models.CharField(blank=True, db_index=True, max_length=50, null=True)),
                ('country', models.CharField(blank=True, db_index=True, max_length=50, null=True)),
                ('birthDate', models.DateField(blank=True, null=True)),
                ('extension', models.CharField(blank=True, max_length=5, null=True)),
                ('notifications', models.CharField(blank=True, default='OFF', max_length=5, null=True)),
                ('status', models.CharField(blank=True, db_index=True, max_length=1, null=True)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GameMessages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('msg', models.CharField(max_length=1500)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GameSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('set', models.IntegerField(default=1)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('fullDraw', models.CharField(default='', max_length=6)),
                ('points', models.IntegerField(default=0)),
                ('current_cards', models.CharField(default='', max_length=500)),
                ('drawn', models.CharField(default='', max_length=100)),
                ('gameId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rummiApp.Game')),
                ('playerId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rummiApp.Player')),
            ],
            options={
                'unique_together': {('playerId', 'gameId', 'set')},
            },
        ),
    ]
