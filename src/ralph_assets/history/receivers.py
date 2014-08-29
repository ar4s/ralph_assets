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
