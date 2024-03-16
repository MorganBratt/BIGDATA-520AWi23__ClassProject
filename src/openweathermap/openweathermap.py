import requests

class Weather_Client:
    def __init__(self,uri,key):
        self.uri = uri
        self.key = key


    def hello_world(self):
        print(F"uri:{self.uri} key:{self.key}")