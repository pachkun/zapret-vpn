# -*- coding: utf-8 -*-
import logging
from ipaddress import ip_network
from collections import Counter
from pathlib import Path
from typing import Optional

import requests

__author__ = 'pachkun'

DELIMITER_CSV = ';'
DELIMITER_IP = '|'


def get_zapret_info() -> str:
    logging.info('start request GITHUB_ZAPRET_LIST_INFO')
    result = requests.get(GITHUB_ZAPRET_LIST_INFO)
    logging.info('end request %s', result.status_code)
    if result.status_code != 200:
        raise ConnectionError
    result.encoding = 'cp1251'
    return result.text


def clean_data_line(data_line: str) -> Optional[str]:
    if data_line.strip() == "":
        return None
    # вот такие строки бывают: ;52.237.222.222;http://52.237.222.222; или  ;li153-160.members.linode.com
    if data_line[0] == DELIMITER_CSV:
        return None
    return data_line


def processing_line(line: str) -> Counter:
    ip_line_counter = Counter()
    line = clean_data_line(line)
    if line is None:
        return ip_line_counter
    # первый стоблец в строка это список ip: 104.24.115.87 | 104.31.80.88 | 104.31.81.88;
    for ip in line.split(DELIMITER_CSV)[0].split(DELIMITER_IP):
        ip_line_counter[ip.strip()] += 1
    return ip_line_counter


def processing_data(data: str) -> Counter:
    ip_counter = Counter()
    data_split = data.split('\n')
    logging.info('%s', data_split[0])
    for line in data_split[1:]:
        ip_counter.update(processing_line(line))
    logging.info('ip in list %s', sum([ip_network(ip).num_addresses for ip in ip_counter]))
    logging.info('top 10 ip %s', ip_counter.most_common(10))
    return ip_counter


def route_in_file(ips: Counter):
    logging.info('сохранаю в файл ip')
    with open(ROUTE_ADD_FILE, 'w') as file_add:
        with open(ROUTE_DELETE_FILE, 'w') as file_del:
            for ip in sorted(ips):
                ip = ip_network(ip)
                file_add.write(f'route add {ip.network_address} mask {ip.netmask} {VPN_BRIDGE}\n')
                file_del.write(f'route delete {ip.network_address}\n')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(filename)s %(levelname)s %(message)s')

    GITHUB_ZAPRET_LIST_INFO = 'https://raw.githubusercontent.com/zapret-info/z-i/master/dump.csv'
    ROUTE_ADD_FILE = Path('E:/Temp/trash/route_add.bat')
    ROUTE_DELETE_FILE = Path('E:/Temp/trash/route_delete.bat')
    VPN_BRIDGE = '10.8.1.5'

    zapret_ips = processing_data(get_zapret_info())
    route_in_file(zapret_ips)
