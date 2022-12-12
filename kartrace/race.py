import pandas as pd
import numpy as np
import bisect
import psycopg2
import psycopg2.extras
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from kartrace.db import get_db

bp = Blueprint('race',__name__)

@bp.route('/race')
def race():
    conn = get_db()
    db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    db.execute("""SELECT id, race_name FROM races order by race_name""")
    races = db.fetchall()
    
    x,y = animationFactory(1)
    return render_template('race/race.html',races=races, x=x, y=y)

def getLaps(raceid):
    conn = get_db()
    db = conn.cursor()
    db.execute("""SELECT karts.kart_name, lap_num, lap_time, rank, cum_time
            FROM laps
            INNER JOIN karts on karts.id = laps.kart_id
            WHERE race_id = '%s';""",(raceid,))
    lapdata = db.fetchall()

    return lapdata

def getQualy(raceid):
    conn = get_db()
    db = conn.cursor()
    db.execute("""SELECT weekend_id from races WHERE id = %s""",(raceid,))
    weekendID = db.fetchone()

    db.execute("""SELECT kart_name, qualy_rank 
                FROM qualy 
                INNER JOIN karts on karts.id = qualy.kart_id
                WHERE weekend_id = %s""",(weekendID,))
    x = db.fetchall()
    startPos = dict(x)

    return startPos

def getFinish(raceid):
    conn = get_db()
    db = conn.cursor()
    
    db.execute("""SELECT kart_name, finish 
                FROM finish 
                INNER JOIN karts on karts.id = finish.kart_id 
                WHERE race_id = %s""",(raceid,))
    x = db.fetchall()
    finishPos = dict(x)
    
    return finishPos


def animationFactory(raceid):

    df = pd.DataFrame( data = getLaps(raceid), columns= ['kart_name','lap_num','lap_time','rank','cum_time'])

    lapTimes = df.pivot(index = 'lap_num', columns= 'kart_name', values='lap_time')

    #lapRanks = df.pivot(index = 'lap_num', columns= 'kart_name', values='rank')

    cumTimes = df.pivot(index = 'lap_num', columns= 'kart_name', values='cum_time')

    duration = max(pd.DataFrame.max(cumTimes))
    timeStep = int(min(pd.DataFrame.min(lapTimes)))

    output_grid = {}

    startPos = getQualy(raceid)
    finishPos = getFinish(raceid)

    for k in cumTimes.keys():
        #logging.debug("Kart: %s" % k)
        output_grid[k] = []
        working_list = cumTimes[k].values.tolist()
        working_list.insert(0, 0)
        i = 0
        time_lower = 0
        time_higher = 0
        finishRank = finishPos[k]
        rel_lap = 0
        while i * timeStep < duration:  # interpolating each lap at each time step

            time_current = (i + 1) * timeStep
            ll = bisect.bisect_left(working_list, time_current) - 1

            if time_current > max(working_list):
                rel_lap = 1 / finishRank * .01 + (ll+1) # fudges progression of final lap to reflect race finish rank
            else:
                time_lower = working_list[ll]
                time_higher = working_list[ll + 1]
                rel_lap = ((time_current - time_lower) / (time_higher - time_lower)) + (ll+1) #interpolation of progress of lap plus the lower lap number. it is plus 1 because ll is indexed at 0
            #logging.debug("Rel Lap: %s" % rel_lap)
            if i == 0:
                output_grid[k].append(1+1/(startPos[k]*100)) # fudge first lap position to reflect starting  grid at start of lap 1 
                #should use qualifying if possible
            output_grid[k].append(rel_lap)
            i = i + 1



    col_headers = np.arange(0, (duration + timeStep)/60, timeStep/60)
    col_headers = col_headers.tolist()

    #lap_progression = pd.DataFrame.from_dict(output_grid, orient='index', columns=col_headers)
    lap_progression = pd.DataFrame.from_dict(output_grid, orient='columns')

    ranking_data = lap_progression.rank(axis = 1, ascending = False)

    ranking_data.index = ranking_data.index * timeStep
    ranking_data = ranking_data.reindex(range(ranking_data.index.max()+1))
    ranking_data = ranking_data.interpolate('linear')

    lap_progression.index = lap_progression.index * timeStep
    lap_progression = lap_progression.reindex(range(lap_progression.index.max()+1))
    lap_progression = lap_progression.interpolate('linear')

    lap_progression.to_dict( orient="index" )

    ranking_data.to_dict( orient="index" )

    return lap_progression, ranking_data