# Generated by Django 4.0.4 on 2022-04-17 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0008_remove_category_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='slug',
            field=models.SlugField(allow_unicode=True, default=1, max_length=200, unique=True),
            preserve_default=False,
        ),
    ]
