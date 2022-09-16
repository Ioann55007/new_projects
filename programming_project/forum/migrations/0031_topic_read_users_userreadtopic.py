# Generated by Django 4.1 on 2022-09-16 15:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0030_alter_topic_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='read_users',
            field=models.ManyToManyField(related_name='user_read', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='UserReadTopic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read_at', models.DateTimeField(auto_now=True)),
                ('topic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='forum.topic')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
