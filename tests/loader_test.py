from nose.tools import *
from pycsv.exceptions import PyCsvExcept, PyCsvInvalidType, PyCsvInvalidCast, PyCsvInvalidColumn, \
    PyCsvOutBound, PyCsvInvalidFile, PyCsvRequiredHeader, PyCsvInvalidOrder
from pycsv.loader import Loader


@raises(PyCsvExcept)
def test_path_not_exist():
    Loader("aaa")

def test_empty_file():
    loader = Loader("tests/fixtures")
    loader.fill_file("empty_file.txt")
    eq_(loader.cols_count, 0)
    eq_(loader.rows_count, 0)

def test_file_with_only_header():
    loader = Loader("tests/fixtures")
    loader.fill_file("file_with_only_header.txt")
    eq_(loader.cols_count, 2)
    eq_(loader.rows_count, 0)

def test_sort_dates():
    loader = Loader("tests/fixtures")
    loader.fill_file("sort_dates.txt")
    eq_(loader.cols_count, 2)
    eq_(loader.rows_count, 3)
    loader.sort_by([{"column": "column2", "type": "datetime", "format": "%Y%m%d"}])
    eq_(loader.get_value(0, 1), "20150310")
    eq_(loader.get_value(1, 1), "20150320")
    eq_(loader.get_value(2, 1), "20150330")

def test_sort_with_2_columns():
    loader = Loader("tests/fixtures")
    loader.fill_file("sort_with_2_columns.txt")
    eq_(loader.cols_count, 3)
    eq_(loader.rows_count, 9)
    loader.sort_by([{"column": "column1", "type": "string"},
                    {"column": "column3", "type": "datetime", "format": "%H:%M"}])

    eq_(loader.get_value(0, 0), 'c0')
    eq_(loader.get_value(1, 0), 'c0')
    eq_(loader.get_value(2, 0), 'c0')
    eq_(loader.get_value(3, 0), 'c0')
    eq_(loader.get_value(4, 0), 'c0')
    eq_(loader.get_value(5, 0), 'c0')
    eq_(loader.get_value(6, 0), 'c1')
    eq_(loader.get_value(7, 0), 'c1')
    eq_(loader.get_value(8, 0), 'c1')

    eq_(loader.get_value(0, 2), '10:15')
    eq_(loader.get_value(1, 2), '11:00')
    eq_(loader.get_value(2, 2), '11:15')
    eq_(loader.get_value(3, 2), '11:40')
    eq_(loader.get_value(4, 2), '11:50')
    eq_(loader.get_value(5, 2), '12:00')
    eq_(loader.get_value(6, 2), '10:20')
    eq_(loader.get_value(7, 2), '10:50')
    eq_(loader.get_value(8, 2), '16:40')

@raises(PyCsvInvalidType)
def test_sort_dates_without_format():
    loader = Loader("tests/fixtures")
    loader.fill_file("sort_dates.txt")
    eq_(loader.cols_count, 2)
    eq_(loader.rows_count, 3)
    loader.sort_by([{"column": "column2", "type": "datetime"}])

@raises(PyCsvInvalidType)
def test_sort_with_type_invalid():
    loader = Loader("tests/fixtures")
    loader.fill_file("sort_dates.txt")
    eq_(loader.cols_count, 2)
    eq_(loader.rows_count, 3)
    loader.sort_by([{"column": "column2", "type": "aa"}])

@raises(PyCsvInvalidCast)
def test_sort_dates_invalid_format():
    loader = Loader("tests/fixtures")
    loader.fill_file("sort_dates.txt")
    eq_(loader.cols_count, 2)
    eq_(loader.rows_count, 3)
    loader.sort_by([{"column": "column2", "type": "datetime", "format": "%A%m%d"}])

@raises(PyCsvInvalidCast)
def test_sort_integer_invalid():
    loader = Loader("tests/fixtures")
    loader.fill_file("sort_with_2_columns.txt")
    loader.sort_by([{"column": "column1", "type": "integer"}])

@raises(PyCsvInvalidColumn)
def test_sort_column_invalid():
    loader = Loader("tests/fixtures")
    loader.fill_file("sort_with_2_columns.txt")
    loader.sort_by([{"column": "column10", "type": "integer"}])

@raises(PyCsvInvalidOrder)
def test_sort_column_order_invalid():
    loader = Loader("tests/fixtures")
    loader.fill_file("sort_with_2_columns.txt")
    loader.sort_by([{"column": "column1", "type": "integer", "order": "bobo"}])


@raises(PyCsvOutBound)
def test_sort_column_out_invalid():
    loader = Loader("tests/fixtures")
    loader.fill_file("sort_with_2_columns.txt")
    loader.get_value(10, 0)

@raises(PyCsvOutBound)
def test_sort_row_out_invalid():
    loader = Loader("tests/fixtures")
    loader.fill_file("sort_with_2_columns.txt")
    loader.get_value(0, 10)

@raises(PyCsvInvalidFile)
def test_sort_file_invalid():
    loader = Loader("tests/fixtures")
    loader.fill_file("invalid_file.txt")

@raises(PyCsvRequiredHeader)
def test_sort_file_invalid():
    loader = Loader("tests/fixtures")
    loader.fill_file("invalid_file.txt", ["aa", "cc"])


def test_sort_separator_in_string():
    loader = Loader("tests/fixtures")
    loader.fill_file("separator_in_string.txt")
    eq_(loader.get_value(0, 0),"aa,bb")


def test_file_without_headers():
    loader = Loader("tests/fixtures", False, ";")
    loader.fill_file("file_without_headers.txt")
    eq_(loader.cols_count, 2)
    eq_(loader.rows_count, 4)
    loader.sort_by([{"index": 0, "type": "integer"}])
    eq_(loader.get_value(0, 0),"0")
    eq_(loader.get_value(1, 0),"1")
    eq_(loader.get_value(2, 0),"2")
    eq_(loader.get_value(3, 0),"3")

@raises(PyCsvInvalidColumn)
def test_file_without_headers_sort_without_index():
    loader = Loader("tests/fixtures", False, ";")
    loader.fill_file("file_without_headers.txt")
    eq_(loader.cols_count, 2)
    eq_(loader.rows_count, 4)
    loader.sort_by([{"type": "integer"}])

def test_file_float():
    loader = Loader("tests/fixtures")
    loader.fill_file("sort_float.txt")
    eq_(loader.cols_count, 2)
    eq_(loader.rows_count, 4)
    loader.sort_by([{"column": "col1", "type": "float"}])
    eq_(loader.get_value(0, 0),"1.5")
    eq_(loader.get_value(1, 0),"2.3")
    eq_(loader.get_value(2, 0),"10")
    eq_(loader.get_value(3, 0),"20")


def test_sort_columns_desc():
    loader = Loader("tests/fixtures")
    loader.fill_file("sort_with_2_columns.txt")
    loader.sort_by([{"column": "column1", "type": "string"},
            {"column": "column3", "type": "datetime", "format": "%H:%M", "order": "desc"}])

    eq_(loader.get_value(0, 0), "c0")
    eq_(loader.get_value(1, 0), "c0")
    eq_(loader.get_value(2, 0), "c0")
    eq_(loader.get_value(3, 0), "c0")
    eq_(loader.get_value(4, 0), "c0")
    eq_(loader.get_value(5, 0), "c0")
    eq_(loader.get_value(6, 0), "c1")
    eq_(loader.get_value(7, 0), "c1")
    eq_(loader.get_value(8, 0), "c1")

    eq_(loader.get_value(0, 2), "12:00")
    eq_(loader.get_value(1, 2), "11:50")
    eq_(loader.get_value(2, 2), "11:40")
    eq_(loader.get_value(3, 2), "11:15")
    eq_(loader.get_value(4, 2), "11:00")
    eq_(loader.get_value(5, 2), "10:15")
    eq_(loader.get_value(6, 2), "16:40")
    eq_(loader.get_value(7, 2), "10:50")
    eq_(loader.get_value(8, 2), "10:20")

