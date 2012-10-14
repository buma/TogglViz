#!/usr/bin/env python2
"""Usage: fill.py FILE...

Arguments:
FILE input file

"""
from docopt import docopt
import csv
try:
    from schema import Schema, Use, SchemaError
except ImportError:
    exit('This example requires that `schema` data-validation library'
         ' is installed: \n pip install schema\n'
         'https://github.com/halst/schema')


def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(unicode_csv_data,
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]


if __name__ == '__main__':
    from togglviz.connectSettings import connectString
    from togglviz.models import DBSession, TimeSlice
    from sqlalchemy import create_engine
    from dateutil.parser import parse
    engine = create_engine(connectString,  echo=True)
    DBSession.configure(bind=engine)
    args = docopt(__doc__)

    schema = Schema({
        'FILE': [Use(open, error='FILE should be readable')],
        })
    try:
        args = schema.validate(args)
    except SchemaError as e:
        exit(e)

    print(args)
    csvreader = unicode_csv_reader(args['FILE'][0])
    header = csvreader.next()
    print header
    # User,Email,Client,Project,"",Description,Billable,Start date,Start time,End date,End time,Duration,Tags
    limit = 0
    for row in csvreader:
        print row
        #client_id = Client.get_client_id(row[1], row[4])
        #project_id = ClientProject.get_client_project_id(row[1], row[4], row[2])
        #print client_id
        #print project_id
        try:
            date = parse(row[7]+" "+row[8], dayfirst=True)
            #print date
            duration = parse(row[11]).time()
            time_slice = TimeSlice(row[2], row[6], row[3], row[5], date, duration)
            DBSession.add(time_slice)
            DBSession.commit()
        except Exception, ex:
            print str(ex)
            DBSession.rollback()
