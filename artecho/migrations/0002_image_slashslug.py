# Generated by Django 2.2.28 on 2024-03-20 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artecho', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='slashSlug',
            field=models.CharField(default='null', max_length=128),
        ),
    ]