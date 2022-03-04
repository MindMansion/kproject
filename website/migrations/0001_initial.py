# Generated by Django 4.0.2 on 2022-02-16 22:18

import autoslug.fields
import datetime
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleSeries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Enter a series name', max_length=200, null=True)),
                ('summary', models.CharField(help_text='Enter short description of the series', max_length=300)),
                ('image', models.ImageField(default='default.jpg', upload_to='articleSeriesImages')),
                ('article_series_slug', autoslug.fields.AutoSlugField(editable=False, populate_from='title')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('tag_slug', autoslug.fields.AutoSlugField(editable=False, populate_from='title')),
            ],
        ),
        migrations.CreateModel(
            name='Learn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Input the title for this learn series', max_length=300)),
                ('summary', models.CharField(help_text='Input the summary for this learn series', max_length=300)),
                ('image', models.ImageField(default='default.jpg', upload_to='learnImages')),
                ('learn_slug', autoslug.fields.AutoSlugField(editable=False, max_length=300, populate_from='title')),
                ('published', models.BooleanField(default=False, help_text='Publish this learning post')),
            ],
        ),
        migrations.CreateModel(
            name='LearnLanguage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Input the title for this language', max_length=300)),
                ('summary', models.CharField(help_text='Input the summary for this language', max_length=300)),
                ('image', models.ImageField(default='default.jpg', upload_to='learnImages')),
                ('learn_lang_slug', autoslug.fields.AutoSlugField(editable=False, populate_from='title')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('summary', models.CharField(max_length=400)),
                ('link', models.URLField(help_text='Enter project url', max_length=300)),
                ('image', models.ImageField(default='default.jpg', upload_to='projectImages')),
                ('published', models.BooleanField(default=False, help_text='Publish this project')),
            ],
        ),
        migrations.CreateModel(
            name='LearnSeries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Input the title for this language series', max_length=300)),
                ('summary', models.CharField(help_text='Input the summary for this language series', max_length=300)),
                ('image', models.ImageField(default='default.jpg', upload_to='learnImages')),
                ('learn_lang_series_slug', autoslug.fields.AutoSlugField(editable=False, populate_from='title')),
                ('published', models.BooleanField(default=False, help_text='Publish this series')),
                ('language', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='website.learnlanguage')),
            ],
            options={
                'verbose_name_plural': 'Learn Series',
            },
        ),
        migrations.CreateModel(
            name='LearnContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Enter post title', max_length=300)),
                ('content', tinymce.models.HTMLField(default='Content')),
                ('code', tinymce.models.HTMLField(default='Enter code', help_text='Enter in the code')),
                ('published_date', models.DateTimeField(default=datetime.datetime.now)),
                ('preview', models.ImageField(default='default.jpg', help_text='Upload image for preview', upload_to='contentPreviews')),
                ('full_content', models.BooleanField(default=False)),
                ('learn', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.learn')),
            ],
        ),
        migrations.AddField(
            model_name='learn',
            name='series',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='website.learnseries'),
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Input the title for this article', max_length=300)),
                ('summary', models.CharField(help_text='Input the summary for this article', max_length=300)),
                ('image', models.ImageField(default='default.jpg', upload_to='articleImages')),
                ('content', tinymce.models.HTMLField()),
                ('published_date', models.DateTimeField(default=datetime.datetime.now)),
                ('updated_date', models.DateTimeField(default=datetime.datetime.now)),
                ('published', models.BooleanField(default=False, help_text='Publish this post')),
                ('article_slug', autoslug.fields.AutoSlugField(editable=False, max_length=300, populate_from='title')),
                ('card_size', models.CharField(choices=[('SM', 'Small'), ('MD', 'Medium'), ('BG', 'Big')], default='SM', max_length=2)),
                ('article_series', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='website.articleseries', verbose_name='ArticleSeries')),
                ('tag', models.ManyToManyField(to='website.ArticleTag', verbose_name='Tag')),
            ],
        ),
    ]
