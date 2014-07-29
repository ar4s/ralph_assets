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


def get_form(with_assets=True):
    class AddForm(forms.ModelForm):
        class Meta:
            model = models_support.Support
            fields = [
                'contract_id',
                'name',
                'date_from',
                'date_to',
                'asset_type',
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
            ]

    class AddFormWithAssets(AddForm):
        class Meta(AddForm.Meta):
            fields = AddForm.Meta.fields + [
                'assets',
            ]

    return AddFormWithAssets if with_assets else AddForm


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
            help='Support type ({})'.format(', '.join(MODE2ASSET_TYPE.keys())),
        ),
    )

    def handle(self, *args, **options):
        filename = options['filename']
        support_type = options['support_type']
        if not filename or not os.path.isfile(filename):
            raise CommandError('File doesn\'t exist.')

        messages = []

        with open(filename, 'rb') as csv_file:
            reader = UnicodeDictReader(csv_file)
            for row in reader:
                print('Add', row['name'], 'to', row['asset_sn'])
                message = {}
                asset_type = MODE2ASSET_TYPE[support_type].id
                support, created = Support.objects.get_or_create(
                    contract_id=row['contract_id'],
                    name=row['name'],
                    date_to=row['date_to'],
                    asset_type=asset_type,
                )
                message['support_created'] = created
                message['support'] = row['name']
                message['support_contract_id'] = row['contract_id']
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
                message['asset'] = row['asset_sn']
                message['asset_exist'] = Asset.objects.filter(
                    sn=row['asset_sn']
                ).count()
                message['assets_len'] = len(assets)

                date_from_calculate = datetime.datetime.strptime(
                    row.get('date_to'), '%Y-%m-%d'
                ) - relativedelta(months=int(row.get('months')))
                date_from = row.get('date_from') or date_from_calculate
                property_of = AssetOwner.objects.filter(
                    name=row.get('property_of')
                )[:1]
                row.update({
                    'asset_type': asset_type,
                    'assets': assets,
                    'date_from': date_from,
                    'property_of': property_of[0].id if property_of else None
                })
                Form = get_form(len(assets) != 0)
                f = Form(row, instance=support)
                if f.is_valid():
                    support = f.save(commit=False)
                    f.save_m2m()
                    support.save()
                    message['status'] = 'Zapisany'
                else:
                    message['status'] = ' | '.join(['{}: {}'.format(er[0], ';'.join([e for e in er[1]])) for er in f.errors.items()])

                messages.append(message)

            print('Generating report..')
            with open('import_results.csv'.format(filename), 'wb') as f:
                w = csv.DictWriter(f, messages[0].keys())
                w.writeheader()
                for message in messages:
                    w.writerow(message)
