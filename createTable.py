#createTable

import psycopg2
from config import config


def createTables():
    """ create tables in the PostgreSQL database"""
    commands = (
                
        """ 
        CREATE TABLE weekends (
                weekendID SERIAL PRIMARY KEY,
                year INTEGER NOT NULL,
                weekendName VARCHAR(255) NOT NULL
                )
        """,
        """
        CREATE TABLE races (
                raceID SERIAL PRIMARY KEY,
                weekendID INTEGER NOT NULL,
                raceName VARCHAR(255) NOT NULL,
                raceType VARCHAR(255) NOT NULL,
                FOREIGN KEY (weekendID)
                    REFERENCES weekends (weekendID)
                    ON UPDATE CASCADE ON DELETE CASCADE

        )
        """,
        """
        CREATE TABLE karts (
                kartID SERIAL PRIMARY KEY,
                kartName VARCHAR(255) NOT NULL
        )
        """,
        """
        CREATE TABLE finish (
                raceID INTEGER NOT NULL,
                kartID INTEGER NOT NULL,
                finish INTEGER NOT NULL,
                PRIMARY KEY (raceID , kartID),
                FOREIGN KEY (raceID)
                    REFERENCES races (raceID)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (kartID)
                    REFERENCES karts (kartID)
                    ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE qualifying (
                weekendID INTEGER NOT NULL,
                kartID INTEGER NOT NULL,
                qualifyingRank INTEGER NOT NULL,
                qualifyingTIME REAL,
                PRIMARY KEY (weekendID , kartID),
                FOREIGN KEY (weekendID)
                    REFERENCES weekends (weekendID)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (kartID)
                    REFERENCES karts (kartID)
                    ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE laps (
                raceID INTEGER NOT NULL,
                kartID INTEGER NOT NULL,
                lapNumber INTEGER NOT NULL,
                lapTime REAL NOT NULL,
                PRIMARY KEY (lapNumber, raceID, kartID),
                FOREIGN KEY (raceID)
                    REFERENCES races (raceID)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (kartID)
                    REFERENCES karts (kartID)
                    ON UPDATE CASCADE ON DELETE CASCADE
        )
        """)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    createTables()