# -*- coding: utf-8 -*-
from django.utils import simplejson
from django.utils.datastructures import SortedDict

__author__ = 'M.Y'


class Cell(object):
    def __init__(self, name, value, width):
        self.value = value
        self.width = width
        self.name = name


class Row(object):
    def __init__(self):
        self.cells = []

    def add_cell(self, cell):
        self.cells.append(cell)

    def create_cell(self, name, value, width):
        self.cells.append(Cell(name, value, width))

    def get_cells_dict(self):
        cells_dict = SortedDict()
        for cell in self.cells:
            cells_dict[cell.name] = cell.value
        return cells_dict


class Header(object):
    def __init__(self):
        self.cells = []

    def add_cell(self, cell):
        self.cells.append(cell)

    def create_cell(self, name, value, width):
        self.cells.append(Cell(name, value, width))


class Table(object):
    def __init__(self):
        self.header = None
        self.rows = []

    def set_header(self, header):
        self.header = header

    def add_row(self, row):
        self.rows.append(row)

    def get_dgrid_json(self, total_page, current_page, all_data_count):
        json_dict = SortedDict({
            "total": total_page,
            "page": current_page,
            "records": all_data_count,
        })
        json_rows = []
        for row in self.rows:
            json_rows.append(row.get_cells_dict())
        json_dict['rows'] = json_rows

        json = simplejson.dumps(json_dict)

        return json





