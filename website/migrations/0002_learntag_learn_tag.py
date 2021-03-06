# Generated by Django 4.0.2 on 2022-02-16 23:32

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LearnTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('tag_slug', autoslug.fields.AutoSlugField(editable=False, populate_from='title')),
            ],
        ),
        migrations.AddField(
            model_name='learn',
            name='tag',
            field=models.ManyToManyField(to='website.LearnTag', verbose_name='Tag'),
        ),
    ]
