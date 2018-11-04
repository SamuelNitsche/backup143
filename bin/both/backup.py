from bin.both.dbcon import dbmanager
from crontab import CronTab
from datetime import datetime
import time
from bin.both.utils import recordbackupfile

db = dbmanager(True)
threshold = 10


def startbackup(task):
    db.log(task, '=============STARTING=============')
    updatetaskstate(task, 'running')


def finishbackup(data):
    db.log(data['task'], '=============FINIHSED=============')
    updatelastrundate(data['task'])
    updatetaskstate(data['task'], 'waiting')
    recordbackupfile(data['task'], data['date'], data['status'], data['path'])


def backupfailed(task, err):
    db.log(task, '=============FAILED=============')
    db.log(task, f"{err}".replace("'", '"'))
    updatetaskstate(task, 'failed')
    updatelastrundate(task)



def updatelastrundate(task):
    date = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    db.query('UPDATE \'143_tasks\' SET \'last_run\' = \'' + date + '\' WHERE id = ' + str(task))


def updatetaskstate(task, state):
    db.query('UPDATE \'143_tasks\' SET \'state\' = \'' + state + '\' WHERE id = ' + str(task))


while True:
    # Fetch all tasks from database
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

        # Check if task is running
        if task['state'] is not 'running':
            # Calculate start date from last run
            if task['last_run'] is not None:
                schedule = CronTab(task['schedule'])
                diff = schedule.next()
                # Start backup if cron matches
                if diff < threshold:
                    print('Starting normal for task ' + str(task['id']))
                    startbackup(task['id'])
                    # Initialize backup task
                    backup = Backup(task)
                    # Start backup
                    # try:
                    result = backup.backup()
                    finishbackup(result)
                    print('Backup for task ' + str(task['id']) + ' created')
                    # except Exception as e:
                    #     backupfailed(task['id'], e)
                    #     print('Backup failed')
                    #     print(e)

            # Start backup immediately if never ran before
            else:
                print('Starting immediately for task ' + str(task['id']))
                startbackup(task['id'])
                # Initialize backup task
                backup = Backup(task)
                # Start backup
                try:
                    result = backup.backup()
                    finishbackup(result)
                    print('Backup for task ' + str(task['id']) + ' created')
                except Exception as e:
                    backupfailed(task['id'], e)
                    print('Backup failed')
                    print(e)
        else:
            print('Backup already running')

    time.sleep(10)
