DROP TABLE IF EXISTS weekends;
DROP TABLE IF EXISTS races;
DROP TABLE IF EXISTS karts;
DROP TABLE IF EXISTS finish;
DROP TABLE IF EXISTS qualifying;
DROP TABLE IF EXISTS laps;

CREATE TABLE weekends (
    id INTEGER AUTOINCREMENT,
    year INTEGER NOT NULL,
    weekend_name TEXT NOT NULL,
    PRIMARY KEY (year , weekend_name)
);

CREATE TABLE races (
    id INTEGER AUTOINCREMENT,
    weekend_id INTEGER NOT NULL,
    race_name TEXT NOT NULL,
    race_type TEXT NOT NULL,
    PRIMARY KEY (race_name, weekend_id),
    FOREIGN KEY (weekend_id)
        REFERENCES weekends (id)
        ON UPDATE CASCADE

);

CREATE TABLE karts (
    id INTEGER AUTOINCREMENT,
    kart_name TEXT NOT NULL PRIMARY KEY
);

CREATE TABLE finish (
    race_id INTEGER NOT NULL,
    kart_id INTEGER NOT NULL,
    finish INTEGER NOT NULL,
    PRIMARY KEY (race_id , kart_id),
    FOREIGN KEY (race_id)
        REFERENCES races (id)
        ON UPDATE CASCADE,
    FOREIGN KEY (kart_id)
        REFERENCES karts (id)
        ON UPDATE CASCADE
);

CREATE TABLE qualy (
    weekend_id INTEGER NOT NULL,
    kart_id INTEGER NOT NULL,
    qualy_rank INTEGER NOT NULL,
    qualy_time REAL,
    PRIMARY KEY (weekend_id , kart_id),
    FOREIGN KEY (weekend_id)
        REFERENCES weekends (id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (kart_id)
        REFERENCES karts (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE laps (
    race_id INTEGER NOT NULL,
    kart_id INTEGER NOT NULL,
    lap_num INTEGER NOT NULL,
    lap_time REAL NOT NULL,
    rank INTEGER NOT NULL,
    cum_time REAL NOT NULL,
    PRIMARY KEY (lap_num, race_id, kart_id),
    FOREIGN KEY (race_id)
        REFERENCES races (id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (kart_id)
        REFERENCES karts (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);