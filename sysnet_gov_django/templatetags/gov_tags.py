from django import template

register = template.Library()

@register.inclusion_tag('gov_django/components/button.html')
def gov_button(text, type='primary', size='md', disabled=False, **kwargs):
    return {
        'text': text,
        'type': type,
        'size': size,
        'disabled': disabled,
        'extra_classes': kwargs.get('class', ''),
        'id': kwargs.get('id', '')
    }

@register.inclusion_tag('gov_django/components/alert.html')
def gov_alert(text, type='info', title=None):
    return {
        'text': text,
        'type': type,
        'title': title
    }
