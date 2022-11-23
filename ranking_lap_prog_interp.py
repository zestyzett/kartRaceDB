import pandas as pd
import numpy as np
import pprint
import bisect
import os
import time
import logging
import math

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
start_time = time.time()
logging.debug("--- %s seconds ---" % (time.time() - start_time))


#logging.disable(logging.CRITICAL)

name_image_lookup_array = pd.read_csv('C:\\Users\\Alex\\Documents\\PRS-race-data\\Kart name Directory - Sheet1.csv').to_numpy()
name_image_lookup_array = name_image_lookup_array.tolist()



lap_data = pd.read_csv('C:\\Users\\Alex\\Documents\\PRS-race-data\\Raw\\Copy of PRS Scoresheet Orlando 21 - Sprint 1.csv')

lap_data.pop("Lap")  # remove lap column

# find minimum lap time to use for time step
stacked_times = np.hstack(lap_data.values)
time_step = int(min(stacked_times))
logging.debug("Time_step: %s" % time_step)

lap_data_cumsum = lap_data.iloc[:, :].cumsum()

# find max race time to use for time step
stacked_times = np.hstack(lap_data_cumsum.values)
#duration = math.ciel(max(stacked_times))
duration = max(stacked_times)
logging.debug("Duration: %s" % duration)
output_grid = {}

rank = .001 

for k in lap_data_cumsum.keys():
    #logging.debug("Kart: %s" % k)
    output_grid[k] = []
    working_list = lap_data_cumsum[k].values.tolist()
    working_list.insert(0, 0)
    i = 0
    time_lower = 0
    time_higher = 0
    rank = lap_data_cumsum.columns.get_loc(k) + 1
    rel_lap = 0
    while i * time_step < duration:  # interpolating each lap at each time step

        time_current = (i + 1) * time_step
        ll = bisect.bisect_left(working_list, time_current) - 1

        if time_current > max(working_list):
            rel_lap = 1 / rank * .01 + (ll+1) # fudges progression of final lap to reflect race finish rank
        else:
            time_lower = working_list[ll]
            time_higher = working_list[ll + 1]
            rel_lap = ((time_current - time_lower) / (time_higher - time_lower)) + (ll+1) #interpolation of progress of lap plus the lower lap number. it is plus 1 because ll is indexed at 0
        #logging.debug("Rel Lap: %s" % rel_lap)
        if i == 0:
            output_grid[k].append((rel_lap/100)+1) # fudge first lap position to reflect starting  grid at start of lap 1
        output_grid[k].append(rel_lap)
        i = i + 1

    kart_row = 0
    for i in range(0, len(name_image_lookup_array)):
        for j in name_image_lookup_array[i]:
            if str(j).lower().replace(" ", "") == str(k).lower().replace(" ", ""):
                kart_row = i
                break
        if kart_row != 0:
            break
    image_link = name_image_lookup_array[kart_row][4]

col_headers = np.arange(0, (duration + time_step)/60, time_step/60)
col_headers = col_headers.tolist()

#lap_progression = pd.DataFrame.from_dict(output_grid, orient='index', columns=col_headers)
lap_progression = pd.DataFrame.from_dict(output_grid, orient='columns')

ranking_data = lap_progression.rank(axis = 1, ascending = False)

ranking_data.index = ranking_data.index * time_step
ranking_data = ranking_data.reindex(range(ranking_data.index.max()+1))
ranking_data = ranking_data.interpolate('linear')

lap_progression.index = lap_progression.index * time_step
lap_progression = lap_progression.reindex(range(lap_progression.index.max()+1))
lap_progression = lap_progression.interpolate('linear')

lap_progression.to_json(path_or_buf='C:\\Users\\Alex\\Documents\\PRS-race-data\\lap_progression', orient="index")

ranking_data.to_json(path_or_buf='C:\\Users\\Alex\\Documents\\PRS-race-data\\ranking_data',orient="index")

logging.debug("--- %s seconds ---" % (time.time() - start_time))