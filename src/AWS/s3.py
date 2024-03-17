import boto3

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
            print(f"'{file_name}' has been uploaded to '{self.bucket_name}/{object_name}'")
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

# Example usage
if __name__ == "__main__":
    bucket_name = 'lostislandapps'
    region_name = 'us-west-2'  # For example, 'us-east-1'
    file_name = 'test.md'
    object_name = 'test/test.md'  # Object name in S3. It can be a path like 'folder/subfolder/example.txt'

    # Initialize the S3BucketManager
    s3_manager = S3BucketManager(bucket_name, region_name)

    # Upload a file
    s3_manager.upload_file(file_name, object_name)

    # Read a file
    content = s3_manager.read_file(object_name)
    if content is not None:
        print(f"Content of '{object_name}':\n{content}")
