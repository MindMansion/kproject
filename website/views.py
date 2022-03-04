from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.views.generic import TemplateView, ListView, DetailView
from .models import Article, ArticleSeries, LearnLanguage, LearnSeries, Learn, LearnContent, About, Project, AboutTimeLine
from django.http import Http404
from django.db.models import Q
from itertools import chain
import random


class IndexView(TemplateView):
    template_name = 'website/index.html'
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        python_langs = {}
        swift_langs = {}

        for i in LearnSeries.objects.filter(language__learn_lang_slug='python', learn__learn_slug__isnull=False)[:1]:
            python_langs[i] = Learn.objects.filter(series__learn_lang_series_slug=i.learn_lang_series_slug)

        for i in LearnSeries.objects.filter(language__learn_lang_slug='swift', learn__learn_slug__isnull=False)[:1]:
            swift_langs[i] = Learn.objects.filter(series__learn_lang_series_slug=i.learn_lang_series_slug)

        context['articles'] = Article.objects.filter(card_size='SM').order_by('-published_date')[:4]
        context['articles_big'] = Article.objects.filter(card_size='MD').order_by('-published_date').first()
        context['python_lang'] = python_langs
        context['swift_langs'] = swift_langs
        context['projects'] = Project.objects.all().order_by('-published_date')[:2]

        return context


class LearnView(ListView):
    model = LearnLanguage
    template_name = 'website/learn-view.html'
    context_object_name = 'languages'

    def get_queryset(self):
        series = LearnLanguage.objects.all()
        return get_list_or_404(series)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cpp_langs = {}
        python_langs = {}
        swift_langs = {}

        for i in LearnSeries.objects.filter(language__learn_lang_slug='python', published=True)[:2]:
            python_langs[i] = Learn.objects.filter(series__learn_lang_series_slug=i.learn_lang_series_slug)

        for i in LearnSeries.objects.filter(language__learn_lang_slug='swift', published=True)[:2]:
            swift_langs[i] = Learn.objects.filter(series__learn_lang_series_slug=i.learn_lang_series_slug)

        for i in LearnSeries.objects.filter(language__learn_lang_slug='cpp', published=True)[:2]:
            cpp_langs[i] = Learn.objects.filter(series__learn_lang_series_slug=i.learn_lang_series_slug)

        context['series'] = LearnSeries.objects.all()
        context['cpp_langs'] = cpp_langs
        context['python_lang'] = python_langs
        context['swift_langs'] = swift_langs
        return context


class LearnSeriesView(ListView):
    model = LearnSeries
    context_object_name = 'learn_series'
    template_name = 'website/learn_series_list.html'
    slug_field = 'learn_lang_series_slug'
    slug_url_kwarg = 'learn_lang_series_slug'

    def get_queryset(self):
        slug = self.kwargs['learn_lang_slug']
        series = LearnSeries.objects.all().filter(language__learn_lang_slug=slug)
        # series = LearnSeries.objects.all()
        # return get_list_or_404(series)
        return series

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('learn_lang_slug')
        learn_series_list = {}

        for i in LearnSeries.objects.filter(language__learn_lang_slug=slug, learn__learn_slug__isnull=False):
            learn_series_list[i] = Learn.objects.filter(series__learn_lang_series_slug=i.learn_lang_series_slug)

        context['parent'] = LearnLanguage.objects.get(learn_lang_slug=slug)
        context['learn_series_list'] = learn_series_list
        return context


class LearnDetailView(DetailView):
    template_name = 'website/learn_detail.html'
    context_object_name = 'learn'
    slug_field = 'learn_slug'
    slug_url_kwarg = 'learn_slug'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('learn_slug')

        learn_lang_slugs = [slug.learn_lang_slug for slug in LearnLanguage.objects.all()]
        learn_lang_series_slugs = [slug.learn_lang_series_slug for slug in LearnSeries.objects.all()]

        if not (self.kwargs['learn_lang_slug'] in learn_lang_slugs and self.kwargs['learn_lang_series_slug']
                in learn_lang_series_slugs):
            raise Http404
        return get_object_or_404(Learn, learn_slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('learn_slug')
        series_slug = self.kwargs.get('learn_lang_series_slug')

        series_list = Learn.objects.filter(series__learn_lang_series_slug=series_slug)
        index = (*series_list, ).index(self.get_object())

        has_next = index < series_list.count() - 1 and series_list.count()
        next_learn = series_list[index + 1 if has_next else 0]

        context['contents'] = LearnContent.objects.filter(learn__learn_slug=slug)
        context['next'] = next_learn
        return context


class ArticleView(ListView):
    model = ArticleSeries
    context_object_name = 'articles'
    template_name = 'website/article-view.html'

    def get_queryset(self):
        series = ArticleSeries.objects.all()
        return get_list_or_404(series)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slugs = [slug for slug in ArticleSeries.objects.all()]
        article_langs = []
        for slug in slugs:
            article_langs.append(Article.objects.filter(article_series__article_series_slug=slug.article_series_slug).order_by('-published_date')[:5])
        series = list(zip(slugs, article_langs))
        context['langs'] = series
        return context


class ArticleSeriesView(ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'website/article_list.html'

    def get_queryset(self):
        slug = self.kwargs['article_series_slug']
        articles = Article.objects.filter(article_series__article_series_slug=slug).order_by('-published_date')
        return articles

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('article_series_slug')
        context['parent'] = ArticleSeries.objects.get(article_series_slug=slug)
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'website/article_detail.html'
    context_object_name = 'article'
    slug_field = 'article_slug'
    slug_url_kwarg = 'article_slug'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('article_slug')
        if not self.kwargs['article_series_slug'] in [slug.article_series_slug for slug in ArticleSeries.objects.all()]:
            raise Http404
        return get_object_or_404(Article, article_slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('article_slug')
        series_slug = self.kwargs.get('article_series_slug')

        ss = Article.objects.filter(article_series__article_series_slug=series_slug).exclude(article_slug__exact=slug).all()
        series_list = sorted(ss.order_by('published_date'), key=lambda x: random.random())

        context['recommended'] = series_list[:2]
        return context


class ProjectView(ListView):
    model = Project
    template_name = 'website/project-list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.all().order_by('-published_date')


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'website/project_detail.html'
    context_object_name = 'project'
    slug_field = 'project_slug'
    slug_url_kwarg = 'project_slug'


class AboutView(ListView):
    model = About
    template_name = 'website/about-view.html'
    context_object_name = 'about'

    def get_queryset(self):
        return About.objects.all().first()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['timelines'] = AboutTimeLine.objects.all()
        return context


class SearchView(ListView):
    template_name = 'website/search-list.html'
    context_object_name = "results"
    paginate_by = 50
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', None)
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)

        if query is not '' and len(query) >= 2 and query is not None:
            ar = Article.objects.filter(Q(title__icontains=query) | Q(summary__icontains=query))
            lr = Learn.objects.filter(Q(title__icontains=query) | Q(summary__icontains=query))
            pr = Project.objects.filter(Q(title__icontains=query) | Q(summary__icontains=query))

            qs_chain = chain(ar, lr, pr)
            qs = sorted(qs_chain, key=lambda instance: instance.pk, reverse=True)
            self.count = len(qs)
            return qs
        return Article.objects.none()
