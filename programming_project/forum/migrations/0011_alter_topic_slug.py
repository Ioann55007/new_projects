# Generated by Django 4.1.7 on 2023-04-08 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0010_alter_topic_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='slug',
            field=models.SlugField(max_length=130, unique=True),
        ),
    ]
