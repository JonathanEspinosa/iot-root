# Generated by Django 3.0.1 on 2021-10-03 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0008_auto_20211003_0107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(default='', max_length=15),
        ),
    ]
