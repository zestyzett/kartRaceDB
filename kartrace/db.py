import sqlite3
import psycopg2
import pandas as pd
import click
import os
from flask import current_app, g
from configparser import ConfigParser


def dbconfig(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def get_db():

        
    params = dbconfig()
    # connect to the PostgreSQL server
    conn = psycopg2.connect(**params)
    #cur = conn.cursor()

    return conn

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.cursor().close()
    


def insertKart(kartName, conn = get_db()):
    
    conn.cursor().execute('INSERT INTO karts (kart_name)'
                ' VALUES(%s);',
            (kartName,)
    )
    conn.commit()
    
def getKartID(kartName, conn = get_db()):

    db = conn.cursor()
    db.execute("""SELECT id from karts WHERE kart_name = %s;""", (kartName,))
    kartID = db.fetchone()

    return kartID

def insertWeekend(year, weekendName, conn = get_db()):
    
    conn.cursor().execute('INSERT INTO weekends (year, weekend_name)'
                ' VALUES(%s,%s);',
            (year, weekendName)
    )
    conn.commit()

def getWeekendID(year, weekendName, conn = get_db()):

    db = conn.cursor()
    db.execute("""SELECT id from weekends WHERE year = %s AND weekend_name = %s;""",
        (year, weekendName)
    )
    
    weekendID = db.fetchone()

    return weekendID

def insertQualy(weekendID, kartID, qualPosition, qualTime, conn = get_db()):
    
    conn.cursor().execute('INSERT INTO qualy (weekend_id, kart_id, qualy_rank, qualy_time)'
                ' VALUES(%s,%s,%s,%s);',
            (weekendID, kartID, qualPosition, qualTime)
    )
    conn.commit()

def parseQualy(qualy, weekendID):

    conn = get_db()

    for i in qualy.index:
            
            qualPosition = i+1
            kartName = qualy[0][i]
            qualTime = qualy[1][i]

            kartID = getKartID(kartName, conn)

            #logging.debug(kartName,kartID)

            insertQualy(weekendID, kartID, qualPosition, qualTime, conn)

def insertRace(weekendID, raceName, raceType, conn):
    
    conn.cursor().execute('INSERT INTO races (weekend_id, race_name, race_type)'
             'VALUES(%s,%s,%s);',
            (weekendID, raceName, raceType)
    )
    conn.commit()

def getRaceID(raceName, weekendID, conn):

    db = conn.cursor() 
    db.execute("""SELECT id from races WHERE race_name = %s AND weekend_id = %s;""",
        (raceName, weekendID)
    )
    
    raceID = db.fetchone()

    return raceID

def insertFinish(raceID, kartID, finish, conn):

    conn.cursor().execute('INSERT INTO finish(race_id, kart_id, finish)'
             'VALUES(%s,%s,%s);',
            (raceID, kartID, finish)
    )
    conn.commit()

def insertLap(raceID, kartID, lapNumber, lapTime, cumTime, rank, conn):

    conn.cursor().execute('INSERT INTO laps(race_id, kart_id, lap_num, lap_time, cum_time, rank)'
             'VALUES(%s,%s,%s,%s,%s,%s);',
            (raceID, kartID, lapNumber, lapTime, cumTime, rank)
    )
    conn.commit()

def parseRace(raceID, raceData):
    
    conn = get_db()

    del raceData['lap']
    #cumulative some of lap times, total elapsed time    
    lapDataCumSum = raceData.iloc[:, :].cumsum()

    #lap by lap ranking summary based off cumsum
    rankData = lapDataCumSum.rank(axis = 1, ascending = True)
     
    finish = 1
    
    for kart in raceData.columns.values:
        
        kartID = getKartID(kart, conn)
        
        insertFinish(raceID, kartID, finish, conn)


        
        for i in raceData.index:
        
            if pd.isnull(raceData[kart][i]):
                continue

            lap = i+1
            laptime = raceData[kart][i]
            cumTime = lapDataCumSum[kart][i]
            rank = rankData[kart][i]
            insertLap(raceID, kartID, lap,laptime,cumTime, rank, conn)

        finish+=1

def populate_db():

    kartList = pd.read_csv('kartrace\static\data\kart master list.csv', header = None)
    kartList = kartList[0].tolist()

    conn = get_db()

    for i in kartList:
        insertKart(i, conn)

    listOfWeekends = os.listdir("kartrace\static\data\qualifying")

    for file in listOfWeekends:
        weekendName = file.split("-")[0]
        year = file.split("-")[1]

        insertWeekend(year,weekendName, conn)

        weekendID = getWeekendID(year,weekendName, conn)

        qualy = pd.read_csv('kartrace\static\data\qualifying\%s' % file, header = None )
        
        parseQualy(qualy, weekendID)

    listOfRaces = os.listdir("kartrace\static\data\Raw")

    for file in listOfRaces:
        #i prebaked the info in the file name
        weekendName = file.split("-")[0].lower()
        year = int(file.split("-")[1])
        raceName = file.split("-")[2][:-4]

    
        #this is hardcoded because there are only two race types
        if raceName[0].lower() == 's':
            raceType = 'sprint'
        else:
            raceType = 'endurance'

        #fetches weekend ID
        weekendID = getWeekendID(year,weekendName, conn)

        insertRace(weekendID, raceName, raceType, conn)

        raceData = pd.read_csv('kartrace\static\data\Raw\%s' % file)

        raceID = getRaceID(raceName,weekendID, conn)

        parseRace(raceID, raceData)

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.cursor().execute(f.read())
        db.commit()


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables"""
    init_db()
    populate_db()
    click.echo('Initialized the database.') 

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)