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

listOfWeekends = os.listdir("data\qualifying")

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


def insertWeekend(year, weekendName):
    """ insert a weekend and qualy info """
    sql = """INSERT INTO weekends(year,weekendname)
             VALUES(%s,%s) RETURNING weekendid;"""
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
        cur.execute(sql, (year,weekendName))
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

def insertQualResult(weekendID, kartID, qualPosition, qualTime):
    """ insert a weekends qualy info """
    sql = """INSERT INTO qualifying(weekendid, kartid, qualifyingrank, qualifyingtime)
             VALUES(%s,%s,%s,%s);"""
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (weekendID, kartID, qualPosition, qualTime))
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

for file in listOfWeekends:
    weekendName = file.split("-")[0]
    year = file.split("-")[1]

    weekendID = insertWeekend(year,weekendName)

    qualifying = pd.read_csv('data\qualifying\%s' % file, header = None )
    
    for i in qualifying.index:
        


        qualPosition = i+1
        kartName = qualifying[0][i]
        qualTime = qualifying[1][i]

        kartID = getKartID(kartName)

        print(kartName,kartID)

        insertQualResult(weekendID, kartID, qualPosition, qualTime)






