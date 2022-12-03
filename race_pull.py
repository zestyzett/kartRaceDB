import pandas as pd
import time
import logging
import psycopg2
from config import config

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
start_time = time.time()
logging.debug("--- %s seconds ---" % (time.time() - start_time))

def getLaps(raceid):
    """ return lap info for given raceid """
    sql = """SELECT *
            FROM laps
            WHERE raceid = '%s';"""
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
        cur.execute(sql % raceid)
        
        # get the generated id back
        lapData = cur.fetchall()
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return lapData

df = pd.DataFrame( data = getLaps(1), columns= ['raceid','kartid','lapnum','laptime','rank','cumtime'])



lapTimes = df.pivot(index = 'lapnum', columns= 'kartid', values='laptime')

lapRanks = df.pivot(index = 'lapnum', columns= 'kartid', values='rank')

cumtimes = df.pivot(index = 'lapnum', columns= 'kartid', values='cumtime')

print("ha,",lapTimes[10][3])

logging.debug("--- %s seconds ---" % (time.time() - start_time))