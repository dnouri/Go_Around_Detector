# The threshold altitude used to determine if a go-around occurred,
# check if points in a given time window (below) after a state change
# are above this altitude
alt_thresh = 500.

# The threshold vertical rate used to determine if a go-around occurred,
# check if points in a given time window (below) after a state change
# contain vertical rates above this threshold
vrt_thresh = 200.

# This sets a time in the future to check, to ensure the aircraft
# is actually going around and not landing (sometimes status changes
# from 'descent' to 'level' rather than 'ground' for a landing
ga_tcheck = 120.


# Takeoff threshold
takeoff_thresh_alt = 400.


# The threshold altitude for the state change, if change occurs above
# this altitude then it's probably not a go-around
ga_st_alt_t = 500.
