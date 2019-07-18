# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

base = 'https://www.realclearpolitics.com'


def get_polls(q=None, p=None):
    response = urlopen('%s/epolls/latest_polls/' % base)

    soup = BeautifulSoup(response, 'html.parser')

    fp = soup.find_all("table", {"class": 'sortable'})

    polling_data = []

    for l in fp:
        cols = l.find_all('tr')
        for col in cols:
            race = col.find('td', {'class': 'lp-race'})

            if not race:
                continue

            t = race.find('a').text
            n = col.find('td', {'class': 'lp-poll'}).find('a').text

            if (q is not None and q.lower() not in t.lower()) or (p is not None and p.lower() not in n.lower()):
                continue

            v = {
                'url': base + race.find('a')['href'],
                'title': t,
                'poll': n,

            }
            polling_data.append(v)

    return polling_data


def get_poll_data(pd, json=False):
    response = urlopen(pd)

    if base not in pd:
        return

    soup = BeautifulSoup(response, 'html.parser')
    fp = soup.find("div", {"id": 'polling-data-full'})

    if not fp:
        return

    rows = fp.find('table', {"class": 'data'})

    p = []

    for row in rows:
        cols = row.find_all(['th', 'td'])
        p.append([ele.text.strip() for ele in cols])

    if not json:
        return p

    arr = [{
        'poll': pd,
        'data': []
    }]

    keys = p[0]

    for k in p[1:]:
        b = {}
        for i, n in enumerate(keys):
            b[n] = k[i]
        arr[0]['data'].append(b)

    return arr
