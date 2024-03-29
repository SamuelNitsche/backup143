import sqlite3
import os.path
from datetime import datetime
from bin.both.log import LogginSystem as logsys

class dbmanager():
    def __init__(self, dict=False):
        try:
            script_dir = os.path.dirname(__file__)
            rel_path = "../../backup143.db"
            database_file_path = os.path.join(script_dir, rel_path)
            self.conn = sqlite3.connect(database_file_path, check_same_thread=False)
            if dict:
                self.conn.row_factory = self.dict_factory
            self.cur = self.conn.cursor()
            log = logsys('db')
            log.write('Successfully connected to backup143.db')
        except sqlite3.Error as e:
            log = logsys('db')
            log.write('Couldn\'t connect to backup143.db (' + str(e) + ')')

    def query(self, arg):
        log = logsys('db')
        log.write('Executing Query: "' + arg + '"')
        self.cur.execute(arg)
        self.conn.commit()
        return self.cur

    def create(self):
        script_dir = os.path.dirname(__file__)
        rel_path = "../../backup143.db"
        database_file_path = os.path.join(script_dir, rel_path)
        if os.path.getsize(database_file_path) == 0:
            log = logsys('db')
            log.write('Database \'backup143.db\' is empty. Trying to insert default data...')
            try:
                script_dir = os.path.dirname(__file__)
                rel_path = "../files/create.sql"
                setup_file_path = os.path.join(script_dir, rel_path)
                f = open(setup_file_path,'r')
                sql = f.read()
                self.cur.executescript(sql)
                self.conn.commit()
                log = logsys('db')
                log.write('Successfully created Database and wrote default configuration!')
                return
            except sqlite3.Error as e:
                log = logsys('db')
                log.write('Error writing default data: \'' + str(e) + '\'')
                return
        else:
            return

    def log(self, task, value):
        date = datetime.now()
        query = f'INSERT INTO \'143_tasklog\' (date, taskid, value) VALUES (\'{date}\', {task}, \'{value}\')'
        self.query(query)

    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def __exit__(self):
        log = logsys('db')
        log.write('Closing Database connection with backup143')
        self.conn.close()