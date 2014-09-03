# -*- coding: utf-8 -*-
"""Templatetags specific for ralph_assets"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django import template
from django.utils.translation import ugettext_lazy as _

from ralph_assets.history.models import History


register = template.Library()


def get_history_queryset(obj):
    return History.objects.get_history_for_this_object(obj=obj)


def get_context(obj, history, limit, full_history_button, title):
    return {
        'full_history_button': full_history_button,
        'history_for_model_url': History.get_history_url_for_object(obj),
        'history_title': _('Short history'),
        'limit': limit,
        'history': history[:limit] if history else None,
    }


@register.inclusion_tag('assets/templatetags/short_history.html')
def short_history(obj, limit=5, full_history_button=True):
    """Render a short history table."""
    history = get_history_queryset(obj)
    if not history:
        return {}
    return get_context(
        obj,
        history.order_by('date'),
        limit,
        full_history_button,
        _('Short history')
    )


@register.inclusion_tag('assets/templatetags/short_history.html')
def status_history(obj, limit=5, full_history_button=True):
    """Render a short history table only for status changes."""
    history = get_history_queryset(obj)
    if not history:
        return {}
    return get_context(
        obj,
        history.filter(field_name__exact='status').order_by('date'),
        limit,
        full_history_button,
        _('Status history')
    )
