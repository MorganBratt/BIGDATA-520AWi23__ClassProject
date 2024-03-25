import boto3, json

class S3BucketManager:
    def __init__(self, bucket_name, region_name='us-east-1'):
        self.bucket_name = bucket_name
        self.region_name = region_name
        self.s3 = boto3.client('s3', region_name=self.region_name)

    def upload_file(self, file_name, object_name=None):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param object_name: S3 object name. If not specified, file_name is used
        """
        if object_name is None:
            object_name = file_name
        try:
            self.s3.upload_file(file_name, self.bucket_name, object_name)
            # print(f"'{file_name}' has been uploaded to '{self.bucket_name}/{object_name}'")
        except Exception as e:
            print(f"Error uploading file: {e}")

    def read_file(self, object_name):
        """Read a file from an S3 bucket

        :param object_name: S3 object name
        :return: The file content as a string
        """
        try:
            response = self.s3.get_object(Bucket=self.bucket_name, Key=object_name)
            file_content = response['Body'].read().decode('utf-8')
            return file_content
        except Exception as e:
            print(f"Error reading file: {e}")
            return None

    def read_json(self, object_name):
        """Read a JSON file from an S3 bucket and return it as a Python dict."""
        file_content_str = self.read_file(object_name)
        if file_content_str is not None:
            return json.loads(file_content_str)
        else:
            return None
        
    def upload_string_as_file(self, string_data, object_name):
        """Upload a string as a file to an S3 bucket."""
        try:
            self.s3.put_object(Body=string_data, Bucket=self.bucket_name, Key=object_name)
            # print(f"'{object_name}' has been updated in '{self.bucket_name}'.")
        except Exception as e:
            print(f"Error updating file: {e}")

    def update_json(self, object_name, updates):
        """Update a JSON file in an S3 bucket with new values for specified keys."""
        data = self.read_json(object_name)
        if data is not None:
            # Update the data with new values
            data.update(updates)
            # Convert the updated dictionary back to a JSON string
            updated_json_str = json.dumps(data)
            # Upload the updated JSON string back to S3
            self.upload_string_as_file(updated_json_str, object_name)
        else:
            print(f"Failed to read {object_name} from bucket {self.bucket_name}.")


# Example usage
if __name__ == "__main__":
    
    import os
    conf_json = os.getenv('PROJECT_CONF')
    configuration = json.loads(conf_json)

    file_name = 'data.json'
    object_name = 'data/data.json'  # Object name in S3. It can be a path like 'folder/subfolder/example.txt'

    # create the s3_manager
    s3_manager = S3BucketManager(configuration['aws']['bucket_name'], configuration['aws']['region_name'])

    # Upload a file
    s3_manager.upload_file(file_name, object_name)

    # Read a file
    content = s3_manager.read_file(object_name)
    if content is not None:
        print(f"Content of '{object_name}':\n{content}")

    # Update the JSON file in S3
    updates = {'bookmark_epoc': 0}
    s3_manager.update_json(object_name, updates)

    # confirm update
    content = s3_manager.read_file(object_name)
    if content is not None:
        print(f"Content of '{object_name}':\n{content}")

