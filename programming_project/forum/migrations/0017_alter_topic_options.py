# Generated by Django 4.0.6 on 2022-08-14 04:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0016_alter_topic_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='topic',
            options={'verbose_name': 'Topic', 'verbose_name_plural': 'Topics'},
        ),
    ]
