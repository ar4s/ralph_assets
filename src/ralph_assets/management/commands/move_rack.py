# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from optparse import make_option

from ralph_assets.models_dc_assets import Rack

HORIZONTAL, VERTICAL = 1, 2


class Command(BaseCommand):
    """Export relations report included relations between asset, user and
    licences."""
    option_list = BaseCommand.option_list + (
        make_option(
            '--rack',
            dest='rack_name',
            type='string',
            help='Rack starts with name pattern',
        ),
        make_option(
            '--row',
            dest='row',
            help='row',
        ),
        make_option(
            '--col',
            dest='col',
            help='col',
        ),
        make_option(
            '--orientation',
            dest='orientation',
            help='orientation',
        ),
    )

    def handle(self, *args, **options):
        rack_name = options['rack_name']
        row = int(options['row'])
        col = int(options['col'])
        orientation = int(options['orientation'])
        racks = Rack.objects.filter(name__icontains=rack_name).order_by('name')
        half = racks.count() / 2

        if orientation == HORIZONTAL:
            self.move(racks[:half], col, row, 1, orientation)
            self.move(racks[half:], col, row + 1, 2, orientation)
        else:
            self.move(racks[:half], col, row, 3, orientation)
            self.move(racks[half:], col + 1, row, 4, orientation)

    def move(self, racks, col, row, row_orientation, orientation):
        if orientation == HORIZONTAL:
            for i, rack in enumerate(racks):
                rack.visualization_row = row
                rack.visualization_col = col + i
                rack.orientation = row_orientation
                rack.save()

        if orientation == VERTICAL:
            for i, rack in enumerate(racks):
                rack.visualization_row = row + i
                rack.visualization_col = col
                rack.orientation = row_orientation
                rack.save()
