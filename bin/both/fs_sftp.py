from bin.both.dbcon import dbmanager
import pysftp as sftp
import os
import shutil
import tempfile
import zipfile
from datetime import datetime


class Backup:
    def __init__(self, task):
        self.db = dbmanager()
        self.task = task
        self.conn = sftp.Connection(host=task['host'], username=task['user'], password=task['password'])

    def backup(self):
        self.conn.chdir(self.task['source'])

        if self.task['compression'] == 'zip':
            if not os.path.isdir(self.task['dest']):
                raise Exception('Destination directory does not exist')

            destination = self.task['dest'] + os.sep + str(datetime.now()) + '.zip'
            path = tempfile.mkdtemp()
            self.conn.get_r('.', path)
            os.chdir(path)
            zipf = zipfile.ZipFile(destination, "w")
            for subdir, dirs, files in os.walk("."):
                for dir in dirs:
                    path = os.path.join(subdir, dir)
                    self.db.log(self.task['id'], "Created backup of folder " + dir)
                    zipf.write(path)

                for file in files:
                    self.db.log(self.task['id'], "Created backup of file " + file)
                    zipf.write(os.path.join(subdir, file))

            shutil.rmtree(path)

        elif self.task['compression'] == 'none':
            if not os.path.isdir(self.task['dest']):
                raise Exception('Destination directory does not exist')

            destination = self.task['dest'] + os.sep + str(datetime.now())
            os.mkdir(destination)
            path = tempfile.mkdtemp()
            self.conn.get_r('.', path)
            os.chdir(path)
            for subdir, dirs, files in os.walk("."):
                for dir in dirs:
                    self.db.log(self.task['id'], "Created backup of folder " + dir)
                    os.mkdir(os.path.join(destination, dir))

                for file in files:
                    self.db.log(self.task['id'], "Created backup of file " + file)
                    shutil.copy(os.path.join(subdir, file), os.path.join(destination, subdir))

        else:
            raise Exception('Could not determine backup destination path')

    def __exit__(self):
        self.conn.close()
