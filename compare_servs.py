#!/usr/bin/env python

import argparse
import requests
import yaml
import sys

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta


TAIL_URL_RU = 'http://tail.apisearch-master.local/jset'
TAIL_URL_FIFA = 'http://tail.apisearch-master-fifa.services.local/jset'
TAIL_URL_OTHER_COUNTRIES = 'http://tail.apisearch-master.{}.local/jset'

QUERY_URI_1 = 'http://{}:8080/catalog/admin/luke?wt=json&show=index&numTerms=0'
QUERY_URI_2 = 'http://{}:8080/catalog/select?q=*:*&fq=is_sellable:true&fq={{!frange%20l=1}}qty&wt=json&fl=sku'

COUNTRIES = ['ru', 'fifa', 'ua', 'by', 'kz']

DELTA = timedelta(hours=1)


def is_outdated(time):
    last_modified = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
    now = datetime.utcnow()
    return (now - last_modified) > DELTA


def load_json(url):
    return requests.get(url).json()


def main():
    error = False

    parser = argparse.ArgumentParser(
        description="Comparison prod and pre-prod servers"
    )
    parser.add_argument("country", type=str, help="Country code")
    args = parser.parse_args()

    if args.country == COUNTRIES[0]:
        tail_url = TAIL_URL_RU
    elif args.country == COUNTRIES[1]:
        tail_url = TAIL_URL_FIFA
    elif args.country in COUNTRIES[2:5]:
        tail_url = TAIL_URL_OTHER_COUNTRIES.format(args.country)
    else:
        print('ERROR: Enter valid country {}'.format(COUNTRIES),
              file=sys.stderr)
        exit(1)

    response = yaml.safe_load(requests.get(tail_url).text)

    urls = []
    servers = [serv[0]['host'] for serv in response['groups'].values()]

    for query in [QUERY_URI_1, QUERY_URI_2]:
        for serv in servers:
            urls.append(query.format(serv))

    with ThreadPoolExecutor(max_workers=4) as executor:
        responses = list(executor.map(load_json, urls))

    equal_list_1 = responses[0:2]
    equal_list_2 = responses[2:4]

    for serv, response in zip(servers, equal_list_1):
        if is_outdated(response['index']['lastModified']):
            print('WARNING: {} was modified more than 1 hour ago'.format(serv),
                  file=sys.stderr)
            error = True
        if not response['index']['current']:
            print('WARNING: {} has current=false'.format(serv),
                  file=sys.stderr)
            error = True

    diff = equal_list_1[0]['index']['numDocs'] - equal_list_1[1]['index']['numDocs']
    if diff:
        print('WARNING: Difference in numDocs is {}'.format(abs(diff)),
              file=sys.stderr)
        error = True

    diff = equal_list_2[0]['response']['numFound'] - equal_list_2[1]['response']['numFound']
    if diff:
        print('WARNING: Difference in numFound is {}'.format(abs(diff)),
              file=sys.stderr)
        error = True

    if error:
        exit(1)
    else:
        print('INFO: All good ;)')


if __name__ == '__main__':
    main()
