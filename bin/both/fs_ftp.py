from bin.both.dbcon import dbmanager
import ftplib

class Backup:
    def __init__(self, source, dest, task):
        self.db = dbmanager()
        self.source = source
        self.dest = dest
        self.task = task

    def backup(self):





    #     self.finishBackup()
    #     print("All done!")
    #
    # def finishBackup(self):
    #     self.db.log(self.task, '=============FINIHSED=============')
    #     self.updateLastRunDate()
    #     self.updateTaskState('waiting')
    #
    # def updateLastRunDate(self):
    #     date = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    #     self.db.query('UPDATE \'143_tasks\' SET \'last_run\' = \''+date+'\' WHERE id = '+str(self.task))
    #
    # def updateTaskState(self, state):
    #     self.db.query('UPDATE \'143_tasks\' SET \'state\' = \''+state+'\' WHERE id = '+str(self.task))
