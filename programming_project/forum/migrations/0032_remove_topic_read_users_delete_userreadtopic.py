# Generated by Django 4.1 on 2022-09-16 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0031_topic_read_users_userreadtopic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='read_users',
        ),
        migrations.DeleteModel(
            name='UserReadTopic',
        ),
    ]