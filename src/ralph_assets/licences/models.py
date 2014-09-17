# -*- coding: utf-8 -*-
"""SAM module models."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Sum
from django.db.models.loading import get_model
from django.utils.functional import cached_property
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _
from lck.django.common.models import (
    Named,
    TimeTrackable,
    WithConcurrentGetOrCreate,
)
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from ralph.discovery.models_util import SavingUser
from ralph.ui.channels import RestrictedLookupChannel
from ralph_assets.models_assets import (
    Asset,
    AssetManufacturer,
    AssetOwner,
    AssetType,
    Attachment,
    AttachmentMixin,
    BudgetInfo,
    CreatableFromString,
    Service,
)
from ralph_assets.models_util import WithForm
from ralph_assets.history.models import History, HistoryMixin


class LicenceType(Named):
    """The type of a licence"""
    class Meta:
        app_label = 'ralph_assets'


class SoftwareCategory(Named, CreatableFromString):
    """The category of the licensed software"""
    asset_type = models.PositiveSmallIntegerField(
        choices=AssetType()
    )

    class Meta:
        app_label = 'ralph_assets'

    @classmethod
    def create_from_string(cls, asset_type, s):
        return cls(asset_type=asset_type, name=s)

    @property
    def licences(self):
        """Iterate over licences."""
        for licence in self.licence_set.all():
            yield licence


class Licence(
    AttachmentMixin,
    HistoryMixin,
    MPTTModel,
    TimeTrackable,
    WithConcurrentGetOrCreate,
    WithForm,
    SavingUser,
):
    """A set of licences for a single software with a single expiration date"""
    manufacturer = models.ForeignKey(
        AssetManufacturer,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    licence_type = models.ForeignKey(
        LicenceType,
        on_delete=models.PROTECT,
    )
    property_of = models.ForeignKey(
        AssetOwner,
        on_delete=models.PROTECT,
        null=True,
    )
    software_category = models.ForeignKey(
        SoftwareCategory,
        on_delete=models.PROTECT,
    )
    number_bought = models.IntegerField(
        verbose_name=_('Number of purchased items'),
    )
    sn = models.TextField(
        verbose_name=_('SN / Key'),
        null=True,
        blank=True,
    )
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_('Parent licence'),
    )
    niw = models.CharField(
        max_length=200,
        verbose_name=_('Inventory number'),
        null=False,
        unique=True,
        default='N/A',
    )
    invoice_date = models.DateField(
        verbose_name=_('Invoice date'),
        null=True,
        blank=True,
    )
    valid_thru = models.DateField(
        null=True,
        blank=True,
        help_text="Leave blank if this licence is perpetual",
    )
    order_no = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, null=True, blank=True,
    )
    accounting_id = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text=_(
            'Any value to help your accounting department '
            'identify this licence'
        ),
    )
    asset_type = models.PositiveSmallIntegerField(
        choices=AssetType(),
        verbose_name=_('Type'),
    )
    assets = models.ManyToManyField(
        Asset,
        verbose_name=_('Assigned Assets'),
        through='LicenceAsset',
    )
    users = models.ManyToManyField(
        User,
        through='LicenceUser',
    )
    attachments = models.ManyToManyField(Attachment, null=True, blank=True)
    provider = models.CharField(max_length=100, null=True, blank=True)
    invoice_no = models.CharField(
        max_length=128, db_index=True, null=True, blank=True
    )
    remarks = models.CharField(
        verbose_name=_('Additional remarks'),
        max_length=1024,
        null=True,
        blank=True,
        default=None,
    )
    license_details = models.CharField(
        verbose_name=_('License details'),
        max_length=1024,
        blank=True,
        default='',
    )
    service_name = models.ForeignKey(Service, null=True, blank=True)
    budget_info = models.ForeignKey(
        BudgetInfo,
        blank=True,
        default=None,
        null=True,
        on_delete=models.PROTECT,
    )

    _used = None

    class Meta:
        app_label = 'ralph_assets'

    def __unicode__(self):
        return "{} x {} - {}".format(
            self.number_bought,
            self.software_category.name,
            self.invoice_date,
        )

    @property
    def url(self):
        return reverse('edit_licence', kwargs={
            'licence_id': self.id,
        })

    @cached_property
    def used(self):
        assets_qs = self.assets.through.objects
        users_qs = self.users.through.objects

        def get_sum(qs):
            return qs.aggregate(sum=Sum('quantity'))['sum'] or 0
        return sum(map(get_sum, [assets_qs, users_qs]))

    @cached_property
    def free(self):
        return self.number_bought - self.used

    def get_model_from_obj(self, obj):
        name = obj._meta.object_name
        allowed_models = ('Asset', 'User')
        if name not in allowed_models:
            raise Exception('{} model is not allowed.'.format(name))
        Model = get_model(
            app_label='ralph_assets',
            model_name='Licence{}'.format(name)
        )
        return Model, name

    def assign(self, obj, quantity=1):
        if quantity <= 0:
            raise ValueError('Variable quantity must be greater than zero.')
        Model, name = self.get_model_from_obj(obj)
        kwargs = {
            name.lower(): obj,
            'licence': self,
        }
        assigned_licence, created = Model.objects.get_or_create(**kwargs)
        assigned_licence.quantity = quantity
        assigned_licence.save(update_fields=['quantity'])
        History.objects.log_changes(
            obj,
            getattr(self, 'saving_user', None),
            [
                {
                    'field': 'assigned_licence_quantity',
                    'old': '-' if created else assigned_licence.quantity,
                    'new': quantity,
                },
            ]
        )

    def detach(self, obj):
        Model, name = self.get_model_from_obj(obj)
        kwargs = {
            name.lower(): obj,
            'licence': self,
        }
        old_value = '-'
        try:
            assigned_licence = Model.objects.get(**kwargs)
            old_value = assigned_licence.quantity
            assigned_licence.delete()
        except Model.DoesNotExist:
            return
        History.objects.log_changes(
            obj,
            getattr(self, 'saving_user', None),
            [
                {
                    'field': 'assigned_licence_quantity',
                    'old': old_value,
                    'new': '-',
                },
            ]
        )


class LicenceAsset(models.Model):
    licence = models.ForeignKey(Licence)
    asset = models.ForeignKey(Asset)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        app_label = 'ralph_assets'
        db_table = 'ralph_assets_licence_assets'
        unique_together = ('licence', 'asset')

    def __unicode__(self):
        return '{} of {} assigned to {}'.format(
            self.quantity, self.licence, self.asset
        )


class LicenceUser(models.Model):
    licence = models.ForeignKey(Licence)
    user = models.ForeignKey(User)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        app_label = 'ralph_assets'
        db_table = 'ralph_assets_licence_users'
        unique_together = ('licence', 'user')

    def __unicode__(self):
        return '{} of {} assigned to {}'.format(
            self.quantity, self.user, self.asset
        )


class BudgetInfoLookup(RestrictedLookupChannel):
    model = BudgetInfo

    class Meta:
        app_label = 'ralph_assets'

    def get_query(self, q, request):
        return BudgetInfo.objects.filter(
            name__icontains=q,
        ).order_by('name')[:10]

    def get_result(self, obj):
        return obj.name

    def format_match(self, obj):
        return self.format_item_display(obj)

    def format_item_display(self, obj):
        return "<span>{name}</span>".format(name=obj.name)


class SoftwareCategoryLookup(RestrictedLookupChannel):
    model = SoftwareCategory

    class Meta:
        app_label = 'ralph_assets'

    def get_query(self, q, request):
        return SoftwareCategory.objects.filter(
            name__icontains=q
        ).order_by('name')[:10]

    def get_result(self, obj):
        return obj.name

    def format_match(self, obj):
        return self.format_item_display(obj)

    def format_item_display(self, obj):
        return escape(obj.name)
