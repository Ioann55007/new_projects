# Generated by Django 4.0.5 on 2022-06-12 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='views',
        ),
    ]
