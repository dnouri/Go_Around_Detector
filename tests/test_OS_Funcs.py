import os

import pandas
import pytest
from traffic.core import Flight


@pytest.fixture
def data_dir():
    return os.path.join(os.path.dirname(__file__), 'data')


class TestProfFl:
    @pytest.fixture
    def proc_fl(self):
        from OS_Funcs import proc_fl
        return proc_fl

    def test_KQA204(self, proc_fl, data_dir, tmpdir):
        from metar_parse import get_metars
        from OS_Airports.RWY import retrieve_runway_list

        odirs = [
            os.path.join(tmpdir, 'NORM-plot') + '/',
            os.path.join(tmpdir, 'PSGA-plot') + '/',
            os.path.join(tmpdir, 'NORM-data') + '/',
            os.path.join(tmpdir, 'PSGA-data') + '/',
            ]
        for odir in odirs:
            os.makedirs(odir)

        result = proc_fl(
            flight=Flight(
                pandas.read_csv(os.path.join(data_dir, 'KQA204.csv'),
                                parse_dates=['timestamp'])),
            metars=get_metars(os.path.join(data_dir, 'VABB_METAR'), False),
            check_rwys=retrieve_runway_list('VABB'),
            odirs=odirs,
            colormap={},
            do_save=False,
            verbose=False,
            )

        assert result[:-1] == [
            True,
            '04c147',
            'KQA204',
            pandas.Timestamp('2019-08-10 00:21:24+0000', tz='UTC'),
            pandas.Timestamp('2019-08-10 00:19:25+0000', tz='UTC'),
            '27',
            -96.00900595749448,
            1347.6201812316162,
            19.08824157714844,
            72.8559820992606,
            370,
            1.3554425701202464,
            0.0027863795136474465,
            3.5391823044835526e-06,
            0.00021195186832100995,
            0.03189928263824995,
            ]
