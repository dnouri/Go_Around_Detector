"""A script to process OpenSky ADS-B data in an attempt to detect go-around events at an airport."""
from traffic.core import Traffic
from datetime import timedelta
import multiprocessing as mp
import metar_parse as MEP
from OS_Airports.RWY import get_runway_list
import OS_Funcs as OSF
import os
import glob
import click


@click.command()
@click.option('--top-dir', default='./')
@click.option('--start-n', default=0)
@click.option('--do-write/--no-write', default=True)
@click.option('--do-plot/--no-plot', default=True)
@click.option('--metars-file', default='VABB_METAR')
@click.option('--airport', default='VABB')
@click.option('--n-files-proc', default=55)
@click.option('--pool-proc', default=16)
@click.option('--verbose', default=False)
def main(top_dir, start_n, do_write, do_plot, metars_file, airport,
         n_files_proc, pool_proc, verbose):
    """The main code for detecting go-arounds.

    Arguments:
    start_n -- The index of the first file to read
    do_write -- boolean flag specifying whether to output data to textfile

    """
    # Total number of aircraft seen
    tot_n_ac = 0

    # Of which go-arounds
    tot_n_ga = 0

    # indir stores the opensky data
    indir = top_dir + 'INDATA/'

    # odir_nm stores plots for normal landings
    odir_pl_nm = top_dir + 'OUT_PLOT/NORM/'

    # odir_ga stores plots for detected go-arounds
    odir_pl_ga = top_dir + 'OUT_PLOT/PSGA/'

    # odir_nm stores plots for normal landings
    odir_da_nm = top_dir + 'OUT_DATA/NORM/'

    # odir_ga stores plots for detected go-arounds
    odir_da_ga = top_dir + 'OUT_DATA/PSGA/'

    odirs = [odir_pl_nm, odir_pl_ga, odir_da_nm, odir_da_ga]
    for odir in odirs:
        os.makedirs(odir, exist_ok=True)

    # Output filenames for saving data about go-arounds
    out_file_ga = top_dir + 'GA_MET_NEW.csv'
    # Output filenames for saving data about non-go-arounds
    out_file_noga = top_dir + 'GA_NOGA_NEW.csv'

    t_frmt = "%Y/%m/%d %H:%M:%S"

    # File to save met info for g/a flights
    if (do_write):
        metfid = open(out_file_ga, 'w')
        nogfid = open(out_file_noga, 'w')
        metfid.write('ICAO24, Callsign, GA_Time, L_Time, Runway, Heading, Alt, Lat, \
                      Lon, gapt, rocvar, hdgvar, latvar, lonvar, gspvar, \
                      Temp, Dewp, Wind_Spd, Wind_Gust, Wind_Dir,Cld_Base,\
                      CB, Vis, Pressure\n')
        nogfid.write('ICAO24, Callsign, GA_Time, L_Time, Runway, gapt, rocvar, \
                      hdgvar, latvar, lonvar, gspvar, \
                      Temp, Dewp, Wind_Spd, Wind_Gust, Wind_Dir,Cld_Base,\
                      CB, Vis, Pressure\n')
    files = []
    files = glob.glob(indir+'*.pkl') + glob.glob(indir+'*/*.pkl')
    files.sort()

    fli_len = len(files)

    colormap = {'GND': 'black', 'GN': 'black', 'CL': 'green', 'CR': 'blue',
                'DE': 'orange', 'LVL': 'purple', 'NA': 'red'}

    metars = MEP.get_metars(metars_file, verbose=verbose)
    rwy_list = get_runway_list(airport)

    f_data = []
    pool = mp.Pool(processes=pool_proc)

    for main_count in range(start_n, fli_len, n_files_proc):
        print("Processing batch starting with "
              + str(main_count + 1).zfill(5) + " of "
              + str(fli_len).zfill(5))

        p_list = []
        # First we load several files at once
        for j in range(0, n_files_proc):
            if (main_count+j < fli_len):
                p_list.append(pool.apply_async(OSF.get_flight,
                                               args=(files[main_count+j],)))

        for p in p_list:
            t_res = p.get()
            for fli in t_res:
                f_data.append(fli)
        if(len(f_data) < 1):
            continue
        traf_arr = Traffic.from_flights(f_data)
        p_list = []
        f_data = []
        # Extend array end time if there's only one flight, else processing
        # will fail as we check to ensure latest flight is > 5 mins from end
        if (len(traf_arr) == 1):
            end_time = traf_arr.end_time + timedelta(minutes=10)
            print("Extending timespan due to single aircraft")
        else:
            end_time = traf_arr.end_time

        # Now we process the results
        for flight in traf_arr:
            if (flight.stop + timedelta(minutes=5) < end_time):
                p_list.append(pool.apply_async(OSF.proc_fl,
                                               args=(flight,
                                                     metars,
                                                     rwy_list,
                                                     odirs,
                                                     colormap,
                                                     do_plot,
                                                     verbose,)))
            else:
                f_data.append(flight)

        for p in p_list:
            t_res = p.get()
            if (t_res != -1):
                tot_n_ac += 1
                # If there's a go-around, this will be True
                if (t_res[0]):
                    if (do_write):
                        metfid.write(t_res[1] + ',' + t_res[2] + ',')
                        metfid.write(t_res[3].strftime(t_frmt) + ',')
                        metfid.write(t_res[4].strftime(t_frmt) + ',')
                        metfid.write(t_res[5] + ',')
                        if (t_res[6] < 0):
                            t_res[6] = 360 + t_res[6]
                        metfid.write(str(t_res[6]) + ',')
                        metfid.write(str(t_res[7]) + ',')
                        metfid.write(str(t_res[8]) + ',')
                        metfid.write(str(t_res[9]) + ',')
                        metfid.write(str(t_res[10]) + ',')
                        metfid.write(str(t_res[11]) + ',')
                        metfid.write(str(t_res[12]) + ',')
                        metfid.write(str(t_res[13]) + ',')
                        metfid.write(str(t_res[14]) + ',')
                        metfid.write(str(t_res[15]) + ',')
                        metfid.write(str(t_res[16].temp) + ',')
                        metfid.write(str(t_res[16].dewp) + ',')
                        metfid.write(str(t_res[16].w_s) + ',')
                        metfid.write(str(t_res[16].w_g) + ',')
                        metfid.write(str(t_res[16].w_d) + ',')
                        metfid.write(str(t_res[16].cld) + ',')
                        if t_res[16].cb:
                            metfid.write('1,')
                        else:
                            metfid.write('0,')
                        metfid.write(str(t_res[16].vis) + ',')
                        metfid.write(str(t_res[16].pres) + '\n')
                    tot_n_ga += 1
                # Otherwise, do the following (doesn't save g/a location etc).
                else:
                    if (do_write):
                        nogfid.write(t_res[1] + ',' + t_res[2] + ',')
                        nogfid.write(t_res[3].strftime(t_frmt) + ',')
                        nogfid.write(t_res[4].strftime(t_frmt) + ',')
                        nogfid.write(t_res[5] + ',')
                        nogfid.write(str(t_res[10]) + ',')
                        nogfid.write(str(t_res[11]) + ',')
                        nogfid.write(str(t_res[12]) + ',')
                        nogfid.write(str(t_res[13]) + ',')
                        nogfid.write(str(t_res[14]) + ',')
                        nogfid.write(str(t_res[15]) + ',')
                        try:
                            outstr = str(t_res[16].temp) + ','
                            outstr = outstr + str(t_res[16].dewp) + ','
                            outstr = outstr + str(t_res[16].w_s) + ','
                            outstr = outstr + str(t_res[16].w_g) + ','
                            outstr = outstr + str(t_res[16].w_d) + ','
                            outstr = outstr + str(t_res[16].cld) + ','
                            if t_res[16].cb:
                                outstr = outstr + '1,'
                            else:
                                outstr = outstr + '0,'
                            outstr = outstr + str(t_res[16].vis) + ','
                            outstr = outstr + str(t_res[16].pres)
                        except Exception as e:
                            print("No METAR data for this flight")
                            outstr = ''
                        nogfid.write(outstr + '\n')

        print("\t-\tHave processed " + str(tot_n_ac) +
              " aircraft. Have seen " + str(tot_n_ga) + " go-arounds.")

    if (do_write):
        metfid.close()
        nogfid.close()


if __name__ == '__main__':
    main()
