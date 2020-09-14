import psycopg2
from psycopg2.extensions import AsIs


def create_db_table():
    create_table_query = '''CREATE TABLE IF NOT EXISTS pcap_stb_result
                            (project                 TEXT    NOT NULL,
                             part_no                 TEXT    NOT NULL,
                             dut_lv                  TEXT    NOT NULL,
                             ic_vender               TEXT,
                             ic_model                TEXT,
                             config_file             TEXT    NOT NULL,
                             tuning                  TEXT    NOT NULL,
                             testing                 TEXT,
                             remark              TEXT,
                             test_date               DATE,
                             all_max             REAL    NOT NULL,
                             all_mean            REAL    NOT NULL,
                             withoutedge_max     REAL    NOT NULL,
                             withoutedge_mean    REAL    NOT NULL,
                             allmax_jitter       REAL    NOT NULL,
                             jitter_ratio         REAL    NOT NULL,
                             detected_ratio       REAL    NOT NULL,
                             hori_max_lin        REAL,
                             hori_mean_lin       REAL,
                             hori_max_drag_ratio  REAL,
                             hori_min_drag_ratio  REAL,
                             hori_break_count        SMALLINT,
                             vert_max_lin        REAL,
                             vert_mean_lin       REAL,
                             vert_max_drag_ratio  REAL,
                             vert_min_drag_ratio  REAL,
                             vert_break_count        SMALLINT,
                             diag_max_lin        REAL,
                             diag_mean_lin       REAL,
                             diag_max_drag_ratio REAL,
                             diag_min_drag_ratio REAL,
                             diag_break_count        SMALLINT,
                             PRIMARY KEY (project, part_no, config_file, remark));'''
    return create_table_query


def insert_db(db_settings_dict, db_dict):
    connection = None
    try:
        connection = psycopg2.connect(user=db_settings_dict['user'],          # default user: postgres
                                      password=db_settings_dict['password'],  # low security password: 123
                                      host=db_settings_dict['host'],          # host: 127.0.0.1
                                      port=db_settings_dict['port'],          # default port: 5432
                                      database=db_settings_dict['database'])  # database
        cursor = connection.cursor()
        cursor.execute('SELECT version();')
        record = cursor.fetchone()
        print('Connected to: ', record)
        cursor.execute('''SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name = 'pcap_stb_result')''')
        if not cursor.fetchone()[0]:
            cursor.execute(create_db_table())
            connection.commit()
        # start insert table
        columns = db_dict.keys()
        columns = [''+column+'' for column in columns]
        values = [db_dict[column] for column in columns]
        insert_statement = '''INSERT INTO pcap_stb_result (%s) VALUES %s'''
        cursor.execute(insert_statement, (AsIs(','.join(columns)), tuple(values)))
        # cursor.execute(create_db_table())
        # print(bool)
        connection.commit()
        print('success')
        return True
    except (Exception, psycopg2.Error) as error :
        print ('Error while connecting to Postgredb', error)
        return False
    finally:
            if connection:
                print(connection)
                cursor.close()
                connection.close()
                print('Postgredb connection is closed')

# write_db()
