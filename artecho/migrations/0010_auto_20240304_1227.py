# Generated by Django 2.2.28 on 2024-03-04 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artecho', '0009_auto_20240304_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='liked',
            field=models.ManyToManyField(default=None, to='artecho.Image'),
        ),
    ]