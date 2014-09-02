# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.core import serializers
from django.db.models import Model

from ralph_assets.history.models import History


def get_choices(instance, field, id):
    try:
        id = int(id)
    except (TypeError, ValueError):
        return id
    choices = instance._meta.get_field_by_name(field)[0].get_choices()
    for choice_id, value in choices:
        if choice_id == id:
            return value


class DictDiffer(object):
    """Based on stack overflow answer."""
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current = set(current_dict.keys())
        self.set_past = set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)

    def changed(self):
        return set(
            change for change in self.intersect
            if self.past_dict[change] != self.current_dict[change]
        )


class ListDiffer(object):
    def __init__(self, current, past):
        self.current, self.past = current, past

    def changed(self):
        self.past = set(self.past)
        return [item for item in self.current if item not in self.past]


class HistoryContext(object):

    def __init__(self):
        self.serializer = serializers.get_serializer("python")()
        self.obj = None

    def pre_save(self):
        self.model = self.obj.__class__
        self.pre_obj = None
        try:
            self.pre_obj = self.model._default_manager.get(pk=self.obj.pk)
        except self.model.DoesNotExist:
            return
        self.past_snapshot = self.get_fields_snapshot(self.pre_obj)

    def get_fields_snapshot(self, obj):
        return self.serializer.serialize(
            [obj],
            fields=self.registry[obj.__class__],
        )[0]['fields']

    @property
    def registry(self):
        if self.m2m and self.model.in_history_m2m_registry:
            from ralph_assets.history import registry_m2m
            return registry_m2m
        if not self.m2m and self.model.in_history_registry:
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
            old_field, _, _, _ = self.pre_obj._meta.get_field_by_name(field)
            new_field, _, _, _ = self.obj._meta.get_field_by_name(field)

            if hasattr(old_field, 'choices') and old_field.choices:
                if int(old_value) == int(new_value):
                    continue
                old_value = get_choices(self.pre_obj, field, old_value)
                new_value = get_choices(self.obj, field, new_value)
            elif hasattr(self.obj, 'get_{}_display'.format(field)):
                old_value = getattr(
                    self.pre_obj, 'get_{}_display'.format(field)
                )()
                new_value = getattr(
                    self.obj, 'get_{}_display'.format(field)
                )()
            elif isinstance(new_field, Model):
                old_value = str(getattr(self.pre_obj, field))
                new_value = str(getattr(self.obj, field))
            diff_data.append(
                {
                    'field': field,
                    'old': old_value,
                    'new': new_value,
                }
            )
        History.objects.log_changes(self.obj, self.obj.saving_user, diff_data)

        if self.m2m and self.model.in_history_m2m_symetric:
            affected_field = self.obj.__class__._meta.object_name.lower()
            for diff in diff_data:
                added = set(diff['new']).difference(diff['old'])
                for pk in added:
                    model = getattr(self.obj, diff['field']).model
                    obj = model._default_manager.get(pk=pk)
                    related_name = self.model._meta.get_field_by_name(
                        diff['field']
                    )[0].related_query_name()
                    all_related = (
                        getattr(obj, related_name + '_set', None)
                        or getattr(obj, related_name)
                    ).all
                    History.objects.log_changes(obj, self.obj.saving_user, [{
                        'field': affected_field,
                        'old': str(self.obj),
                        'new': ', '.join([str(o) for o in all_related()]),
                    }])

    def start(self, obj, m2m=False):
        self.m2m = m2m
        self.obj = obj
        self.pre_save()

    def end(self):
        self.post_save()
        self.m2m = False
        self.obj = None

context = HistoryContext()
