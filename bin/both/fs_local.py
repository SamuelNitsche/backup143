import os
import zipfile
from bin.both.dbcon import dbmanager
from datetime import datetime

class Backup:
    def __init__(self, source, dest, task):
        self.db = dbmanager()
        self.source = source
        self.dest = dest
        self.task = task

    def backup(self):
        self.updateTaskState('running')
        zipf = zipfile.ZipFile(self.dest, "w")
        os.chdir(self.source)
        for subdir, dirs, files in os.walk("."):
            for dir in dirs:
                path = os.path.join(subdir, dir)
                self.db.log(self.task, "Created backup of folder " + dir)
                zipf.write(path)
                # print('Backed up folder '+dir)

            for file in files:
                self.db.log(self.task, "Created backup of file " + file)
                zipf.write(os.path.join(subdir, file))
                # print('Backed up file ' + file)

        self.finishBackup()
        print("All done!")

    def finishBackup(self):
        self.db.log(self.task, '=============FINIHSED=============')
        self.updateLastRunDate()
        self.updateTaskState('waiting')

    def updateLastRunDate(self):
        date = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.db.query('UPDATE \'143_tasks\' SET \'last_run\' = \''+date+'\' WHERE id = '+str(self.task))

    def updateTaskState(self, state):
        self.db.query('UPDATE \'143_tasks\' SET \'state\' = \''+state+'\' WHERE id = '+str(self.task))
