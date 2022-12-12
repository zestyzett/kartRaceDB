import pandas as pd
import time
import logging
import psycopg2
from kartrace.config import config

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
start_time = time.time()
logging.debug("--- %s seconds ---" % (time.time() - start_time))


#logging.disable(logging.CRITICAL)

#pull master lsit and convert to list
kartList = pd.read_csv('data\kart master list.csv', header = None)
kartList = kartList[0].tolist()


def insertKart(kartName):
    """ insert a new kart into the karts table """
    sql = """INSERT INTO karts(kartName)
             VALUES(%s) RETURNING kartID;"""
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
        cur.execute(sql, (kartName,))
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


"""insert karts into database, kartID is autoincremented so it is not necessary to send
this will make it easier to add karts later
right now I am making all karts have unique names"""
for i in kartList:
    insertKart(i)

logging.debug("--- %s seconds ---" % (time.time() - start_time))