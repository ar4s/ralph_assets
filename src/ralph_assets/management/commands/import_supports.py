# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import csv
import datetime
import os

from optparse import make_option
from dateutil.relativedelta import relativedelta

from bob.csvutil import UTF8Recoder
from django.core.management.base import BaseCommand, CommandError

from ralph_assets.models_assets import (
    MODE2ASSET_TYPE,
    Asset,
    AssetOwner,
    AssetType,
)
from ralph_assets.models_support import Support


class UnicodeDictReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding='utf-8', **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)
        self.header = [x.lower() for x in self.reader.next()]

    def next(self):
        row = self.reader.next()
        vals = [unicode(s, 'utf-8') for s in row]
        return dict((self.header[x], vals[x]) for x in range(len(self.header)))

    def __iter__(self):
        return self

from ralph_assets import models_support
from django import forms


class AddForm(forms.ModelForm):
    class Meta:
        model = models_support.Support
        fields = (
            'contract_id',
            'name',
            'date_from',
            'date_to',
            'asset_type',
            'assets',
            'invoice_no',
            'invoice_date',
            'additional_notes',
            'producer',
            'supplier',
            'description',
            'serial_no',
            'contract_terms',
            'escalation_path',
            'property_of',
        )


class Command(BaseCommand):
    """Import supports."""
    option_list = BaseCommand.option_list + (
        make_option(
            '-f',
            '--filename',
            action='store',
            dest='filename',
        ),
        make_option(
            '-t',
            '--type',
            type='choice',
            dest='support_type',
            choices=MODE2ASSET_TYPE.keys(),
            help='Support type',
        ),
    )

    def handle(self, *args, **options):
        filename = options['filename']
        support_type = options['support_type']
        if not filename or not os.path.isfile(filename):
            raise CommandError('File doesn\'t exist.')

        with open(filename, 'rb') as csv_file:
            reader = UnicodeDictReader(csv_file)
            for row in reader:
                asset_type = AssetType.id_from_name(support_type)
                support, _ = Support.objects.get_or_create(
                    contract_id=row['contract_id'],
                    name=row['name'],
                    date_to=row['date_to'],
                    asset_type=asset_type,
                )
                assets = list(
                    support.assets.all().values_list('id', flat=True)
                )
                assets.extend(
                    list(
                        Asset.objects.filter(
                            sn=row['asset_sn']
                        ).values_list('id', flat=True)
                    )
                )
                date_from_calculate = datetime.datetime.strptime(
                    row.get('date_to'), '%Y-%m-%d'
                ) - relativedelta(months=int(row.get('months')))
                date_from = row.get('date_from') or date_from_calculate
                property_of = AssetOwner.objects.filter(
                    name=row['property_of']
                )[:1]
                row.update({
                    'asset_type': asset_type,
                    'assets': assets,
                    'date_from': date_from,
                    'property_of': property_of[0].id if property_of else None
                })
                f = AddForm(row, instance=support)
                f.is_valid()
                support = f.save(commit=False)
                f.save_m2m()
                support.save()
                print('{} -> Asset {}'.format(support, row['asset_sn']))
