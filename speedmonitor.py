#!/usr/bin/env python
#
# Thanks to https://github.com/sivel/speedtest-cli
#
#
import speedtest,sqlite3

# Path where SQLite3 DB will be created and populated
database = "/var/spool/speedmonitor.db"

# Database structure
sql_create_table = """ CREATE TABLE IF NOT EXISTS speed (
                                        ip text NOT NULL,
					ping_time float NOT NULL,
					upload_speed float NOT NULL,
					download_speed float NOT NULL,
                                        add_date text NOT NULL
                                    ); """

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

# create a database connection
conn = create_connection(database)
if conn is not None:
    create_table(conn, sql_create_table)
else:
    print("Error! cannot create the database connection.")
    sys.exit(1)

# purge older row than 3 months (90 days)
conn.execute("DELETE FROM speed WHERE add_date <= date('now','-90 day')")

# start speedtest
s = speedtest.Speedtest()
s.get_best_server()
s.download()
s.upload()

results = s.results.dict()

speed_ip = results['client']['ip']
speed_ping_time = results['ping']
speed_upload = results['upload']
speed_download = results['download']

# Insert data into DB
conn.execute("INSERT INTO speed VALUES (?,?,?,?,date('now'))",(speed_ip,speed_ping_time,speed_upload,speed_download))
# Commit and close
conn.commit()
conn.close()
# DONE