import os
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from dotenv import load_dotenv
import time

# Load environment variables from the .env file
load_dotenv()

# Initialize S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_S3_REGION_NAME', 'us-east-1')
)

# Retrieve bucket name from environment
aws_bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')

def check_s3_connection():
    try:
        # Test listing files in the bucket
        response = s3.list_objects_v2(Bucket=aws_bucket_name)
        
        if 'Contents' in response:
            print("Connection to AWS S3 successful. Files:")
            # List all files in the bucket and pick one for testing
            for file in response['Contents']:
                print(f" - {file['Key']}")

            # Pick an actual file from the list (e.g., use the first file in the list)
            test_file_key = response['Contents'][0]['Key']
            print(f"Testing file access with: {test_file_key}")
            
            # Test CORS by trying to access a file (simulates a web request)
            try:
                s3.get_object(Bucket=aws_bucket_name, Key=test_file_key)
                print(f"File {test_file_key} accessed successfully (CORS check).")
            except ClientError as e:
                if e.response['Error']['Code'] == 'AccessDenied':
                    print(f"Access Denied while accessing {test_file_key}.")
                else:
                    print(f"Error accessing file {test_file_key}: {e}")

            # Now, add tests for static files (CSS and JS)

            # Test accessing CSS file (e.g., css/style.css)
            css_file_key = 'static/css/style.css'  # Adjust based on your actual file path
            print(f"Testing access to static CSS file: {css_file_key}")
            try:
                s3.get_object(Bucket=aws_bucket_name, Key=css_file_key)
                print(f"CSS file {css_file_key} accessed successfully.")
            except ClientError as e:
                if e.response['Error']['Code'] == 'AccessDenied':
                    print(f"Access Denied while accessing CSS file {css_file_key}.")
                else:
                    print(f"Error accessing CSS file {css_file_key}: {e}")
            
            # Test accessing JavaScript file (e.g., scripts/app.js)
            js_file_key = 'static/js/script.js'  # Adjust based on your actual file path
            print(f"Testing access to JavaScript file: {js_file_key}")
            try:
                s3.get_object(Bucket=aws_bucket_name, Key=js_file_key)
                print(f"JavaScript file {js_file_key} accessed successfully.")
            except ClientError as e:
                if e.response['Error']['Code'] == 'AccessDenied':
                    print(f"Access Denied while accessing JavaScript file {js_file_key}.")
                else:
                    print(f"Error accessing JavaScript file {js_file_key}: {e}")

        else:
            print(f"No files found in bucket {aws_bucket_name}.")
        
        # Rest of the upload, download, and deletion tests

    except NoCredentialsError:
        print("AWS credentials are missing or incorrect.")
    except PartialCredentialsError:
        print("Partial AWS credentials found; please check your credentials.")
    except ClientError as e:
        print(f"ClientError occurred: {e}")
        if e.response['Error']['Code'] == 'AccessDenied':
            print("Access Denied: You don't have permission to access this bucket.")
    except Exception as e:
        print(f"Error connecting to S3: {e}")

# Run the function to test S3 access and functionality
check_s3_connection()