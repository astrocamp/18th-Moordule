from django import template

register = template.Library()


@register.inclusion_tag("shared/moordule_button.html")
def moordule_button(*, text, color):
    return {"text": text, "color": color}


@register.inclusion_tag("shared/icon.html")
def icon(*, name):
    return {"name": name}
