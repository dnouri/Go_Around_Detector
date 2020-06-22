import os
import shutil
import sys

from click.testing import CliRunner
import pytest

sys.path.insert(0, '.')


@pytest.fixture
def data_dir():
    return os.path.join(os.path.dirname(__file__), 'data')


@pytest.fixture
def data_dir_copy(data_dir, tmpdir):
    dest = str(tmpdir) + '/' + os.path.basename(data_dir)
    shutil.copytree(data_dir, dest)
    return dest


class TestMain:
    @pytest.fixture
    def vabb(self, data_dir_copy):
        from GA_Detect import main
        runner = CliRunner()
        result = runner.invoke(main, [
            '--top-dir', data_dir_copy + '/',
            '--metars-file', os.path.join(data_dir_copy, 'VABB_METAR'),
            '--pool-proc', '1',
            ])
        assert result.exit_code == 0
        return result

    def test_csv(self, vabb, data_dir, data_dir_copy):
        for fname in ['GA_MET_NEW.csv', 'GA_NOGA_NEW.csv']:
            with open(os.path.join(data_dir, 'expected', fname)) as f:
                csv_expected = f.read()
            with open(os.path.join(data_dir_copy, fname)) as f:
                csv_got = f.read()
            assert csv_expected == csv_got
