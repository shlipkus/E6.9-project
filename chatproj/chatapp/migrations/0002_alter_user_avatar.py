# Generated by Django 5.0.7 on 2024-07-12 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, height_field=200, upload_to='images', width_field=200),
        ),
    ]
