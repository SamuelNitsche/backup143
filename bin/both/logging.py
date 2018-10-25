import os
from datetime import datetime
import zipfile

class LogginSystem(object):

    def __init__(self, filename):
        self.filename = filename
        script_dir = os.path.dirname(__file__)
        rel_path = "../../log"
        log_folder_path = os.path.join(script_dir, rel_path)
        if not os.path.exists(log_folder_path):
            os.makedirs(log_folder_path)
        if not os.path.isfile(log_folder_path + "/"+self.filename+".log"):
            file = open(log_folder_path + "/"+self.filename+".log", "w+")
            file.close()

    def write(self, message):
        script_dir = os.path.dirname(__file__)
        rel_path = "../../log"
        log_folder_path = os.path.join(script_dir, rel_path)
        file = open(log_folder_path + "/"+self.filename+".log", 'a')
        dt = datetime.now()
        file.write('[' + dt.strftime('%d.%m.%Y %H:%M:%S') + ']  ' + message + "\n")
        file.close()
        if os.path.getsize(log_folder_path + "/"+self.filename+".log") > 32000:
            if os.path.exists(log_folder_path + "/"+self.filename+".5.zip"):
                os.remove(log_folder_path + "/"+self.filename+".5.zip")
            if os.path.exists(log_folder_path + "/"+self.filename+".4.zip"):
                os.rename(log_folder_path + "/"+self.filename+".4.zip", log_folder_path + "/"+self.filename+".5.zip")
            if os.path.exists(log_folder_path + "/"+self.filename+".3.zip"):
                os.rename(log_folder_path + "/"+self.filename+".3.zip", log_folder_path + "/"+self.filename+".4.zip")
            if os.path.exists(log_folder_path + "/"+self.filename+".2.zip"):
                os.rename(log_folder_path + "/"+self.filename+".2.zip", log_folder_path + "/"+self.filename+".3.zip")
            if os.path.exists(log_folder_path + "/"+self.filename+".1.zip"):
                os.rename(log_folder_path + "/"+self.filename+".1.zip", log_folder_path + "/"+self.filename+".2.zip")
            zf = zipfile.ZipFile(log_folder_path + "/"+self.filename+".1.zip", "w")
            zf.write(log_folder_path + "/"+self.filename+".log", self.filename+".log")
            zf.close()
            os.remove(log_folder_path + "/"+self.filename+".log")