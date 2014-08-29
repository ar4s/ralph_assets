# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.db.models import signals
from django.db.models.fields import FieldDoesNotExist
from django.db.models.fields.related import RelatedField

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
    return getattr(instance, 'get_{}_display'.format(field))()
