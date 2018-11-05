import os
import zipfile
import tarfile
import shutil
from bin.both.dbcon import dbmanager
from datetime import datetime
from bin.both.hashing import filechanged


class Backup:
    def __init__(self, task):
        self.db = dbmanager()
        self.task = task

    def backup(self):
        # Change pwd for easier tree walking
        os.chdir(self.task['source'])

        # Checking compression mode
        if self.task['compression'] == 'zip':
            # Check if destination folder exists
            if not os.path.isdir(self.task['dest']):
                raise Exception('Destination directory does not exist')

            # Calculate name for backup file
            date = str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
            destination = self.task['dest'] + os.sep + self.task['type'] + '_' + date + '.zip'

            # Initialize zip file for backup
            zipf = zipfile.ZipFile(destination, "w")

            # Walk directory
            for subdir, dirs, files in os.walk("."):
                for file in files:
                    if self.task['type'] == 'incremental':
                        # Check if file hash has changed (only for incremental backup)
                        if filechanged(self.task, os.path.join(self.task['source'], subdir), file, date,
                                       self.task['last_run']):
                            print('File ' + file + ' has changed. Backing up.')
                            self.db.log(self.task['id'], "Created backup of file " + file)
                            # Write file to zip
                            zipf.write(os.path.join(subdir, file))

                    elif self.task['type'] == 'differential':
                        # Check if file hash has changed (only for incremental backup)
                        if filechanged(self.task, os.path.join(self.task['source'], subdir), file, date,
                                       self.task['last_full_run']):
                            print('File ' + file + ' has changed. Backing up.')
                            self.db.log(self.task['id'], "Created backup of file " + file)
                            # Write file to zip
                            zipf.write(os.path.join(subdir, file))

                    elif self.task['type'] == 'full':
                        # Check if file hash has changed (only for incremental backup)
                        if filechanged(self.task, os.path.join(self.task['source'], subdir), file, date,
                                       self.task['last_run']):
                            print('File ' + file + ' has changed. Backing up.')
                            self.db.log(self.task['id'], "Created backup of file " + file)
                            # Write file to zip
                            zipf.write(os.path.join(subdir, file))

            data = {
                'task': self.task['id'],
                'date': date,
                'status': 'ok',
                'path': destination
            }

        elif self.task['compression'] == 'none':
            # Check if destination folder exists
            if not os.path.isdir(self.task['dest']):
                raise Exception('Destination directory does not exist!')

            # Calculate name for backup folder
            date = str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
            destination = self.task['dest'] + os.sep + self.task['type'] + '_' + date

            # Create backup folder
            os.mkdir(destination)

            for subdir, dirs, files in os.walk("."):
                for dir in dirs:
                    self.db.log(self.task['id'], "Created backup of folder " + dir)
                    # Create folder in new directory
                    os.mkdir(os.path.join(destination, dir))

                for file in files:
                    if self.task['type'] == 'incremental':
                        # Check if file hash has changed (only for incremental backup)
                        if filechanged(self.task, os.path.join(self.task['source'], subdir), file, date,
                                       self.task['last_run']):
                            print('File ' + file + ' has changed. Backing up.')
                            self.db.log(self.task['id'], "Created backup of file " + file)
                            # Copy file to new directory (preserve metadata)
                            shutil.copy2(os.path.join(subdir, file), os.path.join(destination, subdir))

                    elif self.task['type'] == 'differential':
                        # Check if file hash has changed (only for incremental backup)
                        if filechanged(self.task, os.path.join(self.task['source'], subdir), file, date,
                                       self.task['last_full_run']):
                            print('File ' + file + ' has changed. Backing up.')
                            self.db.log(self.task['id'], "Created backup of file " + file)
                            # Copy file to new directory (preserve metadata)
                            shutil.copy2(os.path.join(subdir, file), os.path.join(destination, subdir))

                    elif self.task['type'] == 'full':
                        # Check if file hash has changed (only for incremental backup)
                        if filechanged(self.task, os.path.join(self.task['source'], subdir), file, date,
                                       self.task['last_run']):
                            print('File ' + file + ' has changed. Backing up.')
                            self.db.log(self.task['id'], "Created backup of file " + file)
                            # Copy file to new directory (preserve metadata)
                            shutil.copy2(os.path.join(subdir, file), os.path.join(destination, subdir))

            data = {
                'task': self.task['id'],
                'date': date,
                'status': 'ok',
                'path': destination
            }

        elif self.task['compression'] == 'tar':
            # Check if destination folder exists
            if not os.path.isdir(self.task['dest']):
                raise Exception('Destination directory does not exist')

            # Calculate name for backup file
            date = str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
            destination = self.task['dest'] + os.sep + self.task['type'] + '_' + date + '.tar.gz'

            # Initialize tar file for backup
            tarf = tarfile.open(destination, "w:gz")

            # Walk directory
            for subdir, dirs, files in os.walk("."):
                for file in files:
                    if self.task['type'] == 'incremental':
                        # Check if file hash has changed (only for incremental backup)
                        if filechanged(self.task, os.path.join(self.task['source'], subdir), file, date,
                                       self.task['last_run']):
                            print('File ' + file + ' has changed. Backing up.')
                            self.db.log(self.task['id'], "Created backup of file " + file)
                            # Write file to tar
                            tarf.add(os.path.join(subdir, file))

                    elif self.task['type'] == 'differential':
                        # Check if file hash has changed (only for incremental backup)
                        if filechanged(self.task, os.path.join(self.task['source'], subdir), file, date,
                                       self.task['last_full_run']):
                            print('File ' + file + ' has changed. Backing up.')
                            self.db.log(self.task['id'], "Created backup of file " + file)
                            # Write file to tar
                            tarf.add(os.path.join(subdir, file))

                    elif self.task['type'] == 'full':
                        # Check if file hash has changed (only for incremental backup)
                        if filechanged(self.task, os.path.join(self.task['source'], subdir), file, date,
                                       self.task['last_run']):
                            print('File ' + file + ' has changed. Backing up.')
                            self.db.log(self.task['id'], "Created backup of file " + file)
                            # Write file to tar
                            tarf.add(os.path.join(subdir, file))

            tarf.close()

            data = {
                'task': self.task['id'],
                'date': date,
                'status': 'ok',
                'path': destination
            }

        else:
            # No valid compression mode detected
            raise Exception('Could not determine compression mode')

        backupid = self.task['backupid']
        query = f"UPDATE '143_backups' SET last_full_run = '{date}' WHERE id = {backupid}"
        if self.task['type'] == 'full':
            print('Created full backup')
            self.db.query(query)

        elif self.task['type'] == 'incremental' or self.task['type'] == 'differential':
            print(self.task['last_run'])
            if self.task['last_run'] is None:
                print('Backup ran never before')
                self.db.query(query)

        return data
