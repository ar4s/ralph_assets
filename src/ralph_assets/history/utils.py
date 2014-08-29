# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from threading import local

from django.core import serializers

from ralph_assets.history.models import History


class DictDiffer(object):
    """Based on stack overflow"""
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)

    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])


class ThreadContext(object):

    def __init__(self):
        self.storage = local()
        self.serializer = serializers.get_serializer("python")()

    def pre_save(self):
        model = self.obj.__class__
        self.pre_obj = None
        try:
            self.pre_obj = model._default_manager.get(pk=self.obj.pk)
        except model.DoesNotExist:
            pass

    def post_save(self):
        from ralph_assets.history import registry
        if not self.pre_obj:
            return
        present, past = self.serializer.serialize(
            [self.obj, self.pre_obj],
            fields=registry[self.obj.__class__],
        )
        fields_diff = DictDiffer(present['fields'], past['fields']).changed()

        diff_data = []
        for field in fields_diff:
            old_value, new_value = past['fields'][field], present['fields'][field]
            if hasattr(self.pre_obj, 'get_{}_display'.format(field)):
                old_value = getattr(
                    self.pre_obj, 'get_{}_display'.format(field)
                )()
                new_value = getattr(
                    self.obj, 'get_{}_display'.format(field)
                )()
            diff_data.append(
                {
                    'field': field,
                    'old': old_value,
                    'new': new_value,
                }
            )
        History.objects.log_changes(self.obj, diff_data)

    def start(self, obj):
        self.storage.lock = True
        self.obj = obj
        self.pre_save()

    def end(self):
        self.storage.lock = False
        self.post_save()

context = ThreadContext()
