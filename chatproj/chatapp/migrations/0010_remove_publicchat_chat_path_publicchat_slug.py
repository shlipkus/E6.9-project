# Generated by Django 5.0.7 on 2024-07-19 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0009_alter_publicchat_owner_publicmessage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publicchat',
            name='chat_path',
        ),
        migrations.AddField(
            model_name='publicchat',
            name='slug',
            field=models.SlugField(default='', unique=True),
        ),
    ]
