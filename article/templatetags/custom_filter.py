from django import template
from django.utils.translation import gettext, gettext_lazy, gettext_noop, activate
from django.template.defaultfilters import stringfilter
import re

register = template.Library()


@register.filter
@stringfilter
def upto(value, delimiter=None):
    return value.split(delimiter)[0]


upto.is_safe = True


@register.filter
def custom_trans(s, language):

    re.findall("(\w+) starts following you", s)
    return gettext_lazy(s)


@register.filter
def times(number):
    return range(1, number+1)
