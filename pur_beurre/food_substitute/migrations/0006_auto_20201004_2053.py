# Generated by Django 3.0.4 on 2020-10-04 18:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('food_substitute', '0005_auto_20200423_0859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='category',
            field=models.ManyToManyField(to='food_substitute.Category'),
        ),
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('products_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prod_id', to='food_substitute.Products')),
                ('substitute_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subs_id', to='food_substitute.Products')),
                ('users_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
