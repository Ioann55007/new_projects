# Generated by Django 4.1 on 2022-08-30 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0011_topic_reply_topic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='reply_topic',
        ),
    ]
