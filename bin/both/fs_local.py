import os
import zipfile
from bin.both.dbcon import dbmanager

class Backup:
    def __init__(self, task):
        self.db = dbmanager()
        self.task = task

    def backup(self):
        zipf = zipfile.ZipFile(self.task['dest'], "w")
        os.chdir(self.task['source'])
        for subdir, dirs, files in os.walk("."):
            for dir in dirs:
                path = os.path.join(subdir, dir)
                self.db.log(self.task['id'], "Created backup of folder " + dir)
                zipf.write(path)

            for file in files:
                self.db.log(self.task['id'], "Created backup of file " + file)
                zipf.write(os.path.join(subdir, file))