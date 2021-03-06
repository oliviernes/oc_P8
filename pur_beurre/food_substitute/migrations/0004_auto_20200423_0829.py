# Generated by Django 3.0.4 on 2020-04-23 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("food_substitute", "0003_auto_20200418_0907"),
    ]

    operations = [
        migrations.RemoveField(model_name="products", name="image_front",),
        migrations.RemoveField(
            model_name="products", name="image_front_thumb",
        ),
        migrations.AddField(
            model_name="products",
            name="image",
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name="products",
            name="image_small",
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name="products",
            name="category",
            field=models.ManyToManyField(to="food_substitute.Category"),
        ),
        migrations.AlterField(
            model_name="products",
            name="image_nutrition",
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name="products",
            name="url",
            field=models.URLField(null=True),
        ),
    ]
