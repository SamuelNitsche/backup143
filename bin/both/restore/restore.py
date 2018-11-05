from bin.both.dbcon import dbmanager
from datetime import datetime
import time
import _thread

db = dbmanager(True)

def startrestore(task):
    db.log(task, '=============STARTING=============')
    updatetaskstate(task, 'running')


def finishrestore(data):
    db.log(data['task'], '=============FINIHSED=============')
    updatelastrundate(data['task'])
    updatetaskstate(data['task'], 'finished')


def restorefailed(task, err):
    db.log(task, '=============FAILED=============')
    db.log(task, f"{err}".replace("'", '"'))
    updatetaskstate(task, 'failed')
    updatelastrundate(task)
    
    
def updatelastrundate(task):
    date = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    db.query('UPDATE \'143_tasks\' SET \'last_run\' = \'' + date + '\' WHERE id = ' + str(task))
    
    
def updatetaskstate(task, state):
    db.query('UPDATE \'143_tasks\' SET \'state\' = \'' + state + '\' WHERE id = ' + str(task))
    
    
def checkforrestores():
    db = dbmanager(True)
    while True:
        # Fetch all tasks from database
        query = db.query('SELECT c.path AS source, '
                         'd.path AS dest, '
                         'a.schedule, '
                         'a.id, '
                         'a.last_run, '
                         'a.backupfilesid, '
                         'a.backupid, '
                         'c.system AS source_fs, '
                         'd.system AS dest_fs, '
                         'c.host AS host, '
                         'c.username AS user, '
                         'c.password AS password, '
                         'a.state, '
                         'b.compression, '
                         'a.backuptyp as type, '
                         'b.last_full_run, '
                         'a.action '
                         'FROM \'143_tasks\' AS a '
                         'JOIN \'143_backups\' AS b ON a.backupid = b.id '
                         'JOIN \'143_pool\' AS c ON b.pool_src = c.id '
                         'JOIN \'143_pool\' AS d ON b.pool_dst = d.id '
                         'WHERE a.action = \'restore\'')

        tasks = query.fetchall()
        for task in tasks:
            # Import correct script for filesystem
            if task['source_fs'] == 'ftp':
                from bin.both.restore.fs_ftp import Restore
            elif task['source_fs'] == 'sftp':
                from bin.both.restore.fs_sftp import Restore
            else:
                from bin.both.restore.fs_local import Restore

            # Check if task is running and not finished
            if task['state'] != 'finished' and task['state'] != 'running':
                print('Starting normal for task ' + str(task['id']))
                startrestore(task['id'])
                # Initialize restore task
                restore = Restore(task)
                # Start restore
                #try:
                result = restore.restore()
                finishrestore(result)
                print('Restore for task ' + str(task['id']) + ' created')
                #except Exception as e:
                #    restorefailed(task['id'], e)
                #    print('Restore failed')
                #    print(e)
        time.sleep(10)
        
_thread.start_new_thread(checkforrestores, ())