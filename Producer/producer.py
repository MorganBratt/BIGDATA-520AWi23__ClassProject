import os

def get_key():
    # grab the key if the code is running local
    key = os.getenv('openweathermap')


get_key()
