import json
from json import load
from os.path import join as pjoin

def extractor(filename):
    with open(filename, 'r') as f:
        load_dict = json.load(f)
        num_news = len(load_dict)
        print(num_news) 


extractor('./crawler_urls/BBC News_test.json')
extractor('./crawler_extracted/BBC News_test.json')

extractor('./crawler_urls/Reuters_test.json')
extractor('./crawler_extracted/Reuters_test.json')