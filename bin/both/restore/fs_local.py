import os
import zipfile
import shutil
from bin.both.dbcon import dbmanager
from datetime import datetime
from bin.both.hashing import filechanged


class Restore:
    def __init__(self, task):
        self.db = dbmanager()
        self.task = task

    def restore(self):
        # Change pwd for easier tree walking
        os.chdir(self.task['source'])
        # Checking compression mode
        if self.task['compression'] == 'zip':
            # Check if destination folder exists
            if not os.path.isdir(self.task['dest']):
                raise Exception('Destination directory does not exist')
            if not os.path.isdir(self.task['source']):
                raise Exception('Source directory does not exist!')

            # generate backup zipfile name
            destination = self.task['dest'] + os.sep + self.task['backupfiledate'] + '.zip'
            # extract zipfile
            zipf = zipfile.ZipFile(destination, "r")
            zipf.extractall()

            return {
                'task': self.task['id'],
                'date': date,
                'status': 'ok',
                'path': self.task['source']
            }

        elif self.task['compression'] == 'none':
            # Check if destination folder exists
            if not os.path.isdir(self.task['dest']):
                raise Exception('Destination directory does not exist!')
            if not os.path.isdir(self.task['source']):
                raise Exception('Source directory does not exist!')

            # generate backup folder name
            destination = self.task['dest'] + os.sep + self.task['backupfiledate']
            # Change pwd for easier tree walking
            os.chdir(destination)
            # Walk Files in Backup Folder and Copy to Source Folder
            for subdir, dirs, files in os.walk("."):
                for dir in dirs:
                    self.db.log(self.task['id'], "Restored Folder " + dir)
                    # Create folder in new directory
                    os.mkdir(os.path.join(self.task['source'], dir))

                for file in files:
                    # Check if file hash has changed (only for incremental backup)
                    self.db.log(self.task['id'], "Restored file " + file)
                    # Copy file to new directory (preserve metadata)
                    shutil.copy2(os.path.join(subdir, file), os.path.join(self.task['source'], subdir))

            return {
                'task': self.task['id'],
                'date': date,
                'status': 'ok',
                'path': self.task['source']
            }

        else:
            # No valid compression mode detected
            raise Exception('Could not determine compression mode')
