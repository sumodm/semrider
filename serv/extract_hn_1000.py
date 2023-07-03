import csv
import sys

def lazy_csv_reader(csvfile):
  with open(csvfile) as f:
    r = csv.reader(f)
    next(r, None) # Skip the header row
    for row in r:
      yield row

csvfile = sys.argv[1]
for row in lazy_csv_reader(csvfile):
  if row[5] != '' and int(row[5])>100 and row[1] != '':
    print("\"",row[1],"\",",row[5])

lazy_csv_reader(sys.argv[1])

# To run, do python serv/extract_hn_100.py serv/data/hn_url_gt_100.csv
