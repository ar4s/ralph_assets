# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import tempfile
import datetime

from django.core.management import call_command
from django.test import TestCase

from ralph_assets.tests.utils.assets import AssetFactory, AssetOwnerFactory
from ralph_assets.models_support import Support
from ralph_assets.models_assets import Asset


class TestImportSupports(TestCase):
    def test_import_without_parameters(self):
        with self.assertRaises(SystemExit):
            call_command('import_supports', [], {})

    def test_import_one_support_many_assets(self):
        csv_rows = ['"name","contract_id","months","date_to","asset_sn",'
                    '"barcode","property_of","invoice_date","invoice_no",'
                    '"producer","supplier","description","serial_no"']
        csv_row = ('"cisco_12_01","XXYYZZ","12","2012-12-12","{sn}","{barcode}'
                   '","Firma","3/28/2014","123456789","Cisco",'
                   '"Integrated Solutions","description","serial_no"')

        owner = AssetOwnerFactory(name='Firma')
        num_of_assets = 2
        for i in xrange(num_of_assets):
            asset = AssetFactory()
            data = {
                'sn': asset.sn,
                'barcode': asset.barcode,
            }
            csv_rows.append(csv_row.format(**data))
        csv_content = '\n'.join(csv_rows)

        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(csv_content)
            f.close()
            args = []
            kwargs = {
                'filename': f.name,
                'support_type': 'back_office',
            }
            call_command('import_supports', *args, **kwargs)
            self.assertEqual(Support.objects.all().count(), 1)
            support = Support.objects.all()[0]
            self.assertEqual(support.name, 'cisco_12_01')
            self.assertEqual(support.contract_id, 'XXYYZZ')
            self.assertEqual(support.invoice_date, datetime.date(2014, 3, 28))
            self.assertEqual(support.date_from, datetime.date(2011, 12, 12))
            self.assertEqual(support.date_to, datetime.date(2012, 12, 12))
            self.assertEqual(support.invoice_no, '123456789')
            self.assertEqual(support.producer, 'Cisco')
            self.assertEqual(support.supplier, 'Integrated Solutions')
            self.assertEqual(support.description, 'description')
            self.assertEqual(support.serial_no, 'serial_no')
            self.assertEqual(support.property_of, owner)
            self.assertEqual(Asset.objects.all().count(), num_of_assets)
            for asset in Asset.objects.all():
                self.assertIn(support, asset.supports.all())
