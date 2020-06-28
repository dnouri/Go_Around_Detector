import numpy as np
from numpy import (
    arctan2,
    cos,
    pi,
    sin,
    sqrt,
    )
import pytest


def dist(p1, p2):
    R = 6371e3
    φ1 = p1[0] * pi/180
    φ2 = p2[0] * pi/180
    Δφ = (p2[0]-p1[0]) * pi/180
    Δλ = (p2[1]-p1[1]) * pi/180
    a = (sin(Δφ/2) * sin(Δφ/2) +
         cos(φ1) * cos(φ2) *
         sin(Δλ/2) * sin(Δλ/2))
    c = 2 * arctan2(sqrt(a), sqrt(1-a))
    return R * c


class TestRetrieveRunwayList:
    @pytest.fixture
    def retrieve_runway_list(self):
        from OS_Airports.RWY import retrieve_runway_list
        return retrieve_runway_list

    @pytest.mark.parametrize('index', range(4))
    def test_vabb_distances(self, retrieve_runway_list, index):
        from OS_Airports.VABB import rwy_list as expected
        got = retrieve_runway_list('VABB')
        expected = sorted(expected, key=lambda x: x.name)[index]
        got = sorted(got, key=lambda x: x.name)[index]
        assert got.name == expected.name
        assert dist(got.rwy, expected.rwy) < 750
        assert dist(got.rwy2, expected.rwy2) < 750
        assert dist(got.gate, expected.gate) < 750
        np.testing.assert_allclose(got.heading, expected.heading, atol=1)
