import os
import csv
import sys
import requests
from bs4 import BeautifulSoup

def cleanup(embed_file, meta_file, clean = True):
   if clean:
      if os.path.exists(embed_file):
         os.remove(embed_file)
      
      if os.path.exists(meta_file):
         os.remove(meta_file)

def lazy_csv_reader(csvfile):
  with open(csvfile) as f:
    r = csv.reader(f)
    next(r, None) # Skip the header row
    for row in r:
      yield row

def lazy_txt_reader(txtfile, delimiter='|'):
  with open(txtfile) as f:
      for line in f:
          yield line.split("|")


def csv_writer(csvfile, text):
  with open(csvfile, 'a') as file: 
    file.write(text)
    file.close()


def extract_text_from_url(url):
    ''' Extract text from html
        Returns
         status: Boolean
         result: text
    ''' 
    try:
        response = requests.get(url.strip())
        html_content = response.text
        bs_html_parser = BeautifulSoup(html_content, 'html.parser')
        text = bs_html_parser.get_text()
    except:
        return False, "Unable to extract text from url"
    return True, text
