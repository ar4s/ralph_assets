# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.core import serializers
from django.db.models import Model

from ralph_assets.history.models import History


class DictDiffer(object):
    """Based on stack overflow answer."""
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current = set(current_dict.keys())
        self.set_past = set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)

    def changed(self):
        return set(
            o for o in self.intersect
            if self.past_dict[o] != self.current_dict[o]
        )


class ListDiffer(object):
    def __init__(self, current, past):
        self.current, self.past = current, past

    def changed(self):
        self.past = set(self.past)
        return [item for item in self.current if item not in self.past]


class Context(object):

    def __init__(self):
        self.serializer = serializers.get_serializer("python")()

    def pre_save(self):
        model = self.obj.__class__
        self.pre_obj = None
        try:
            self.pre_obj = model._default_manager.get(pk=self.obj.pk)
        except model.DoesNotExist:
            return
        self.past_snapshot = self.get_fields_snapshot(self.pre_obj)

    def get_fields_snapshot(self, obj):
        return self.serializer.serialize(
            [obj],
            fields=self.registry[obj.__class__],
        )[0]['fields']

    @property
    def registry(self):
        if self.m2m and self.obj.__class__.in_history_m2m_registry:
            from ralph_assets.history import registry_m2m
            return registry_m2m
        if not self.m2m and self.obj.__class__.in_history_registry:
            from ralph_assets.history import registry
            return registry

    def post_save(self):
        if not self.pre_obj:
            return
        current_snapshot = self.get_fields_snapshot(self.obj)

        fields_diff = DictDiffer(
            current_snapshot, self.past_snapshot).changed()

        diff_data = []
        for field in fields_diff:
            old_value = self.past_snapshot[field]
            new_value = current_snapshot[field]
            old_field = getattr(self.pre_obj, field)
            new_field = getattr(self.obj, field)

            if hasattr(self.pre_obj, 'get_{}_display'.format(field)):
                old_value = getattr(
                    self.pre_obj, 'get_{}_display'.format(field)
                )()
                new_value = getattr(
                    self.obj, 'get_{}_display'.format(field)
                )()
            if isinstance(old_field, Model):
                old_value = str(old_field)
                new_value = str(new_field)
            diff_data.append(
                {
                    'field': field,
                    'old': old_value,
                    'new': new_value,
                }
            )
        History.objects.log_changes(self.obj, diff_data)
        if self.m2m and self.obj.__class__.in_history_m2m_symetric:
            field = self.obj.__class__._meta.object_name.lower()
            for diff in diff_data:
                added = set(diff['new']).difference(diff['old'])
                print(added)
                for pk in added:
                    model = getattr(self.obj, diff['field']).model
                    obj = model._default_manager.get(pk=pk)
                    History.objects.log_changes(obj, [{
                        'field': field,
                        'old': '-',
                        'new': str(obj),
                    }])

    def start(self, obj, m2m=False):
        self.m2m = m2m
        self.obj = obj
        self.pre_save()

    def end(self):
        self.post_save()

context = Context()
