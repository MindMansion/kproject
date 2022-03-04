from django import template
from website.models import LearnContent, ProjectContent
import readtime

register = template.Library()


@register.filter(name='readtime')
def total_read_time(items):
    times = [get_learn_time(i) for i in items]
    return sum(times)


def get_learn_time(learn):
    contents = LearnContent.objects.filter(learn__learn_slug=learn.learn_slug)
    times = ''.join([time.content for time in contents])
    if times:
        return readtime.of_html(times).minutes
    return 0


@register.filter(name='learnTime')
def learn_read_time(learn):
    contents = LearnContent.objects.filter(learn__learn_slug=learn.learn_slug)
    times = ''.join([time.content for time in contents])
    if times:
        return readtime.of_html(times).text
    return 0


@register.filter(name="contents")
def fetch_project_contents(project):
    contents = ProjectContent.objects.filter(project__project_slug=project.project_slug)
    return contents


@register.filter(name='headline')
def headline(title: str):
    title = title.title()
    h = title.lower()
    if 'swiftui' in h or 'to' in h or 'uikit' in h:
        text = ' '.join([make_capital(i) for i in title.lower().split(' ')])
        title = text
    return title


@register.filter(name='searchValue')
def get_input_query(query):
    if not query:
        return "search site for keywords"
    return query


@register.filter(name='tagColor')
def tag_color(tag: str):
    tags = {
        "swift": "tag-swift",
        "swiftui": "tag-swiftui",
        "python": "tag-python",
        "algorithms": "tag-algo",
    }
    if tag.lower() in tags.keys():
        return tags[tag.lower()]
    return "tag"


@register.filter(name='colorMatch')
def color_match_summary(summary: str, q):
    if summary:
        return ' '.join([color_match(val, q, i) for i, val in enumerate(summary.lower().split(' '))])


def color_match(text, q: str, index):
    if q in text:
        val = text.capitalize() if index is 0 else text
        if q == text:
            return f'<span class="color-match-bg">{make_capital(val)}</span>'
        return f'<span class="color-match">{make_capital(val)}</span>'
    return text.capitalize() if index is 0 else text


def make_capital(text):
    if text == 'swiftui':
        return 'SwiftUI'
    elif text == 'to':
        return 'to'
    elif text == 'uikit':
        return 'UIKit'
    else:
        return text.title()


@register.filter('startswith')
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False

