# -*- coding: utf-8 -*-
from django.utils import simplejson
from django.utils.datastructures import SortedDict

__author__ = 'M.Y'


class Cell(object):
    def __init__(self, name, value, width, aggregation):
        self.value = value
        self.width = width
        self.name = name
        self.aggregation = aggregation


class Row(object):
    def __init__(self):
        self.cells = []

    def add_cell(self, cell):
        self.cells.append(cell)

    def create_cell(self, name, value, width, aggregation):
        self.add_cell(Cell(name, value, width, aggregation))

    def get_cells_dict(self):
        cells_dict = SortedDict()
        for cell in self.cells:
            cells_dict[cell.name] = cell.value
        return cells_dict

    def __iter__(self):
        return iter(self.cells)


class Header(object):
    def __init__(self):
        self.cells = []
        self.sums = []

    def add_cell(self, cell):
        self.cells.append(cell)

    def create_cell(self, name, value, width, aggregation):
        self.add_cell(Cell(name, value, width, aggregation))
        self.sums.append(0)

    def aggregate(self, row):
        i = 0
        for cell in row:
            if cell.aggregation:
                self.sums[i] += int(cell.value)
            i += 1

    def __iter__(self):
        return iter(self.cells)


class Table(object):
    def __init__(self):
        self.header = None
        self.rows = []

    def set_header(self, header):
        self.header = header

    def add_row(self, row):
        self.rows.append(row)
        self.header.aggregate(row)

    def get_dgrid_json(self, total_page, current_page, all_data_count, aggregation=False):
        json_dict = SortedDict({
            "total": total_page,
            "page": current_page,
            "records": all_data_count,
        })
        json_rows = []
        for row in self.rows:
            json_rows.append(row.get_cells_dict())
        json_dict['rows'] = json_rows

        footer_row = {}
        i = 0
        for cell in self.header:
            footer_row[cell.name] = self.header.sums[i]
            i += 1
        footer_row.update({self.header.cells[1].name: u"مجموع:"})

        if aggregation:
            json_dict["userdata"] = footer_row

        json = simplejson.dumps(json_dict)

        return json

    def __iter__(self):
        return iter(self.rows)
