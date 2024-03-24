import os, json
from . import s3

DATA_FILE_PATH = "data/data.json" # move to config?

class DataRepository:
    def __init__(self):
        conf_json = os.getenv('PROJECT_CONF')
        self.configuration = json.loads(conf_json)
        self.s3_manager = s3.S3BucketManager(self.configuration['aws']['bucket_name'], self.configuration['aws']['region_name'])

# get bookmark
    def get_bookmark(self):
        content = self.s3_manager.read_file(DATA_FILE_PATH)
        content_json = json.loads(content)
        return(content_json["bookmark_epoc"])

# set bookmark
    def set_bookmark(self, bookmark:int):
        content = self.s3_manager.read_file(DATA_FILE_PATH)
        content_json = json.loads(content)
        content_json["bookmark_epoc"] = bookmark
        self.s3_manager.update_json(DATA_FILE_PATH, content_json)

# get start
    def get_start_date_epoch(self):
        content = self.s3_manager.read_file(DATA_FILE_PATH)
        content_json = json.loads(content)
        return(content_json["start_epoc"])
    


if __name__ == "__main__":
    
    # test the data repository
    data_repository = DataRepository()
    
    # get the current bookmark
    bookmark_before = data_repository.get_bookmark()
    print(f"bookmark get: {bookmark_before}")

    # set the bookmark
    data_repository.set_bookmark(bookmark_before + 1)

    # validate the update to the bookmark
    bookmark_after = data_repository.get_bookmark()
    print(f"bookmark get: {bookmark_after}")

    #set the bookmark back
    # set the bookmark
    data_repository.set_bookmark(bookmark_before)

    # get the start date if the bookmark is 0 or none
    start_date = data_repository.get_start_date_epoch()
    print(f"Default date to start from: {start_date}")