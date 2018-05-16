# -*- coding: utf-8 -*-
from collections import Counter
from zapret_ip import clean_data_line, DELIMITER_CSV, processing_line, processing_data

__author__ = 'pachkun'


def test_clean_data_line():
    line = '52.237.222.222;http://52.237.222.222;'
    assert clean_data_line('') is None
    assert clean_data_line('   ') is None
    assert clean_data_line(line) == line
    assert clean_data_line(DELIMITER_CSV + line) is None


def test_processing_line():
    line = '104.18.104.21 | 104.18.105.21 | 104.18.105.21 | 104.18.108.21;letmew1n.com;;суд;2-927/2013;2013-12-10'
    assert processing_line(line) == Counter({'104.18.104.21': 1, '104.18.105.21': 2, '104.18.108.21': 1})


def test_processing_data():
    data = """
    104.16.214.246 | 104.18.106.21;letmeberich.com;http://letmeberich.com/?s=35;ФНС;2-6-20/2017-03-03-182-АИ;2017-03-06\n
    104.18.104.21 | 104.18.105.21 | 104.18.106.21 | 104.18.108.21;letmew1n.com;;суд;2-927/2013;2013-12-10\n
    """
    assert processing_data(data) == Counter(
        {'104.18.104.21': 1, '104.18.106.21': 2, '104.18.108.21': 1, '104.16.214.246': 1, '104.18.105.21': 1})
