class process():
    def start(self):
        import bin.both.webserver
        import bin.both.api
        import bin.both.backup.backup
        while True:
            '''thread = threading.Thread(target=self.run, args=())
            thread.daemon = True
            thread.start()'''