import importlib
import os

from numpy import (
    arcsin,
    arctan2,
    cos,
    degrees,
    pi,
    radians,
    sin,
    )
import pandas
import requests


class rwy_data:
    ''' Defines a new runway for an airport. Takes the form:
    Name: Name of the runway, i.e: '01L'
    Mainhdg: Measured heading of the runway, often differs from the name
    Heading: Array of min/max values for aircraft heading: [ -11, 0, 0, 11]
             1st: Min heading, 2nd: Max heading for split
             3rd: Min heading for split, 4th: Max heading
             Split is necessary as some runways cross zero or 180 degrees,
             which makes calculations difficult.
    Rwy: Lat, lon of the runway threshold at the near end: [38.946, -77.474]
    Rwy2: Lat, lon of the runway threshold at the far end: [38.969, -77.474]
    Gate: Lat, lon of a checkpoint ~2.9km prior to the rwy: [38.920, -77.475]
    Then follows a series of numbers to define lines of best fit for approaches
    to a given runway. Each of these are a list containing 6 values for a
    polynomial fit: y = f0 * x^6 + f1 * x^5 ... f6
    '''
    def __init__(self, name, mainhdg, heading, rwy, rwy2, gate,
                 lons1=None, lonm=None, lonp1=None,
                 lats1=None, latm=None, latp1=None,
                 hdgs1=None, hdgm=None, hdgp1=None,
                 gals1=None, galm=None, galp1=None,
                 alts1=None, altm=None, altp1=None,
                 rocs1=None, rocm=None, rocp1=None):
                 
        self.name = name
        self.mainhdg = mainhdg
        self.heading = heading 
        self.rwy = rwy
        self.rwy2 = rwy2
        self.gate = gate
        self.lons1 = lons1
        self.lonm = lonm
        self.lonp1 = lonp1
        self.lats1 = lats1
        self.latm = latm
        self.latp1 = latp1
        self.hdgs1 = hdgs1
        self.hdgm = hdgm
        self.hdgp1 = hdgp1
        self.gals1 = gals1
        self.galm = galm
        self.galp1 = galp1
        self.alts1 = alts1
        self.altm = altm
        self.altp1 = altp1
        self.rocs1 = rocs1
        self.rocm = rocm
        self.rocp1 = rocp1

    def __eq__(self, other):
        return vars(self) == vars(other)

    def __repr__(self):
        return (
            'rwy_data(' +
            ', '.join([
                f'{key}={val!r}'
                for key, val in vars(self).items() if val is not None
                ]) +
            ')'
            )


def gate(rwy, rwy2, dist=2.9e3, R=6371e3):
    φ1, λ1 = radians(rwy[0]), radians(rwy[1])
    φ2, λ2 = radians(rwy2[0]), radians(rwy2[1])
    Δλ = λ2 - λ1
    θ = arctan2(sin(Δλ) * cos(φ2), cos(φ1) * sin(φ2) -
                sin(φ1) * cos(φ2) * cos(Δλ)) + pi
    φ3 = arcsin(sin(φ1) * cos(dist/R) +
                cos(φ1) * sin(dist/R) * cos(θ))
    λ3 = λ1 + arctan2(sin(θ) * sin(dist/R) * cos(φ1),
                      cos(dist/R) - sin(φ1) * sin(φ2))
    return [degrees(φ3), degrees(λ3)]


def retrieve_runway_list(name, runways_csv='runways.csv'):
    result = []
    if not os.path.exists(runways_csv):
        text = requests.get('https://ourairports.com/data/runways.csv').text
        with open(runways_csv, 'w') as f:
            f.write(text)
    runways = pandas.read_csv(runways_csv)
    runways = runways.query(f'airport_ident == "{name}"')
    for idx, row in runways.iterrows():
        le_heading = row.le_heading_degT
        he_heading = row.he_heading_degT
        if le_heading > 180:
            le_heading = -(360 - le_heading)
        if he_heading > 180:
            he_heading = -(360 - he_heading)
        result.append(rwy_data(
            name=row.le_ident,
            mainhdg=row.le_heading_degT,
            heading=[
                le_heading-10,
                le_heading,
                le_heading,
                le_heading+10,
                ],
            rwy=[row.le_latitude_deg, row.le_longitude_deg],
            rwy2=[row.he_latitude_deg, row.he_longitude_deg],
            gate=gate(
                [row.le_latitude_deg, row.le_longitude_deg],
                [row.he_latitude_deg, row.he_longitude_deg],
                ),
            ))
        result.append(rwy_data(
            name=row.he_ident,
            mainhdg=row.he_heading_degT,
            heading=[
                he_heading-10,
                he_heading,
                he_heading,
                he_heading+10,
                ],
            rwy=[row.he_latitude_deg, row.he_longitude_deg],
            rwy2=[row.le_latitude_deg, row.le_longitude_deg],
            gate=gate(
                [row.he_latitude_deg, row.he_longitude_deg],
                [row.le_latitude_deg, row.le_longitude_deg],
                ),
            ))
    return result


def get_runway_list(name):
    try:
        module = importlib.import_module(f'OS_Airports.{name}')
    except ModuleNotFoundError:
        return retrieve_runway_list(name)
    else:
        return getattr(module, 'rwy_list')
