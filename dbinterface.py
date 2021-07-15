import sqlite3


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
    request text NOT NULL,
    word text NOT NULL,
    result text NOT NULL,
    ip varchar(16) NOT NULL,
    browser text NOT NULL
    )""")
    con.commit()


def log_event_ins(log_date_time, request, word, result, ip, browser):
    con = connect()
    cur = con.cursor()
    _SQL = """INSERT INTO log (
                    log_date_time,
                    request,
                    word,
                    result,
                    ip,
                    browser
                )
                VALUES ( ?, ?, ?, ?, ?, ? );"""
    print(_SQL)
    cur.execute(_SQL, (str(log_date_time), str(request), str(word), str(result), str(ip), str(browser)))
    con.commit()


def list_tables(cur, con):
    cur.execute("""select * from sqlite_master""")
    res = cur.fetchall()
    print(res)
