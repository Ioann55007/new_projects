# Generated by Django 4.0.6 on 2022-08-13 05:15

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0010_alter_topic_managers'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='topic',
            managers=[
                ('newmanager', django.db.models.manager.Manager()),
            ],
        ),
    ]
