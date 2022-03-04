from django.urls import path
from . import views

app_name = 'website'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),

] + [  # learning urls
    path('learn', views.LearnView.as_view(), name="learn-view"),
    path('learn/<slug:learn_lang_slug>', views.LearnSeriesView.as_view(), name="learn-series-list"),
    path('learn/<slug:learn_lang_slug>/<slug:learn_lang_series_slug>/<slug:learn_slug>', views.LearnDetailView.as_view(), name="learn-detail"),

] + [  # articles urls
    path('articles', views.ArticleView.as_view(), name="article-view"),
    path('articles/<slug:article_series_slug>', views.ArticleSeriesView.as_view(), name="article-list"),
    path('articles/<slug:article_series_slug>/<slug:article_slug>', views.ArticleDetailView.as_view(), name="article-detail"),

] + [  # projects and about urls
    path('projects', views.ProjectView.as_view(), name="project-view"),
    path('projects/<slug:project_slug>', views.ProjectDetailView.as_view(), name="project-detail"),
    path('about', views.AboutView.as_view(), name="about-view"),

] + [
    path('search/', views.SearchView.as_view(), name='search-view')
]
