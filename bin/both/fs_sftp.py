from bin.both.dbcon import dbmanager
import pysftp as sftp
import os
import shutil
import tempfile
import zipfile

class Backup:
    def __init__(self, task):
        self.db = dbmanager()
        self.task = task
        self.conn = sftp.Connection(host=task['host'], username=task['user'], password=task['password'])

    def backup(self):
        self.conn.chdir(self.task['source'])
        if os.path.isdir(self.task['dest']):
            self.conn.get_r('.', self.task['dest'])
        elif str(self.task['dest']).endswith('.zip'):
            path = tempfile.mkdtemp()
            self.conn.get_r('.', path)
            os.chdir(path)
            zipf = zipfile.ZipFile(self.task['dest'], "w")
            for subdir, dirs, files in os.walk("."):
                for dir in dirs:
                    path = os.path.join(subdir, dir)
                    self.db.log(self.task['id'], "Created backup of folder " + dir)
                    zipf.write(path)

                for file in files:
                    self.db.log(self.task['id'], "Created backup of file " + file)
                    zipf.write(os.path.join(subdir, file))

            shutil.rmtree(path)
        else:
            raise Exception('Could not determine backup destination path')

    def __exit__(self):
        self.conn.close()