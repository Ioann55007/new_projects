# Generated by Django 4.1 on 2022-09-13 14:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0028_alter_topic_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='topic_bookmark', to=settings.AUTH_USER_MODEL),
        ),
    ]
