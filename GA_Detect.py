from traffic.core import Traffic
from datetime import timedelta
import multiprocessing as mp
import OS_Funcs as OSF
import glob


def main(start_n):
    top_dir = '/gf2/eodg/SRP001_PROUD_TURBREP/GO_AROUNDS/VABB/'
    indir = top_dir + 'INDATA/'
    odir_nm = top_dir + 'OUT_PLOT/NORM/'
    odir_ga = top_dir + 'OUT_PLOT/PSGA/'

    files = glob.glob(indir+'*.pkl')
    files.sort()

    fli_len = len(files)

    colormap = {'GND': 'black', 'CL': 'green', 'CR': 'blue',
                'DE': 'orange', 'LVL': 'purple', 'NA': 'red'}

    # Number of files to open in one go
    n_files_proc = 55

    pool_proc = 100

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
        traf_arr = Traffic.from_flights(f_data)

        p_list = []
        f_data = []

        end_time = traf_arr.end_time

        # Now we process the results
        for flight in traf_arr:
            if (flight.stop + timedelta(minutes=5) < end_time):
                p_list.append(pool.apply_async(OSF.proc_fl, args=(flight,
                                                                  odir_nm,
                                                                  odir_ga,
                                                                  colormap,
                                                                  False,)))
            else:
                f_data.append(flight)

        for p in p_list:
            t_res = p.get()


main(5116)
