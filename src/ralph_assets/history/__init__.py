# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.db.models import signals

from ralph_assets.history.receivers import post_save, pre_save


registry = {}


def register(model, exclude):
    """Register model to history observer."""
    if exclude is None:
        raise TypeError('Please specified exclude argument.')

    if model in registry:
        raise Exception('{} is arleady registered.'.format(model))

    fields = set([field.name for field in model._meta.fields])
    fields.difference_update(set(exclude))
    registry[model] = fields
    model.__class__.in_history_registry = True

    signals.pre_save.connect(pre_save, sender=model)
    signals.post_save.connect(post_save, sender=model)
