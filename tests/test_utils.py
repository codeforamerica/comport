# -*- coding: utf-8 -*-
from comport.utils import parse_date
from datetime import datetime

class TestUtils:

    def test_parse_date(self):
        ''' Well formatted date is parsed, other inputs return None
        '''
        # well formatted date is parsed
        assert parse_date("2015-10-17 00:00:00") == datetime(2015, 10, 17, 0, 0)
        # other inputs return None
        assert parse_date(None) is None
        assert parse_date("None") is None
        assert parse_date("2015-10-17 00:00") is None
        assert parse_date(123.22) is None
        assert parse_date(datetime(2015, 10, 17, 0, 0)) is None
