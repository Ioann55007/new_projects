# Generated by Django 4.1.7 on 2023-04-06 08:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0006_remove_topic_views_topic_count_views_topiccountviews'),
    ]

    operations = [
        migrations.CreateModel(
            name='Viewer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ipaddress', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP address')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='topic',
            name='count_views',
        ),
        migrations.DeleteModel(
            name='TopicCountViews',
        ),
        migrations.AddField(
            model_name='topic',
            name='viewers',
            field=models.ManyToManyField(to='forum.viewer'),
        ),
    ]
