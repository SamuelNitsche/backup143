from bin.both.fs_local import Backup
from bin.both.dbcon import dbmanager
from crontab import CronTab
from datetime import datetime
import time

db = dbmanager()
threshold = 10

while True:
    query = db.query('SELECT c.path, d.path, a.schedule, a.id, a.last_run FROM \'143_tasks\' AS a '
                     'JOIN \'143_backups\' AS b ON a.backupid = b.id '
                     'JOIN \'143_pool\' AS c ON b.pool_src = c.id '
                     'JOIN \'143_pool\' AS d ON b.pool_dst = d.id')

    tasks = query.fetchall()
    for task in tasks:
        src = task[0]
        dst = task[1]
        schedule = task[2]
        task_id = task[3]
        last_run = task[4]

        if not last_run == None:
            schedule = CronTab(schedule)
            diff = schedule.next()
            if diff < threshold:
                backup = Backup(src, dst, task_id)
                backup.backup()
                print('Backup for task ' + str(task_id) + ' created')
        else:
            backup = Backup(src, dst, task_id)
            backup.backup()
            print('Backup for task ' + str(task_id) + ' created')

    # print('Backups created')

    time.sleep(10)