import requests
from bs4 import BeautifulSoup
from collections import OrderedDict

URL = 'http://www.stib-mivb.be/horaires-dienstregeling2.html'
WAY = {2: 'V', 1: 'F'}


def get(line, stop, way, date):
    if not way in ('V', 'F'):
        way = WAY[way]

    params = {
        'fmodule': 'l',
        'results': 'r',
        'moduscode': 'T',
        'linecode': line,
        'arretcode': stop,
        'codesens': way,
        'horairedate': date
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:27.0) Gecko/20100101 Firefox/27.0',
    }

    c = requests.get(URL, params=params, headers=headers)
    if 'TIMETABLE NOT AVAILABLE' in c.text or 'HORAIRES NON DISPONIBLES' in c.text:
        raise Exception('Timetable not available')

    soup = BeautifulSoup(c.text)

    table = soup.find(id='horaireTable')
    header = table.find(id='horaireHeader')

    cols_head = header.find_all('span')

    #time_len = len(cols_head)
    # begin_h = int(cols_head[0].text.strip())
    # end_h = int(cols_head[-1].text.strip())
    # Should check if time_len, begin_h and end_h are consistent

    rows = table.find(id='horaireLines').find_all('div')

    time_table = OrderedDict()

    for head in cols_head:
        time = int(head.text.strip())
        time_table[time] = []

    for row in rows:
        cols = row.find_all('span')
        if not cols:
            continue
        for time, slot in zip(time_table.keys(), cols):
            content = slot.text.strip()
            if content:
                time_table[time].append(content)

    return time_table
