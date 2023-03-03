from django.template.defaulttags import register


@register.filter
def cut_text(str):
    if str is not None:
        if len(str) > 50:
            return str[:50] + '...'
        else:
            return str
        
    return ''
