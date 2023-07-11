import os
from dotenv import load_dotenv

class Manager():

    def __init__(self) -> None:
        self.env_path = '.env'
        load_dotenv(self.env_path)

    def get_database_credentials(self) -> dict:
        credentials = {
            'NAME': os.getenv('NAME'),
            'USER': os.getenv('USER'),
            'PASSWORD': os.getenv('PASSWORD'),
            'HOST': os.getenv('HOST'),
            'PORT': os.getenv('PORT'),
        }        
        return credentials
    
    def get_items(self, *args) -> dict:
        values = {arg : os.getenv(arg) for arg in args}
        return values
    
    def get_key(self, key) -> dict:
        return os.getenv(key)
    
