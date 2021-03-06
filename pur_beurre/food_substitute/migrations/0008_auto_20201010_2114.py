# Generated by Django 3.0.4 on 2020-10-10 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food_substitute', '0007_auto_20201004_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorites',
            name='products',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prod_id', to='food_substitute.Products'),
        ),
        migrations.AlterField(
            model_name='favorites',
            name='substitute',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subs_id', to='food_substitute.Products'),
        ),
        migrations.AlterField(
            model_name='products',
            name='category',
            field=models.ManyToManyField(to='food_substitute.Category'),
        ),
    ]
