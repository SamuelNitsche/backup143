import os
import zipfile
import tarfile
import shutil
from bin.both.dbcon import dbmanager
from datetime import datetime
from bin.both.hashing import filechanged


class Restore:
    def __init__(self, task):
        self.db = dbmanager()
        self.task = task
        self.restores = []

    def restore(self):
        # Get Backuptyp from selected Backupfile
        qry = self.db.query("SELECT t2.backuptyp FROM '143_tasks' t1 INNER JOIN '143_backupfiles' bf ON t1.backupfilesid = bf.id INNER JOIN '143_tasks' t2 ON bf.taskid = t2.id WHERE t1.id = '"+str(self.task['id'])+"';")
        result = qry.fetchone()
        # Create a Array with backupfiles for this Restore
        print(result[0])
        if result[0] == "full":
            self.restores.append(self.task['backupfilesid'])
        if result[0] == "incremental":
            self.incrementalids()
        if result[0] == "differential":
            self.differentialids()
        
        for restore in self.restores:
            qry = self.db.query("SELECT path FROM '143_backupfiles' WHERE id = '"+str(restore)+"';")
            backupfilespath = qry.fetchone()
            # Change pwd for easier tree walking
            os.chdir(self.task['source'])
            # Checking compression mode
            if self.task['compression'] == 'zip':
                # Check if destination folder exists
                if not os.path.isdir(self.task['dest']):
                    raise Exception('Destination directory does not exist')
                if not os.path.isdir(self.task['source']):
                    raise Exception('Source directory does not exist!')

                # extract zipfile
                zipf = zipfile.ZipFile(backupfilespath[0], "r")
                zipf.extractall()

            elif self.task['compression'] == 'none':
                # Check if destination folder exists
                if not os.path.isdir(self.task['dest']):
                    raise Exception('Destination directory does not exist!')
                if not os.path.isdir(self.task['source']):
                    raise Exception('Source directory does not exist!')

                # Change pwd for easier tree walking
                os.chdir(backupfilespath[0])
                # Walk Files in Backup Folder and Copy to Source Folder
                for subdir, dirs, files in os.walk("."):
                    for dir in dirs:
                        self.db.log(self.task['id'], "Restored Folder " + dir)
                        # Create folder in new directory
                        if not os.path.isdir(os.path.join(self.task['source'], dir)):
                            os.mkdir(os.path.join(self.task['source'], dir))

                    for file in files:
                        # Check if file hash has changed (only for incremental backup)
                        self.db.log(self.task['id'], "Restored file " + file)
                        # Copy file to new directory (preserve metadata)
                        if os.path.isfile(os.path.join(self.task['source'], subdir)):
                            os.remove(os.path.join(self.task['source'], subdir))
                        shutil.copy2(os.path.join(subdir, file), os.path.join(self.task['source'], subdir))
        
            elif self.task['compression'] == 'tar':
                # Check if destination folder exists
                if not os.path.isdir(self.task['dest']):
                    raise Exception('Destination directory does not exist')
                if not os.path.isdir(self.task['source']):
                    raise Exception('Source directory does not exist!')

                # extract zipfile
                tarf = tarfile.open(backupfilespath[0], "r:gz")
                tarf.extractall()

                tarf.close()
                
            else:
                # No valid compression mode detected
                raise Exception('Could not determine compression mode')

        date = str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        data = {
            'task': self.task['id'],
            'date': date,
            'status': 'ok',
            'path': self.task['source']
        }
                
        return data
            
    def incrementalids(self):
        qry = self.db.query("SELECT bf.id, t.backuptyp FROM '143_backups' b INNER JOIN '143_tasks' t ON b.id = t.backupid INNER JOIN '143_backupfiles' bf ON t.id = bf.taskid WHERE b.id="+str(self.task['backupid'])+" AND bf.id <= "+str(self.task['backupfilesid'])+" AND t.backuptyp = 'incremental' OR b.id="+str(self.task['backupid'])+" AND bf.id <= "+str(self.task['backupfilesid'])+" AND t.backuptyp = 'full' ORDER by bf.id DESC;")
        for row in qry:
            self.restores.append(row[0])
            if row[1] == "full":
                self.restores.append(row[0])
                return
    def differentialids(self):
        qry = self.db.query("SELECT bf.id, t.backuptyp FROM '143_backups' b INNER JOIN '143_tasks' t ON b.id = t.backupid INNER JOIN '143_backupfiles' bf ON t.id = bf.taskid WHERE b.id="+str(self.task['backupid'])+" AND bf.id <= "+str(self.task['backupfilesid'])+" AND t.backuptyp = 'differential' OR b.id="+str(self.task['backupid'])+" AND bf.id <= "+str(self.task['backupfilesid'])+" AND t.backuptyp = 'full' ORDER by bf.id DESC;")
        for row in qry:
            self.restores.append(row[0])
            if row[1] == "full":
                self.restores.append(row[0])
                return