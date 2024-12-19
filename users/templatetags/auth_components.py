from django import template

register = template.Library()


@register.inclusion_tag("users/components/email_input.html")
def email_input(verbose_name="", value="", error="", placeholder="", validate=True):
    return {
        "verbose_name": verbose_name,
        "value": value,
        "error": error,
        "placeholder": placeholder,
        "should_validate": validate,
    }


@register.inclusion_tag("users/components/password_input.html")
def password_input(
    verbose_name="", name="", value="", error="", placeholder="", validate=True
):
    return {
        "verbose_name": verbose_name,
        "name": name,
        "value": value,
        "error": error,
        "placeholder": placeholder,
        "should_validate": validate,
    }
