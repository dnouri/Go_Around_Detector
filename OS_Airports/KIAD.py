import OS_Airports.RWY as RWY

rwy_01l = RWY.rwy_data('01L',
                       [-11., 0., 0., 11.],
                       [38.946484, -77.474800],
                       [38.969244, -77.474411],
                       [38.920293, -77.47556])

rwy_01c = RWY.rwy_data('01C',
                       [-11., 0., 0., 11.],
                       [38.940606, -77.459754],
                       [38.969065, -77.459342],
                       [38.91455, -77.46019])

rwy_01r = RWY.rwy_data('01R',
                    [-11., 0., 0., 11.],
                       [38.925277, -77.436404],
                       [38.953764, -77.435980],
                       [38.899013, -77.436880])

rwy_19l = RWY.rwy_data('19L',
                       [-180.05, -170., 170., 180.05],
                       [38.953764, -77.435980],
                       [38.925277, -77.436404],
                       [38.979806, -77.435867])

rwy_19c = RWY.rwy_data('19C',
                       [-180.05, -170., 170., 180.05],
                       [38.969065, -77.459342],
                       [38.940606, -77.459754],
                       [38.995216, -77.458928])

rwy_19r = RWY.rwy_data('19R',
                       [-180.05, -170., 170., 180.05],
                       [38.969244, -77.474411],
                       [38.946484, -77.474800],
                       [38.995225, -77.474642])

rwy_list = [rwy_01l, rwy_01c, rwy_01r,
            rwy_19l, rwy_19c, rwy_19r]