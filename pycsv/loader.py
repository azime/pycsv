# coding=utf-8

from exceptions import PyCsvExcept, PyCsvRequiredHeader, PyCsvInvalidColumn, \
    PyCsvInvalidCast, PyCsvInvalidType, PyCsvOutBound, PyCsvInvalidFile
import os
import csv
from datetime import datetime


class Loader(object):
    def __init__(self, path, with_header=True, separator=','):
        self.path = path
        self.with_header = with_header
        self.separator = separator
        self.data = []
        self.header = []
        self.type_collection = ["integer", "string", "datetime"]
        if not os.path.exists(self.path):
            msg = 'Path not exist, you give {path}'.format(path=self.path)
            raise PyCsvExcept(msg)

    @property
    def rows_count(self):
        return len(self.data)

    @property
    def cols_count(self):
        return len(self.header)

    def __check_headers(self, required_headers):
        if not required_headers:
            return True
        if len(required_headers) == 0:
            return True
        for r_header in required_headers:
            if r_header not in self.header:
                return False

    def __add_index_column(self, columns):
        for column in columns:
            if "type" not in column:
                raise PyCsvInvalidType("Column invalid.")
            if column["type"] not in self.type_collection:
                raise PyCsvInvalidType("Type invalid for sort function. you give :{col}".format(col=column["type"]))
            if column["type"] == "datetime" and "format" not in column:
                raise PyCsvInvalidType("Format date is required. you give :{col}".format(col=column["type"]))
            try:
                column["index"] = self.header.index(column["column"])
            except ValueError:
                raise PyCsvInvalidColumn("Column {column} invalid.".format(column=column["column"]))

    def __sort_func(self, columns):
        def sort_func(item):
            result =[]
            for column in columns:
                if column["type"] == "integer":
                    result.append(self.__to_int(item[column["index"]]))
                if column["type"] == "datetime":
                    result.append(self.__to_date(item[column["index"]], column["format"]))
                if column["type"] == "string":
                    result.append(item[column["index"]])
            return tuple(result)
        return sort_func

    def __to_int(self, value):
        try:
            return int(value)
        except ValueError:
            raise PyCsvInvalidCast("Impossible to convert {v} to integer.".format(v=value))

    def __to_date(self, value, fromat_date):
        try:
            return datetime.strptime(value, fromat_date)
        except ValueError:
            raise PyCsvInvalidCast("Impossible to convert {v} to date.".format(v=value))

    def is_col_row(self, col, row):
        if col > self.cols_count or col < 0:
            return False
        if row > self.rows_count or row < 0:
            return False
        return True

    def get_value(self, col, row):
        '''
        :param col: 0 to self.cols_count
        :param row: 0 to self.cols_count
        :return: value or except PyCsvOutBound
        '''

        if col > self.cols_count or col < 0:
            raise PyCsvOutBound("Invalid column {col}.".format(col=col))
        if row > self.rows_count or row < 0:
            raise PyCsvOutBound("Invalid row {row}.".format(row=row))
        return self.data[row][col]

    def fill_file(self, filename, required_headers=None):
        '''
        fill self.data
        :param filename: file name
        :param required_headers: list of header required
        excepts :
            PyCsvExcept
            PyCsvRequiredHeader
            PyCsvInvalidFile
        '''
        file_name = os.path.join(self.path, filename)
        try:
            csvfile = open(file_name, "r")
        except IOError, e:
            csvfile.close()
            raise PyCsvExcept("Connot open file %s, error : %s." % (file_name, str(e)))
        reader = csv.reader(csvfile, delimiter=self.separator)

        if self.with_header:
            for tmp in reader:
                self.header = [col.strip() for col in tmp]
                if not self.__check_headers(required_headers):
                    csvfile.close()
                    raise PyCsvRequiredHeader('The header required not exist.')
                break

        for row in reader:
            if len(row) > 0:
                if len(row) != len(self.header):
                    csvfile.close()
                    raise PyCsvInvalidFile("Invalid file, invalid cloumns number!")
                self.data.append([r.strip() for r in row])
        csvfile.close()

    def content_by_filename(self, filename):
        if filename in self.data:
            return self.data[filename]
        return None

    def column_count(self, filename):
        content = self.content_by_filename(filename)
        if content:
            return len(content[0])
        return -1

    def row_count(self, filename):
        content = self.content_by_filename(filename)
        if content:
            return len(content)
        return -1

    def sort_by(self, columns):
        '''
        :param column:
            values : [{"column": "column1", "type": "string"}
                    {"column": "column1", "type": "integer"}
                    {"column": "column1", "type": "datetime", "format": "%Y%m%d"}]
        '''
        self.__add_index_column(columns)
        self.data.sort(key=self.__sort_func(columns))
    