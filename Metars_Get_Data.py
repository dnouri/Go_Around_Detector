import click
import requests

METAR_URL_TEMPLATE = 'https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station={station}&data=metar&year1={year1}&month1={month1}&day1={day1}&year2={year2}&month2={month2}&day2={day2}&tz=Etc%2FUTC&format=onlycomma&latlon=no&missing=M&trace=T&direct=no&report_type=1&report_type=2'


@click.command()
@click.option('--station', default='VABB')
@click.option('--start-dt', default='2019-08-10')
@click.option('--end-dt', default='2019-08-21')
@click.option('--outfile', default=None)
def main(station, start_dt, end_dt, outfile):
    if outfile is None:
        outfile = f'{station}_METAR'
    year1, month1, day1 = start_dt.split('-')
    year2, month2, day2 = end_dt.split('-')
    url = METAR_URL_TEMPLATE.format(
        station=station,
        year1=year1, month1=month1, day1=day1,
        year2=year2, month2=month2, day2=day2,
        )
    resp = requests.get(url)
    resp.raise_for_status()

    with open(outfile, 'w') as fout:
        fout.writelines(line + '\n' for line in resp.text.splitlines()[1:])


if __name__ == '__main__':
    main()
