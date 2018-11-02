from bin.both.dbcon import dbmanager
from crontab import CronTab
from datetime import datetime
import time

db = dbmanager(True)
threshold = 10

def startBackup(task):
    db.log(task, '=============STARTING=============')
    updateTaskState(task, 'running')

def finishBackup(task):
    db.log(task, '=============FINIHSED=============')
    updateLastRunDate(task)
    updateTaskState(task, 'waiting')

def updateLastRunDate(task):
    date = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    db.query('UPDATE \'143_tasks\' SET \'last_run\' = \''+date+'\' WHERE id = '+str(task))

def updateTaskState(task, state):
    db.query('UPDATE \'143_tasks\' SET \'state\' = \''+state+'\' WHERE id = '+str(task))

while True:
    query = db.query('SELECT c.path AS source, '
                     'd.path AS dest, '
                     'a.schedule, '
                     'a.id, '
                     'a.last_run, '
                     'c.system AS source_fs, '
                     'd.system AS dest_fs, '
                     'c.host AS host, '
                     'c.username AS user, '
                     'c.password AS password, '
                     'a.state, '
                     'b.compression, '
                     'a.backuptyp as type '
                     'FROM \'143_tasks\' AS a '
                     'JOIN \'143_backups\' AS b ON a.backupid = b.id '
                     'JOIN \'143_pool\' AS c ON b.pool_src = c.id '
                     'JOIN \'143_pool\' AS d ON b.pool_dst = d.id')

    tasks = query.fetchall()
    for task in tasks:
        # Import correct script for filesystem
        if task['source_fs'] == 'ftp':
            from bin.both.fs_ftp import Backup
        elif task['source_fs'] == 'sftp':
            from bin.both.fs_sftp import Backup
        else:
            from bin.both.fs_local import Backup

        if task['state'] is not 'running':
            if task['last_run'] is not None:
                schedule = CronTab(task['schedule'])
                diff = schedule.next()
                if diff < threshold:
                    print('Starting normal for task ' + str(task['id']))
                    startBackup(task['id'])
                    backup = Backup(task)
                    backup.backup()
                    finishBackup(task['id'])
                    print('Backup for task ' + str(task['id']) + ' created')

            # Start backup immediately if never ran before
            else:
                print('Starting immediately for task ' + str(task['id']))
                startBackup(task['id'])
                backup = Backup(task)
                backup.backup()
                finishBackup(task['id'])
                print('Backup for task ' + str(task['id']) + ' created')
        else:
            print('Backup already running')

    time.sleep(10)