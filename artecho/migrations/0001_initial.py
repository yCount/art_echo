# Generated by Django 5.0.1 on 2024-03-22 13:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=128, unique=True)),
                ("totalPosts", models.IntegerField(default=0)),
                ("totalLikes", models.IntegerField(default=0)),
                ("slug", models.SlugField()),
            ],
            options={
                "verbose_name_plural": "categories",
            },
        ),
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=128)),
                ("isAI", models.BooleanField(default=False)),
                ("file", models.ImageField(upload_to="images/")),
                ("likes", models.IntegerField(default=0)),
                ("description", models.TextField(max_length=1000)),
                ("slug", models.SlugField()),
                ("nameSlug", models.SlugField()),
                ("slashSlug", models.CharField(default="null", max_length=128)),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="artecho.category",
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="artecho.image",
                    ),
                ),
                (
                    "poster",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "images",
            },
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("type", models.CharField(max_length=128)),
                (
                    "profilePicture",
                    models.ImageField(
                        default="images/blank_pfp.png", upload_to="profilePics/"
                    ),
                ),
                ("bio", models.TextField(max_length=1000)),
                ("totalLikes", models.IntegerField(default=0)),
                ("slug", models.SlugField(null=True, unique=True)),
                ("liked", models.ManyToManyField(default=None, to="artecho.image")),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
