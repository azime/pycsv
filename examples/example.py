from pycsv.loader import Loader
from pycsv.exceptions import PyCsvExcept, PyCsvInvalidColumn, \
    PyCsvInvalidType, PyCsvInvalidOrder, PyCsvOutBound


if __name__ == "__main__":
    try:
        loader = Loader("../tests/fixtures")
        loader.fill_file("sort_with_2_columns.txt")
        try:
            loader.sort_by([{"column": "column1", "type": "string", "order": "asc"},
                    {"column": "column3", "type": "datetime", "format": "%H:%M", "order": "desc"}])
            val = loader.get_value(2, 0)
        except PyCsvInvalidType, e:
            print e.message
        except PyCsvInvalidColumn, e:
            print e.message
        except PyCsvInvalidOrder, e:
            print e.message
        except PyCsvOutBound, e:
            print e.message
    except PyCsvExcept, e:
        print 'exception !!!: ', e.message

    for row in loader.data:
        print row
'''
Out:
['c0', '5', '12:00']
['c0', '4', '11:50']
['c0', '3', '11:40']
['c0', '2', '11:15']
['c0', '1', '11:00']
['c0', '0', '10:15']
['c1', '2', '16:40']
['c1', '1', '10:50']
['c1', '0', '10:20']
'''
