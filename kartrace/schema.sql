DROP TABLE IF EXISTS laps;
DROP TABLE IF EXISTS qualy;
DROP TABLE IF EXISTS finish;
DROP TABLE IF EXISTS karts;
DROP TABLE IF EXISTS races;
DROP TABLE IF EXISTS weekends;




CREATE TABLE weekends (
        id SERIAL PRIMARY KEY,
        year INTEGER NOT NULL,
        weekend_name VARCHAR(255) NOT NULL,
        UNIQUE (year, weekend_name)
);

CREATE TABLE races (
        id SERIAL PRIMARY KEY,
        weekend_id INTEGER NOT NULL,
        race_name VARCHAR(255) NOT NULL,
        race_type VARCHAR(255) NOT NULL,
        UNIQUE (weekend_id, race_name),
        FOREIGN KEY (weekend_id)
            REFERENCES weekends (id)
            ON UPDATE CASCADE

);

CREATE TABLE karts (
        id SERIAL PRIMARY KEY,
        kart_name VARCHAR(255) NOT NULL UNIQUE
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
            ON UPDATE CASCADE,
        FOREIGN KEY (kart_id)
            REFERENCES karts (id)
            ON UPDATE CASCADE
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
            ON UPDATE CASCADE,
        FOREIGN KEY (kart_id)
            REFERENCES karts (id)
            ON UPDATE CASCADE
);