# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.forms.models import formset_factory
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect

from ralph_assets import models as assets_models
from ralph_assets.forms import AttachmentForm
from ralph_assets.models_attachments import Attachment
from ralph_assets.views.base import AssetsBase, get_return_link


logger = logging.getLogger(__name__)


class AttachmentMixin(object):
    def dispatch(self, request, *args, **kwargs):
        self.Parent = ContentType.objects.get_for_id(
            kwargs['content_type_id']).model_class()
        self.parent = self.Parent.objects.get(pk=kwargs['object_id'])
        self.attachment = None
        if 'attachment_id' in kwargs:
            self.attachment = Attachment.object.get(id=attachment_id)
        return super(AttachmentMixin, self).dispatch(
            request, *args, **kwargs
        )


class AddAttachment(AttachmentMixin, AssetsBase):
    """
    Adding attachments to object - yep, object - no concrete model.
    """
    template_name = 'assets/add_attachment.html'
    mainmenu_selected = 'asset'

    def get_context_data(self, **kwargs):
        context = super(AddAttachment, self).get_context_data(**kwargs)
        context.update({
            'selected_parents': [self.parent],
        })
        return context

    def get(self, *args, **kwargs):
        AttachmentFormset = formset_factory(
            form=AttachmentForm, extra=1,
        )
        kwargs['formset'] = AttachmentFormset()
        return super(AddAttachment, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        AttachmentFormset = formset_factory(
            form=AttachmentForm, extra=0,
        )
        attachments_formset = AttachmentFormset(
            self.request.POST, self.request.FILES,
        )
        kwargs['formset'] = attachments_formset
        if attachments_formset.is_valid():
            for form in attachments_formset.forms:
                attachment = form.save(commit=False)
                attachment.uploaded_by = self.request.user
                attachment.content_type_id = self.kwargs['content_type_id']
                attachment.object_id = self.kwargs['object_id']
                attachment.save()
            messages.success(self.request, _('Changes saved.'))
            return HttpResponseRedirect('../../../../')  # TODO: change this
        messages.error(self.request, _('Please correct the errors.'))
        return super(AddAttachment, self).get(*args, **kwargs)


class DeleteAttachment(AttachmentMixin, AssetsBase):

    def post(self, *args, **kwargs):
        parent_id = self.request.POST.get('parent_id')
        back_url = self.parent.get_absolute_url()
        attachment_id = self.request.POST.get('attachment_id')
        try:
            attachment = Attachment.objects.get(id=attachment_id)
        except Attachment.DoesNotExist:
            messages.error(
                self.request, _('Selected attachment doesn\'t exists.')
            )
            return HttpResponseRedirect(back_url)
        try:
            self.parent = self.Parent.objects.get(pk=parent_id)
        except self.Parent.DoesNotExist:
            messages.error(
                self.request,
                _('Selected {} doesn\'t exists.').format(self.parent_name),
            )
            return HttpResponseRedirect(back_url)
        delete_type = self.request.POST.get('delete_type')
        if delete_type == 'from_one':
            if attachment in self.parent.attachments.all():
                self.parent.attachments.remove(attachment)
                self.parent.save()
                msg = _('Attachment was deleted')
            else:
                msg = _(
                    '{} does not include the attachment any more'.format(
                        self.parent_name.title()
                    )
                )
            messages.success(self.request, _(msg))

        elif delete_type == 'from_all':
            Attachment.objects.filter(pk=attachment.id).delete()
            messages.success(self.request, _('Attachments was deleted'))
        else:
            msg = 'Unknown delete type: {}'.format(delete_type)
            messages.error(self.request, _(msg))
        return HttpResponseRedirect(back_url)
