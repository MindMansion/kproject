# Generated by Django 4.0.2 on 2022-02-28 02:23

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_project_published_date_alter_project_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_slug',
            field=autoslug.fields.AutoSlugField(default='first project', editable=False, max_length=300, populate_from='title'),
            preserve_default=False,
        ),
    ]
