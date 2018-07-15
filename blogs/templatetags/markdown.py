from django import template

import markdown as md

register = template.Library()
extensions = ['pymdownx.extra', 'pymdownx.emoji', 'pymdownx.progressbar', 'pymdownx.magiclink', 'pymdownx.mark',
              'pymdownx.keys', 'pymdownx.smartsymbols', 'pymdownx.superfences', 'pymdownx.highlight',
              'pymdownx.tasklist', 'pymdownx.details']


@register.filter(name='markdown')
def markdown(string):
    print(string)
    return md.markdown(string, extensions)
