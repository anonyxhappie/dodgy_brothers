class Constants:
    
    """
    Constant is class used to store all string literals
    """
    
    ERROR = 'error'
    EXCEPTION_CODES = {
        'DEFAULT': [10000, 'There is some error in service, please try again later'],
        'INVALID_REQUEST': [10001, 'Request data is invalid'],
        'DATABASE_READ_ERROR': [10002, 'An error occured while reading database'],
        'DATABASE_WRITE_ERROR': [10003, 'An error occured while writing in database'],
        'INVALID_CAR': [10100, 'Invalid car'],
    }
    MESSAGE = 'message'
    RESULT = 'result'
    STATUS = 'status'
    PAGE = 'page'
    EMAIL_FROM = 'admin@dodgy-brothers.local'
    EMAIL_TO = 'mike@example.org'
