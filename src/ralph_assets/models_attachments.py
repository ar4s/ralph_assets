# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
from uuid import uuid4

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse

from ralph.discovery.models_util import SavingUser
from lck.django.common.models import TimeTrackable


#TODO: this function is duplicated in models assets!!
def _get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid4(), ext)
    return os.path.join('assets', filename)


class Attachment(SavingUser, TimeTrackable):
    original_filename = models.CharField(max_length=255, unique=False)
    file = models.FileField(upload_to=_get_file_path, blank=False, null=True)
    uploaded_by = models.ForeignKey(User, null=True, blank=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        self.original_filename = self.file.name
        super(Attachment, self).save(*args, **kwargs)


class WithAttachments(models.Model):
    attachments = generic.GenericRelation(Attachment)

    class Meta:
        abstract = True

    @property
    def add_attachment_url(self):
        content_type_id = ContentType.objects.get_for_model(self).pk
        return reverse('add_attachment', kwargs={
            'content_type_id': content_type_id,
            'object_id': self.pk,
       })
