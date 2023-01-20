class Config(object):
    """Base Configuration Settings for Flask App."""
    # Flask Config
    DEBUG = True
    
    # import secrets
    # secret_key = secrets.token_urlsafe(64)
    SECRET_KEY = 'NiHuLSNTFA4RsvtbBmCcDDJXJxbAnw13MRwJsL9WdNT9Jf8_hrQ0hMKroq_96ewipByaBqGRfSuhMQqSn3cArg'
    TESTING = True

    # String Date Formatting
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    # Database Config
    HOST = 'localhost'
    PORT = 33060
    USER = 'client'
    PASSWORD = 'clientPassword5!'

    @property
    def DB_CREDENTIALS(self):  # Note: all caps
        return {
            'host': self.HOST,
            'port': self.PORT,
            'user': self.USER,
            'password': self.PASSWORD
        }
    
    @property
    def UPLOAD_FOLDER(self):  # Note: all caps
        return self.UPLOAD_FOLDER

    EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

    @property
    def ALLOWED_EXTENSIONS(self):  # Note: all caps
        return self.EXTENSIONS

    # Config Settings Message
    MESSAGE = "Default Config"

    @property
    def MESSAGE(self):  # Note: all caps
        return self.MESSAGE


class Work_Laptop_Config(Config):
    """Work Laptop Config Settings for Flask App"""
    MESSAGE = "Work Laptop Config"

    # Database Connection
    HOST = '192.168.1.42'
    PORT = 33060
    USER = 'client'
    PASSWORD = 'clientPassword5!'

    # File Saving
    UPLOAD_FOLDER = '/mnt/c/Users/Nathaniel Reeves/Documents/uploads'


class Home_PC_Config(Config):
    """Home PC Config Settings for Flask App"""
    MESSAGE = "Home PC Config"

    # Database Connection
    HOST = 'localhost'
    PORT = 13307
    USER = 'client'
    PASSWORD = 'clientPassword5!'

    # File Saving
    UPLOAD_FOLDER = '/mnt/s/uploads'


class School_Laptop_Config(Config):
    """School Laptop Config Settings for Flask App"""
    MESSAGE = "School Laptop Config"

    # Database Connection
    HOST = 'localhost'
    PORT = 33060
    USER = 'client'
    PASSWORD = 'clientPassword5!'

    # File Saving
    UPLOAD_FOLDER = '/mnt/c/uploads'


class Pi_Server_Config(Config):
    """Pi Server Config Settings for Flask App"""
    MESSAGE = "Pi Server Config"

    # Database Connection
    HOST = '192.168.1.42'
    PORT = 33060
    USER = 'client'
    PASSWORD = 'clientPassword5!'

    # File Saving
    UPLOAD_FOLDER = '/home/nreeves/uploads'
