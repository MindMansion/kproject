# Generated by Django 4.0.2 on 2022-02-17 05:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_learntag_learn_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='learn',
            name='published_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='learn',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]