# Generated by Django 4.1 on 2022-09-08 20:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0013_views'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ip',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='ip',
            name='user',
        ),
    ]
