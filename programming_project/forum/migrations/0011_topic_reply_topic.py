# Generated by Django 4.1 on 2022-08-30 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0010_remove_topic_date_end_remove_topic_date_start'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='reply_topic',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replyas', to='forum.reply'),
        ),
    ]