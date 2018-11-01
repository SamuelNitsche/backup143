from bin.both.fs_local import Backup
from bin.both.dbcon import dbmanager

# source = '/Users/samuelnitsche/Desktop/BackupTest'
# dest = '/Users/samuelnitsche/Desktop/backup.zip'

db = dbmanager()

query = db.query('SELECT * FROM \'143_tasks\'')
tasks = query.fetchall()
for task in tasks:
    print(task[2])


# print(backups.fetchone())

# backup = Backup(source, dest)
#
# backup.backup()