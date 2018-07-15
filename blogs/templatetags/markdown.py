import bleach
from bleach_whitelist import bleach_whitelist
from django import template
import markdown as md

register = template.Library()
extensions = ['pymdownx.extra', 'pymdownx.emoji', 'pymdownx.progressbar', 'pymdownx.magiclink', 'pymdownx.mark',
              'pymdownx.keys', 'pymdownx.smartsymbols', 'pymdownx.superfences', 'pymdownx.highlight',
              'pymdownx.tasklist', 'pymdownx.details']

markdown_tags = bleach_whitelist.markdown_tags + [
    'kbd', 'mark', 'details', 'pre', 'summary', 'input', 'label', 'span', 'div',
    'table', 'tbody', 'thead', 'td', 'th', 'tr'
]

markdown_attrs = {
    "details": ["open", "class"],
    "img": ["src", "alt", "title", "class"],
    "a": ["href", "alt", "title"],
    "input": ["class", "checked", "id", "name", "type", "disabled"],
    "label": ["for", "class"],
    "span": ["class"],
    "pre": ["class"],
    "div": ["class", "style"],
    "ul": ["class"],
    "li": ["class"],
    "p": ["class"]
}


@register.filter(name='markdown')
def markdown(string):
    formatted = md.markdown(string, extensions, safe_mode='escape')
    return bleach.clean(formatted, tags=markdown_tags, attributes=markdown_attrs, styles=['width'])

