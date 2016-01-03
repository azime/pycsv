#Contributor

## Clone project

```
git clone git@github.com:azime/pycsv.git
```

## Create virtual environment

```
virtualenv venv
```

## Activate virtual environment

```
source venv/bin/activate
```

## Testing

```
nosetests test/*
```

# Installation

`
pip install pycsv
`

# Using

`

    from pycsv.loader import Loader
    from pycsv.exceptions import PyCsvExcept, PyCsvInvalidColumn, PyCsvInvalidType
    if __name__ == "__main__":
        columns_to_sort = [
                            {"column": "column1", "type": "string"},
                            {"column": "column3", "type": "datetime", "format": "%H:%M"}
                        ]
        try:
            loader = Loader("../tests/fixtures")
            loader.fill_file("sort_with_2_columns.txt")
            try:
                loader.sort_by(columns_to_sort)
                print loader.get_value(2, 0)
            except PyCsvInvalidType, e:
                print e.message
            except PyCsvInvalidColumn, e:
                print e.message
        except PyCsvExcept, e:
            print 'exception !!!: ', e.message
`

See examples
