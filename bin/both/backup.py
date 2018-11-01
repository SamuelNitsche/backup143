from bin.both.fs_local import Backup
from bin.both.dbcon import dbmanager
from crontab import CronTab
from datetime import datetime
import time

db = dbmanager()

while True:
    query = db.query('SELECT c.path, d.path, a.schedule, a.id, a.last_run FROM \'143_tasks\' AS a '
                     'JOIN \'143_backups\' AS b ON a.backupid = b.id '
                     'JOIN \'143_pool\' AS c ON b.pool_src = c.id '
                     'JOIN \'143_pool\' AS d ON b.pool_dst = d.id')

    tasks = query.fetchall()
    for task in tasks:
        print(task[4])
        last_run = datetime.strftime(task[4], '%Y-%m-%y %H:%M:%S')
        print(last_run)
        # schedule = CronTab(task[2])
        # diff = schedule.next()
        # if diff < 0:
        #     backup = Backup(task[0], task[1])
        #     backup.backup()
        #     print('Backup for task ' + task[3] + ' created')

    print('Backups created')

    time.sleep(1)