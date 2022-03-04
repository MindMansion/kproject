from autoslug import AutoSlugField
from django.db import models
from tinymce.models import HTMLField
from django.urls import reverse
from datetime import datetime
import readtime
from lxml import etree


class ArticleSeries(models.Model):
    title = models.CharField(max_length=200, help_text="Enter a series name", null=True)
    summary = models.CharField(max_length=300, help_text="Enter short description of the series")
    image = models.ImageField(default="default.jpg", upload_to="articleSeriesImages")
    article_series_slug = AutoSlugField(populate_from='title')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        try:
            this = ArticleSeries.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except:
            pass
        super(ArticleSeries, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('website:article-list', kwargs={'article_series_slug': self.article_series_slug})


class ArticleTag(models.Model):
    title = models.CharField(max_length=50)
    tag_slug = AutoSlugField(populate_from='title')

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=300, help_text="Input the title for this article")
    summary = models.CharField(max_length=300, help_text="Input the summary for this article")
    image = models.ImageField(default="default.jpg", upload_to="articleImages")
    content = HTMLField()
    published_date = models.DateTimeField(default=datetime.now)
    updated_date = models.DateTimeField(default=datetime.now)
    published = models.BooleanField(default=False, help_text="Publish this post")
    no_image = models.BooleanField(default=False, help_text="No Image")
    article_series = models.ForeignKey(ArticleSeries, default=1, verbose_name="ArticleSeries",
                                       on_delete=models.SET_DEFAULT)
    tag = models.ManyToManyField(ArticleTag, verbose_name='Tag')
    article_slug = AutoSlugField(populate_from='title', max_length=300)

    CARD_CHOICES = [
        ('SM', 'Small'),
        ('MD', 'Medium'),
        ('BG', 'Big'),
    ]

    card_size = models.CharField(max_length=2, choices=CARD_CHOICES, default='SM')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        try:
            this = Article.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except:
            pass
        super(Article, self).save(*args, **kwargs)

    def get_toc(self):
        doc = etree.HTML(self.content)
        toc = [(node.tag, node.text) for node in doc.xpath('//h2|//h3|//h4|//h5')]
        return toc

    def get_read_time(self):
        result = readtime.of_html(self.content)
        return result.text

    def get_absolute_url(self):
        return reverse('website:article-detail', kwargs={
            'article_series_slug': self.article_series.article_series_slug,
            'article_slug': self.article_slug
        })


class LearnLanguage(models.Model):
    title = models.CharField(max_length=300, help_text="Input the title for this language")
    summary = models.CharField(max_length=300, help_text="Input the summary for this language")
    image = models.ImageField(default="default.jpg", upload_to="learnImages")
    learn_lang_slug = AutoSlugField(populate_from='title')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        try:
            this = LearnLanguage.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except:
            pass
        super(LearnLanguage, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('website:learn-series-list', kwargs={'learn_lang_slug': self.learn_lang_slug})


class LearnSeries(models.Model):
    title = models.CharField(max_length=300, help_text="Input the title for this language series")
    summary = models.CharField(max_length=300, help_text="Input the summary for this language series")
    image = models.ImageField(default="default.jpg", upload_to="learnImages")
    learn_lang_series_slug = AutoSlugField(populate_from='title')
    language = models.ForeignKey(LearnLanguage, default=1, on_delete=models.SET_DEFAULT)
    published = models.BooleanField(default=False, help_text="Publish this series")

    class Meta:
        verbose_name_plural = 'Learn Series'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        try:
            this = LearnSeries.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except:
            pass
        super(LearnSeries, self).save(*args, **kwargs)


class LearnTag(models.Model):
    title = models.CharField(max_length=50)
    tag_slug = AutoSlugField(populate_from='title')

    def __str__(self):
        return self.title


class Learn(models.Model):
    title = models.CharField(max_length=300, help_text="Input the title for this learn series")
    summary = models.CharField(max_length=300, help_text="Input the summary for this learn series")
    image = models.ImageField(default="default.jpg", upload_to="learnImages")
    published_date = models.DateTimeField(default=datetime.now)
    updated_date = models.DateTimeField(default=datetime.now)
    learn_slug = AutoSlugField(populate_from='title', max_length=300)
    tag = models.ManyToManyField(LearnTag, verbose_name='Tag')
    series = models.ForeignKey(LearnSeries, default=1, on_delete=models.SET_DEFAULT)
    published = models.BooleanField(default=False, help_text="Publish this learning post")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        try:
            this = Learn.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except:
            pass
        super(Learn, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('website:learn-detail', kwargs={
            'learn_lang_slug': self.series.language.learn_lang_slug,
            'learn_lang_series_slug': self.series.learn_lang_series_slug,
            'learn_slug': self.learn_slug
        })


class LearnContent(models.Model):
    title = models.CharField(max_length=300, help_text="Enter post title")
    content = HTMLField()
    code = HTMLField(help_text="Enter in the code")
    published_date = models.DateTimeField(default=datetime.now)
    preview = models.ImageField(default="default.jpg", upload_to="contentPreviews",
                                help_text="Upload image for preview")
    show_preview = models.BooleanField(default=False)
    learn = models.ForeignKey(Learn, on_delete=models.CASCADE, null=True)
    full_image = models.ImageField(default='default.jpg', upload_to="contentImages")

    CONTENT_TYPES = [
        ('BOT', 'Both'),
        ('FUL', 'Full'),
        ('IMG', 'Image'),
    ]

    content_type = models.CharField(max_length=3, choices=CONTENT_TYPES, default='BOT')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        try:
            this = LearnContent.objects.get(id=self.id)
            if this.preview != self.preview:
                this.preview.delete(save=False)

            if this.full_image != self.full_image:
                this.full_image.delete(save=False)
        except:
            pass
        super(LearnContent, self).save(*args, **kwargs)


class Project(models.Model):
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=400)
    link = models.URLField(max_length=300, help_text="Enter project url", blank=True)
    image = models.ImageField(default="default.jpg", upload_to="projectImages")
    preview = models.ImageField(default="default.jpg", upload_to="projectImages")
    published_date = models.DateTimeField(default=datetime.now)
    is_external = models.BooleanField(default=False)
    published = models.BooleanField(default=False, help_text="Publish this project")
    project_slug = AutoSlugField(populate_from='title', max_length=300)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        try:
            this = Project.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)

            if this.preview != self.preview:
                this.preview.delete(save=False)
        except:
            pass
        super(Project, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('website:project-detail', kwargs={
            'project_slug': self.project_slug
        })


class ProjectContent(models.Model):
    title = models.CharField(max_length=100)
    content = HTMLField()
    image = models.ImageField(default='default-project.jpg', upload_to='projectContentImages')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)

    POSITIONS = [
        ('LFT', 'Left'),
        ('RHT', 'Right'),
        ('FUL', 'Full'),
        ('IMG', 'Image'),
    ]
    content_position = models.CharField(max_length=3, choices=POSITIONS, default='LFT')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        try:
            this = ProjectContent.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except:
            pass
        super(ProjectContent, self).save(*args, **kwargs)


class About(models.Model):
    content = HTMLField()

    def __str__(self):
        return "content"


class AboutTimeLine(models.Model):
    title = models.CharField(max_length=100)
    summary = models.CharField(max_length=1000)
    published_date = models.DateTimeField(default=datetime.now)
    link = models.URLField(max_length=300, blank=True)
    about = models.ForeignKey(About, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title
