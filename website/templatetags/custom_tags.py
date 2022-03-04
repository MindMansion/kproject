from django import template

register = template.Library()


@register.filter(name='toc')
def toc_style(toc):
    els = {
        "h2": "toc-h2",
        "h3": "toc-h3",
        "h4": "toc-h4",
        "h5": "toc-h5",
        "h6": "toc-h6"
    }
    if toc in els.keys():
        return els[toc]
    return 'toc'
