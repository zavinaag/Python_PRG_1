import sqlite3
from DBcm import DBcm


def connect():
    try:
        with sqlite3.connect('webapp.db') as con:
            return con
    except FileNotFoundError():
        print("No such file")


def create_log_table() -> None:
    con = connect()
    cur = con.cursor()
    cur.execute("""create table if not exists log (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
    log_date_time text,
    ts timestamp default current_timestamp, 
    word text NOT NULL,
    result text NOT NULL,
    ip varchar(16) NOT NULL,
    browser text NOT NULL
    )""")
    con.commit()
    cur.close()


def log_event_ins(log_date_time, word, result, ip, browser):
    con = connect()
    cur = con.cursor()
    _SQL = """INSERT INTO log (
                    log_date_time,
                    word,
                    result,
                    ip,
                    browser
                )
                VALUES ( ?, ?, ?, ?, ? );"""
    cur.execute(_SQL, (str(log_date_time), str(word), str(result), str(ip), str(browser)))
    cur.close()
    con.commit()


def log_event_ins_dbcm(log_date_time, word, result, ip, browser):
    iparam = {'database': 'webapp.db'}
    with DBcm(iparam) as cur:
        _SQL = """INSERT INTO log_dbcm (
                        log_date_time,
                        word,
                        result,
                        ip,
                        browser
                    )
                    VALUES ( ?, ?, ?, ?, ? );"""
        cur.execute(_SQL, (str(log_date_time), str(word), str(result), str(ip), str(browser)))


def log_event_get() -> list:
    con = connect()
    cur = con.cursor()
    _SQL = "select * from log"
    cur.execute(_SQL)
    res = []
    for row in cur.fetchall():
        res.append(row)
    return res
