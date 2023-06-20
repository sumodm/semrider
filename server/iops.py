import csv
import sys

def lazy_csv_reader(csvfile):
  with open(csvfile) as f:
    r = csv.reader(f)
    next(r, None) # Skip the header row
    for row in r:
      yield row
