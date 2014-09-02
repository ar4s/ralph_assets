# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ralph_assets.history.utils import context


def pre_save(sender, instance, **kwargs):
    context.start(instance)


def post_save(sender, instance, **kwargs):
    context.end()


def m2m_changed(sender, instance, action, reverse, model, pk_set, **kwargs):
    if not context.obj and action in ['pre_clear', 'pre_add']:
        context.start(instance, m2m=True)
    elif action == 'post_add':
        context.end()
