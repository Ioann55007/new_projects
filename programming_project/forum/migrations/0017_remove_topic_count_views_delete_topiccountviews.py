# Generated by Django 4.1 on 2022-09-10 04:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0016_topic_count_views_topiccountviews'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='count_views',
        ),
        migrations.DeleteModel(
            name='TopicCountViews',
        ),
    ]
