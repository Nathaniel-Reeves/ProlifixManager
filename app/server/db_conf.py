class Config:
    """Base Configuration Settings for Flask App."""
    def __init__(self):
        # Connection Credentials Message
        self.MESSAGE = 'Default Database Connection Credentials'
        
        # import secrets
        # secret_key = secrets.token_urlsafe(64)
        self.SECRET_KEY = 'NiHuLSNTFA4RsvtbBmCcDDJXJxbAnw13MRwJsL9WdNT9Jf8_hrQ0hMKroq_96ewipByaBqGRfSuhMQqSn3cArg'

        # String Date Formatting
        self.DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
        self.DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

        # Database Config
        self.HOST = 'localhost'
        self.PORT = 3306
        self.USER = 'client'
        self.PASSWORD = 'clientPassword5!'

        self.EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

    def get_db_credentials(self):
        return {
            "host": self.HOST,
            "port": self.PORT,
            "user": self.USER,
            "password": self.PASSWORD
        }

    def get_message(self):
        return self.MESSAGE


class Work_Laptop_Config(Config):
    """Work Laptop Config Settings for Flask App"""
    def __init__(self):
        super().__init__()

        # Connection Credentials Message
        self.MESSAGE = 'Work Laptop DB Connection Credentials'

        # Database Connection
        self.HOST = '192.168.1.136'

        # File Saving
        self.UPLOAD_FOLDER = '/mnt/c/Users/Nathaniel Reeves/Documents/uploads'


class Home_PC_Config(Config):
    """Home PC Config Settings for Flask App"""

    def __init__(self):
        super().__init__()

        # Connection Credentials Message
        self.MESSAGE = 'Home PC DB Connection Credentials'

        # Database Connection
        self.HOST = 'localhost'

        # File Saving
        self.UPLOAD_FOLDER = '/mnt/s/uploads'


class Home_PC_To_Pi_Config(Config):
    """Home PC Config Settings for Flask App connecting to pi-server"""

    def __init__(self):
        super().__init__()

        # Connection Credentials Message
        self.MESSAGE = 'Home PC DB Connection Credentials'

        # Database Connection
        self.HOST = '209.33.207.141'

        # File Saving
        self.UPLOAD_FOLDER = '/mnt/s/uploads'


class School_Laptop_Config(Config):
    """School Laptop Config Settings for Flask App"""

    def __init__(self):
        super().__init__()

        # Connection Credentials Message
        self.MESSAGE = "School Laptop DB Connection Credentials"

        # Database Connection
        self.HOST = 'localhost'

        # File Saving
        self.UPLOAD_FOLDER = '/mnt/c/uploads'


class School_Laptop_To_Pi_Config(Config):
    """School Laptop Config Settings for Flask App"""

    def __init__(self):
        super().__init__()

        # Connection Credentials Message
        self.MESSAGE = "School Laptop DB Connection Credentials"

        # Database Connection
        self.HOST = '209.33.207.141'

        # File Saving
        self.UPLOAD_FOLDER = '/mnt/c/uploads'


class Pi_Server_Config(Config):
    """Pi Server Config Settings for Flask App"""

    def __init__(self):
        super().__init__()

        # Connection Credentials Message
        self.MESSAGE = "Pi Server DB Connection Credentials"

        # Database Connection
        self.HOST = '192.168.1.136'

        # File Saving
        self.UPLOAD_FOLDER = '/home/nreeves/uploads'

class Production_Config(Config):
    """Production Config Settings for Flask App"""

    def __init__(self):
        super().__init__()

        # Connection Credentials Message
        self.MESSAGE = "Production DB Connection Credentials"

        # Database Connection
        self.HOST = 'localhost'

        # File Saving
        self.UPLOAD_FOLDER = '/home/nreeves/uploads'

