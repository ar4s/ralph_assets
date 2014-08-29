# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.db.models import signals

from ralph_assets.history.receivers import post_save, pre_save


registry = {}


def register(model, exclude=None):
    """Register model to history observer."""
    if exclude is None:
        raise TypeError('Please specified fields or exclude argument.')

    if model in registry:
        raise Exception('{} is arleady registered.')

    fields = []
    for field in model._meta.fields:
        if field.name not in exclude:
            fields.append(field.name)
    registry[model] = fields

    signals.pre_save.connect(pre_save, sender=model)
    signals.post_save.connect(post_save, sender=model)
