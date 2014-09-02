# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ralph_assets.history.models import History
from ralph_assets.views.base import AssetsBase, ContentTypeMixin, PaginateMixin
from ralph_assets.models_assets import ASSET_TYPE2MODE


class HistoryBase(AssetsBase):
    mainmenu_selected = 'unknown'
    sidebar_selected = None

    def get_section(self):
        if str(self.content_type) == 'asset':
            return ASSET_TYPE2MODE[self.content_type.get_object_for_this_type(
                id=self.object_id
            ).type]
        mapper = {
            'licence': 'licences',
            'support': 'supports',
        }
        return mapper[str(self.content_type)]

    def get_context_data(self, **kwargs):
        context = super(HistoryBase, self).get_context_data(**kwargs)
        context.update({
            'section': self.get_section(),
        })
        return context


class HistoryListForModel(PaginateMixin, ContentTypeMixin, HistoryBase):
    """View for history of object."""
    template_name = 'assets/history/history_for_model.html'

    def get_paginate_queryset(self):
        return History.objects.get_history_for_this_content_type(
            content_type=self.content_type,
            object_id=self.object_id,
        )

    def get_context_data(self, **kwargs):
        context = super(HistoryListForModel, self).get_context_data(**kwargs)
        context.update({
            'history': History.objects.get_history_for_this_content_type(
                content_type=self.content_type,
                object_id=self.object_id,
            ),
        })
        return context
