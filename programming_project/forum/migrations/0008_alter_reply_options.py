# Generated by Django 4.0.6 on 2022-08-21 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0007_alter_reply_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reply',
            options={'ordering': ('-id',), 'verbose_name': 'Reply', 'verbose_name_plural': 'Replies'},
        ),
    ]
