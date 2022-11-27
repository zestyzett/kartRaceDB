import pandas as pd
import time
import logging
import psycopg2
import os
from config import config

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
start_time = time.time()
logging.debug("--- %s seconds ---" % (time.time() - start_time))


#logging.disable(logging.CRITICAL)

listOfRaces = os.listdir("data\Raw")

def getKartID(kartName):
    """ return kartid matching kartname """
    sql = """SELECT kartid 
            FROM karts
            WHERE kartname = '%s';"""
    conn = None
    kartID = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql % kartName)
        
        # get the generated id back
        kartID = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return kartID

def getWeekendID(weekendName, year):
    """ return weekendid matching weekendname and year"""
    sql = """SELECT weekendid 
            FROM weekends
            WHERE weekendname = %s AND year = %s;"""
    conn = None
    weekendID = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (weekendName,year))
        
        # get the generated id back
        weekendID = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return weekendID


#creates new race and returns raceid
def insertRace(weekendID, raceName, raceType):
    """ insert a race and info """
    sql = """INSERT INTO races(weekendid,racename,racetype)
             VALUES(%s,%s,%s) RETURNING raceid;"""
    conn = None
    raceID = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (weekendID, raceName, raceType))
        # get the generated id back
        raceID = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return raceID

def insertFinish(raceID, kartID, finishRank):
    """ insert a race finish info """
    sql = """INSERT INTO finish(raceid, kartid, finish)
             VALUES(%s,%s,%s);"""
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (raceID, kartID, finishRank))
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insertLap(raceID, kartID, lapNumber, lapTime, cumTime, rank):
    """ insert a lap info """
    sql = """INSERT INTO laps(raceid, kartid, lapnumber, laptime, cumtime, rank)
             VALUES(%s,%s,%s,%s,%s,%s);"""
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (raceID, kartID, lapNumber, lapTime, cumTime, rank))
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

for file in listOfRaces:
    weekendName = file.split("-")[0].lower()
    year = int(file.split("-")[1])
    raceName = file.split("-")[2][:-4]

   
    
    if raceName[0].lower() == 's':
        raceType = 'sprint'
    else:
        raceType = 'endurance'

    weekendID = getWeekendID(weekendName, year)

    raceData = pd.read_csv('data\Raw\%s' % file)
    
    raceID = insertRace(weekendID,raceName, raceType)

    del raceData['lap']
    
    lapDataCumSum = raceData.iloc[:, :].cumsum()

    rankData = lapDataCumSum.rank(axis = 1, ascending = True)

     
    finish = 1

    logging.debug(raceName)
    
    for kart in raceData.columns.values:
        
        kartID = getKartID(kart)
        
        insertFinish(raceID, kartID, finish)


        
        for i in raceData.index:
        
            if pd.isnull(raceData[kart][i]):
                continue

            lap = i+1
            laptime = raceData[kart][i]
            cumTime = lapDataCumSum[kart][i]
            rank = rankData[kart][i]
            insertLap(raceID, kartID, lap,laptime,cumTime, rank)

        finish+=1



logging.debug("--- %s seconds ---" % (time.time() - start_time))
        

            
        

        








