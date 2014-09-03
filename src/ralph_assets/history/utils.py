# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.core import serializers
from django.db.models import Model
from django.db.models.fields import FieldDoesNotExist
from django.db.models.fields.related import RelatedField
from django.utils.functional import cached_property

from ralph_assets.history.models import History


def field_changes(instance, ignore=('id', 'ralph_device_id')):
    """Yield the name, original value and new value for each changed field.
    Skip all insignificant fields and those passed in ``ignore``.
    When creating asset, the first asset status will be added into the history.
    """
    from ralph_assets.models_assets import Asset
    if isinstance(instance, Asset) and instance.cache_version == 0:
        yield 'status', '–', get_choices(instance, 'status', instance.status)
    for field, orig in instance.dirty_fields.iteritems():
        if field in ignore:
            continue
        if field in instance.insignificant_fields:
            continue
        field_object = None
        try:
            field_object, _, _, _ = instance._meta.get_field_by_name(field)
        except FieldDoesNotExist:
            try:
                field = field[:-3]
                field_object, _, _, _ = instance._meta.get_field_by_name(field)
            except FieldDoesNotExist:
                continue
        if isinstance(field_object, RelatedField):
            parent_model = field_object.related.parent_model
            try:
                if orig is not None:
                    orig = parent_model.objects.get(pk=orig)
            except parent_model.DoesNotExist:
                orig = None
        try:
            new = getattr(instance, field)
        except AttributeError:
            continue
        if field in ('office_info', 'device_info', 'part_info'):
            continue
        if hasattr(field_object, 'choices') and field_object.choices:
            new = get_choices(instance, field, new)
            orig = get_choices(instance, field, orig)
        if field == 'attachment':
            if str(orig).strip() == str(new).strip():
                continue
        yield field, orig, new


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

    def get_fields_snapshot(self, objs):
        if not objs:
            return
        kwargs = {}
        fields = self.registry.get(objs[0].__class__, [])
        if fields:
            kwargs.update({
                'fields': fields
            })
        return self.serializer.serialize(
            objs,
            **kwargs
        )

    @property
    def registry(self):
        if self.m2m and self.model.in_history_m2m_registry:
            from ralph_assets.history import registry_m2m
            return registry_m2m
        if not self.m2m and self.model.in_history_registry:
            from ralph_assets.history import registry
            return registry

    @property
    def m2m_info(self):
        source_class = self.obj.__class__
        source_obj = self.obj
        source_field_name = source_class._meta.object_name.lower()

        target_field = None
        for target_field in self.sender._meta.fields[1:]:
            if target_field.name != source_class._meta.object_name.lower():
                break
        m2m_class = target_field.model
        target_class = target_field.related.parent_model
        target_obj = target_class.objects.filter(pk__in=self.pk_set)
        target_field_name = target_field.name
        return locals()

    def m2m_pre_save(self):
        # print(self.m2m_info['source_field_name'])
        kwargs = {
            self.m2m_info['source_field_name']: self.obj.pk,
        }
        snapshot = self.get_fields_snapshot(
            self.sender.objects.filter(**kwargs)
        )
        self.past_snapshot = []
        if snapshot:
            self.past_snapshot = [snap['fields'] for snap in snapshot]

    def m2m_post_save(self):
        kwargs = {
            self.m2m_info['source_field_name']: self.obj.pk,
        }
        # snapshot = self.get_fields_snapshot(self.sender.objects.filter(**kwargs))
        # current_snapshot = [snap['fields'] for snap in snapshot]

        # field = self.m2m_info['target_field_name']
        # obj = self.obj
        # old = set([item[field] for item in self.past_snapshot])
        # new = set([item[field] for item in current_snapshot])

        # History.objects.log_changes(obj, self.obj.saving_user, [{
        #     'field': field,
        #     'old': old,
        #     'new': new,
        # }])


        # if not self.reverse:
        #     kwargs = {
        #         '{}__in'.format(self.m2m_info['target_field_name']): self.m2m_info['target_obj'],
        #         # self.m2m_info['source_field_name']: self.m2m_info['source_obj'],
        #     }
        #     snapshot = self.get_fields_snapshot(self.sender.objects.filter(**kwargs))
        #     current_snapshot = [snap['fields'] for snap in snapshot]
        #     # print(self.m2m_info['source_obj'], current_snapshot)  # DETELE THIS
        #     field = self.m2m_info['source_field_name']
        #     old = set([item[field] for item in self.past_snapshot])
        #     new = set([item[field] for item in current_snapshot])
        #     print(old, new)  # DETELE THIS
        #     if old != new:
        #         for obj in self.m2m_info['target_obj']:
        #             History.objects.log_changes(obj, self.obj.saving_user, [{
        #                 'field': field,
        #                 'old': old,
        #                 'new': new,
        #             }])




        # kwargs = {
        #     to_field_name: to_obj,
        #     from_field_name: from_obj,
        # }
        # m2m_objs = m2m_class.objects.filter(**kwargs)
        # print('m2m', [(m.asset.pk, m.licence.pk) for m in m2m_objs])  # DETELE THIS


        # print(self.sender._default_manager.all())
        # dest_field = None
        # for dest_field in self.sender._meta.fields[1:]:
        #     if dest_field.name != affected_field:
        #         break

        # print(self.obj, self.sender, self.pk_set)  # DETELE THIS
        # History.objects.log_changes(self.obj, self.obj.saving_user, [{
        #     'field': dest_field.name,
        #     'old': str(self.obj),
        #     'new': dest_field.parent_model._default_manager.get,
        # }])


        # affected_field = self.obj.__class__._meta.object_name.lower()
        # print(affected_field)  # DETELE THIS
        # print(self.obj.pk)
        # for diff in diff_data:
        #     added = set(diff['new']).difference(diff['old'])
        #     for pk in added:
        #         model = getattr(self.obj, diff['field']).model
        #         obj = model._default_manager.get(pk=pk)
        #         related_name = self.model._meta.get_field_by_name(
        #             diff['field']
        #         )[0].related_query_name()
        #         all_related = (
        #             getattr(obj, related_name + '_set', None)
        #             or getattr(obj, related_name)
        #         ).all
        #         History.objects.log_changes(obj, self.obj.saving_user, [{
        #             'field': affected_field,
        #             'old': str(self.obj),
        #             'new': ', '.join([str(o) for o in all_related()]),
        #         }])
        #         # add licence to asset history
        #         History.objects.log_changes(self.obj, self.obj.saving_user, [{
        #             'field': affected_field,
        #             'old': str(self.obj),
        #             'new': ', '.join([str(o) for o in all_related()]),
        #         }])

    def pre_save(self):
        self.pre_obj = None
        try:
            self.pre_obj = self.model._default_manager.get(pk=self.obj.pk)
        except self.model.DoesNotExist:
            return
        self.past_snapshot = self.get_fields_snapshot(
            [self.pre_obj]
        )[0]['fields']

    def post_save(self):
        if not self.pre_obj:
            return
        current_snapshot = self.get_fields_snapshot([self.obj])[0]['fields']

        # print(current_snapshot, self.past_snapshot)
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

        # if self.m2m and self.model.in_history_m2m_symetric:
            # field = None
            # for field in self.sender._meta.fields[1:]:
            #     if field.related.parent_model == self.obj.__class__:
            #         break

            # print(field)  # DETELE THIS
            # print(self.obj)  # DETELE THIS
            # for field in self.sender._meta.fields[1:]:
            #     print(field.related.parent_model)
            #     History.objects.log_changes(self.obj, self.obj.saving_user, [{
            #         'field': 'affected_field',
            #         'old': str(self.obj),
            #         'new': 'dups'
            #     }])


            # print(self.sender._meta.fields[1:])
            # print(self.obj._meta.get_all_related_objects())  # DETELE THIS
            # print([rel.get_accessor_name() for rel in self.obj._meta.get_all_related_objects()])

    def start(self, sender, obj, m2m=False, pk_set=set(), reverse=False):
        self.m2m = m2m
        self.obj = obj
        self.reverse = reverse
        self.model = self.obj.__class__
        self.pk_set = pk_set
        self.sender = sender
        if m2m:
            self.m2m_pre_save()
        else:
            self.pre_save()

    def end(self):
        if self.m2m:
            self.m2m_post_save()
        else:
            self.post_save()
        self.m2m = False
        self.obj = None
        self.sender = None
        self.reverse = False

context = HistoryContext()
