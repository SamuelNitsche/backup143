import os
import zipfile
import shutil
from bin.both.dbcon import dbmanager
from datetime import datetime
from bin.both.compare import file_changed


class Backup:
    def __init__(self, task):
        self.db = dbmanager()
        self.task = task

    def backup(self):
        os.chdir(self.task['source'])
        if self.task['compression'] == 'zip':
            if not os.path.isdir(self.task['dest']):
                raise Exception('Destination directory does not exist')

            oldpath = os.path.join(self.task['dest'], str(self.task['last_run']).replace('_', ' ').replace('-', ':'))
            print(oldpath)
            if os.path.exists(oldpath):
                print('Old backup exists')
            else:
                print('Old backup does not exist')

            destination = self.task['dest'] + os.sep + str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S')) + '.zip'
            zipf = zipfile.ZipFile(destination, "w")
            for subdir, dirs, files in os.walk("."):
                for dir in dirs:
                    path = os.path.join(subdir, dir)
                    self.db.log(self.task['id'], "Created backup of folder " + dir)
                    zipf.write(path)

                for file in files:
                    # if file_changed(oldfile, file):
                    self.db.log(self.task['id'], "Created backup of file " + file)
                    zipf.write(os.path.join(subdir, file))

        elif self.task['compression'] == 'none':
            if not os.path.isdir(self.task['dest']):
                raise Exception('Destination directory does not exist!')

            destination = self.task['dest'] + os.sep + str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
            os.mkdir(destination)
            for subdir, dirs, files in os.walk("."):
                for dir in dirs:
                    self.db.log(self.task['id'], "Created backup of folder " + dir)
                    os.mkdir(os.path.join(destination, dir))

                for file in files:
                    self.db.log(self.task['id'], "Created backup of file " + file)
                    shutil.copy(os.path.join(subdir, file), os.path.join(destination, subdir))

        else:
            raise Exception('Could not determine compression mode')