#--encoding=utf-8--
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def to_unicode(value):
    return unicode(value)

@register.filter
@stringfilter
def cost_type(value):
    res=['差旅', '采购', '业务招待']
    try:
        return res[int(value)]
    except Exception as e:
        return value

@register.filter
@stringfilter
def holiday_type(value):
    res=['事假', '病假', '婚假', '产假', '年假']
    try:
        return res[int(value)]
    except Exception as e:
        return value

@register.filter
@stringfilter
def current_status(value):
    res = ['已新建', '已提交', '已同意', '已驳回']
    try:
        return res[int(value)]
    except Exception as e:
        return value

@register.filter
@stringfilter
def sex_ch(value):
    res = ['女', '男', '--']
    return res[int(value)]