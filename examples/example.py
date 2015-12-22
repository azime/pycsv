from pycsv.loader import Loader
from pycsv.exceptions import PyCsvExcept, \
    PyCsvInvalidColumn, PyCsvInvalidType


if __name__ == "__main__":
    try:
        loader = Loader("../tests/fixtures")
        loader.fill_file("sort_with_2_columns.txt")
        try:
            loader.sort_by([{"column": "column1", "type": "string"},
                    {"column": "column3", "type": "datetime", "format": "%H:%M"}])
        except PyCsvInvalidType, e:
            print str(e.message)
        except PyCsvInvalidColumn, e:
            print str(e.message)
        print loader.get_value(2, 0)
    except PyCsvExcept, e:
        print 'exception !!!: ', str(e)