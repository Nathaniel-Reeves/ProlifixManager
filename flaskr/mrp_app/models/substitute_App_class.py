class App:
    def __init__(self):
        self.HOST = '192.168.1.42'
        self.PORT = 33060
        self.USER = 'client'
        self.PASSWORD = 'clientPassword5!'
        self.config = {
            "DB_CREDENTIALS": {
                'host': self.HOST,
                'port': self.PORT,
                'user': self.USER,
                'password': self.PASSWORD
            },
            "UPLOAD_FOLDER": '/mnt/c/Users/Nathaniel Reeves/Documents/uploads'
        }
