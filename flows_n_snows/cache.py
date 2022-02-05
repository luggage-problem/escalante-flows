from utils import fetch_flows_to_df, fetch_snotel_to_df
import config
import sqlite3
import datetime
import pandas as pd

CREATE_TABLES = """
CREATE TABLE IF NOT EXISTS flow (
    id INTEGER PRIMARY KEY,
    gauge_id TEXT,
    datetime DATETIME,
    value FLOAT,
    date_pulled DATETIME
);
CREATE TABLE IF NOT EXISTS snotel (
    id INTEGER PRIMARY KEY,
    site_id TEXT,
    datetime DATETIME,
    value FLOAT,
    date_pulled DATETIME
);
"""

def update_db() -> None:
    with sqlite3.connect(config.db_uri) as con:
        con.executescript(CREATE_TABLES)
        # update snotel
        for snotel_site in config.snotel_sites.values():
            print(f'fetching values for snotel site {snotel_site}')
            most_recent_record = con.execute('SELECT datetime, value FROM snotel WHERE site_id=? ORDER BY datetime DESC LIMIT 1', (snotel_site,)).fetchone()
            if not most_recent_record:
                start_date = '01-01-1980'
            else:
                start_date = most_recent_record[0]
            current_date = datetime.datetime.today().strftime('%m-%d-%Y')
            values = [[snotel_site, row[1], row[4], datetime.datetime.today()] for row in fetch_snotel_to_df(snotel_site, start_date, current_date).itertuples()]
            con.executemany('INSERT INTO snotel (site_id, value, datetime, date_pulled) VALUES (?, ?, ?, ?)', values)

        # update flow
        print(f'fetching values for river gauge ({config.river_gauge})')
        most_recent_record = con.execute('SELECT datetime, value FROM flow WHERE gauge_id=? ORDER BY datetime DESC LIMIT 1', (config.river_gauge,)).fetchone()
        if not most_recent_record:
            start_date = '01-01-1980'
        else:
            start_date = most_recent_record[0]
        current_date = datetime.datetime.today().strftime('%m-%d-%Y')
        values = [[config.river_gauge, row[1], str(pd.to_datetime(row[0])), datetime.datetime.today()] for row in fetch_flows_to_df(config.river_gauge, start_date, current_date).itertuples()]
        con.executemany('INSERT INTO flow (gauge_id, value, datetime, date_pulled) VALUES (?, ?, ?, ?)', values)

def get_flows(river_id: str, start_date: str, end_date: str) -> pd.DataFrame:
    with sqlite3.connect(config.db_uri) as con:
        results = con.execute('SELECT gauge_id, datetime, value, date_pulled FROM flow WHERE gauge_id=? AND datetime BETWEEN ? AND ?', (river_id, start_date, end_date)).fetchall()
        return pd.DataFrame(results, columns=['gauge_id', 'datetime', 'value', 'date_pulled'])

def get_snotel(snotel_id: str, start_date: str, end_date: str) -> pd.DataFrame:
    with sqlite3.connect(config.db_uri) as con:
        results = con.execute('SELECT site_id, datetime, value, date_pulled FROM snotel WHERE site_id=? AND datetime BETWEEN ? AND ?', (snotel_id, start_date, end_date)).fetchall()
        return pd.DataFrame(results, columns=['site_id', 'datetime', 'value', 'date_pulled'])

if __name__ == '__main__':
    update_db(config.db_uri)