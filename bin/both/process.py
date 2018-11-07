import time

class process():
    def start(self):
        import bin.both.webserver
        import bin.both.api
        from bin.both.backup.backup import checkforbackups
        from bin.both.restore.restore import checkforrestores
        while True:
            checkforbackups()
            checkforrestores()
            time.sleep(30)