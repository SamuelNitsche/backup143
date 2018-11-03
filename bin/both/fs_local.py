import os
import zipfile
import shutil
from bin.both.dbcon import dbmanager
from datetime import datetime
from bin.both.hashing import filechanged


class Backup:
    def __init__(self, task):
        self.db = dbmanager()
        self.task = task

    def backup(self):
        raise Exception('test')
        # Change pwd for easier tree walking
        os.chdir(self.task['source'])
        # Checking compression mode
        if self.task['compression'] == 'zip':
            # Check if destination folder exists
            if not os.path.isdir(self.task['dest']):
                raise Exception('Destination directory does not exist')

            # Calculate name for backup file
            destination = self.task['dest'] + os.sep + str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S')) + '.zip'
            # Initialize zip file for backup
            zipf = zipfile.ZipFile(destination, "w")
            # Walk directory
            for subdir, dirs, files in os.walk("."):
                for dir in dirs:
                    path = os.path.join(subdir, dir)
                    self.db.log(self.task['id'], "Created backup of folder " + dir)
                    # Write folder to zip file
                    zipf.write(path)

                for file in files:
                    # Check if file hash has changed (only for incremental backup)
                    if filechanged(self.task, os.path.join(self.task['source'], subdir), file):
                        print('File ' + file + ' has changed. Backing up.')
                        self.db.log(self.task['id'], "Created backup of file " + file)
                        # Write file to zip
                        zipf.write(os.path.join(subdir, file))

        elif self.task['compression'] == 'none':
            # Check if destination folder exists
            if not os.path.isdir(self.task['dest']):
                raise Exception('Destination directory does not exist!')

            # Calculate name for backup folder
            destination = self.task['dest'] + os.sep + str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
            # Create backup folder
            os.mkdir(destination)
            for subdir, dirs, files in os.walk("."):
                for dir in dirs:
                    self.db.log(self.task['id'], "Created backup of folder " + dir)
                    # Create folder in new directory
                    os.mkdir(os.path.join(destination, dir))

                for file in files:
                    # Check if file hash has changed (only for incremental backup)
                    if filechanged(self.task, os.path.join(self.task['source'], subdir), file):
                        self.db.log(self.task['id'], "Created backup of file " + file)
                        # Copy file to new directory (preserve metadata)
                        shutil.copy2(os.path.join(subdir, file), os.path.join(destination, subdir))

        else:
            # No valid compression mode detected
            raise Exception('Could not determine compression mode')