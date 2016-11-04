from xlrd import open_workbook
import sys
import db
from db import Participant
database = db.database
database.connect()
reload(sys)
sys.setdefaultencoding('utf-8')

class Part(object):
    def __init__(self, timestamp, fname, lname, email, school, grad, major, random, link1, link2, link3, teach, location, random2, diet, dis, welcom, cut, blank):
        self.fname = fname
        self.lname = lname
        self.email = email

    def __str__(self):
        return("Part object:\n"
               "  fname = {0}\n"
               "  lname = {1}\n"
               "  email = {2}\n"
               .format(self.fname, self.lname, self.email))

wb = open_workbook('HackATLAcceptances.xlsx')
for sheet in wb.sheets():
    number_of_rows = sheet.nrows
    number_of_columns = sheet.ncols

    items = []

    rows = []
    for row in range(1, number_of_rows):
        values = []
        for col in range(number_of_columns):
            value  = (sheet.cell(row,col).value)
            try:
                value = str(int(value))
            except ValueError:
                pass
            finally:
                values.append(value)
        item = Part(*values)
        items.append(item)

for item in items:
    print item
    Participant.create(email= item.email, first_name=item.fname, last_name=item.lname)
    print("Accessing one single value (eg. name): {0}".format(item.fname))
    print

database.close()
