from django.conf import settings

from django import template

register = template.Library()


@register.simple_tag
def get_from_iframe_src(value, want="src"):
    [src, height] = value.split(" ")
    if not height:
        height = "600px"
    if want == "src":
        if "ALLOWABLE_IFRAME_SRCS" in settings.PYUSITE:
            for allowable_iframe_src in settings.PYUSITE["ALLOWABLE_IFRAME_SRCS"]:
                if src.find(allowable_iframe_src) == 0:
                    return src

    if want == "height":
        return height
