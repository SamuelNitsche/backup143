from bin.both.dbcon import dbmanager

db = dbmanager()


def recordbackupfile(taskid, date, status, path):
    query = f'INSERT INTO \'143_backupfiles\' (taskid, date, status, path) ' \
            f'VALUES (\'{taskid}\', \'{date}\', \'{status}\', \'{path}\')'
    db.query(query)
