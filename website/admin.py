from django.contrib import admin
from .models import ArticleSeries, Article, LearnLanguage, LearnSeries, Learn, LearnContent, Project, ArticleTag, LearnTag, About, ProjectContent, AboutTimeLine


class LearnContentInline(admin.TabularInline):
    model = LearnContent
    extra = 1


@admin.register(Learn)
class LearnAdmin(admin.ModelAdmin):
    list_filter = ('series', 'tag', 'published_date')
    list_display = ('title', 'published_date', 'series')
    fieldsets = [
        ('Title/Summary/Image', {"fields": ["title", "summary", "image"]}),
        ("Publish this learning", {"fields": ["published"]}),
        ("Published Date", {"fields": ["published_date", "updated_date"]}),
        ("Belongs to what Series", {"fields": ["series", "tag"]}),
    ]
    inlines = [LearnContentInline]


@admin.register(LearnContent)
class LearnContentAdmin(admin.ModelAdmin):
    list_filter = ('learn', 'content_type', 'published_date')
    list_display = ('title', 'published_date', 'learn')
    fieldsets = [
        ('Title/Content', {"fields": ["title", "content", ]}),
        ("Preview/Code", {"fields": ["preview", "full_image", "code"]}),
        ("Belongs to what learn", {"fields": ["learn"]}),
        ("Set States", {"fields": ["content_type", "show_preview"]}),
    ]


@admin.register(LearnSeries)
class LearnSeriesAdmin(admin.ModelAdmin):
    list_filter = ('language', 'published')
    list_display = ('title', 'language')


class ProjectContentInline(admin.TabularInline):
    model = ProjectContent
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_filter = ('is_external', 'published_date')
    list_display = ('title', 'is_external')
    fieldsets = [
        ('PROJECT DESCRIPTION', {"fields": ['title', 'summary', 'image', 'preview', 'link', 'published_date']}),
        ('PROJECT STATE', {"fields": ['published', 'is_external']})
    ]
    inlines = [ProjectContentInline]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_filter = ('article_series', 'tag', 'published_date')
    list_display = ('title', 'published_date', 'article_series')


class AboutTimeLineInline(admin.TabularInline):
    model = AboutTimeLine
    extra = 1


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    inlines = [AboutTimeLineInline]


admin.site.register(ArticleSeries)
admin.site.register(ArticleTag)
admin.site.register(LearnLanguage)
admin.site.register(LearnTag)

