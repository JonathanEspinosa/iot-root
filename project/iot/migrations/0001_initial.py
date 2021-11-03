# Generated by Django 3.0.1 on 2021-11-01 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('rolcode', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=100)),
                ('description', models.CharField(default='', max_length=250)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('typecode', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('usercode', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('name', models.CharField(default='', max_length=100)),
                ('email', models.CharField(default='', max_length=100)),
                ('phone', models.CharField(default='', max_length=15)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('groupcode', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=False)),
                ('fathercode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='iot.Group')),
            ],
        ),
        migrations.CreateModel(
            name='EnergyConsuption',
            fields=[
                ('eneconcode', models.IntegerField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('energyday', models.FloatField(default=False)),
                ('groupcode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iot.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('devicecode', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=False)),
                ('groupcode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iot.Group')),
                ('typecode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iot.Type')),
            ],
        ),
        migrations.CreateModel(
            name='RolUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('rolcode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iot.Rol')),
                ('usercode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iot.User')),
            ],
            options={
                'unique_together': {('rolcode', 'usercode')},
            },
        ),
        migrations.CreateModel(
            name='RolDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('devicecode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iot.Device')),
                ('rolcode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iot.Rol')),
            ],
            options={
                'unique_together': {('rolcode', 'devicecode')},
            },
        ),
    ]
