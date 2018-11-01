import os
import zipfile
from bin.both.dbcon import dbmanager

class Backup:
    def __init__(self, source, dest, task):
        self.db = dbmanager()
        self.source = source
        self.dest = dest
        self.task = task

    def backup(self):
        self.db.query('UPDATE ')
        zipf = zipfile.ZipFile(self.dest, "w")
        os.chdir(self.source)
        for subdir, dirs, files in os.walk("."):
            for dir in dirs:
                path = os.path.join(subdir, dir)
                self.db.log(1, "Created backup of folder " + dir)
                zipf.write(path)

            for file in files:
                self.db.log(1, "Created backup of file " + file)
                zipf.write(os.path.join(subdir, file))

        self.db.log(1, '=============FINIHSED=============')
        print("All done!")