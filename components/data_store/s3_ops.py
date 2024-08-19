import boto3
from utils import util_functions as uf
def upload_image_to_s3(bucket_name, image_parts, image_id):
  """Pushes an image to an S3 bucket.

  Args:
    bucket_name: The name of the S3 bucket.
    image_parts: A list of image parts, each with a mime type and data.
    image_id: The ID to use for the uploaded image.
  """

  s3 = boto3.client('s3',region_name = uf.get_secret('AWS_DEFAULT_REGION')) 

  try:
    s3.put_object(
        Bucket=bucket_name,
        Key=f'{image_id}',
        Body=image_parts[0]['data'],
        ContentType=image_parts[0]['mime_type']
    )
    #print(f"Image '{image_id}.jpg' uploaded successfully to S3 bucket '{bucket_name}'.")
  except Exception as e:
    print(f"Error uploading image: {e}")

def read_object_from_s3(bucket_name, object_name):
  """Reads an object from an S3 bucket.

  Args:
    bucket_name: The name of the S3 bucket.
    object_name: The name of the object to read.

  Returns:
    The contents of the object as a string.
  """

  s3 = boto3.client('s3',region_name = uf.get_secret('AWS_DEFAULT_REGION')) 

  try:
    response = s3.get_object(Bucket=bucket_name, Key=object_name)
    retdict = {}
    retdict['data'] = response['Body'].read()
    retdict['mime_type'] = response['ContentType'] 
    return retdict
  except Exception as e:
    print(f"Error reading object: {e}")
    return None

def return_response_as_image(response):
    bytes_data = response['Body'].read()
    mime_type = response['ContentType']

    image_parts = [
        {
            "mime_type": mime_type,
            "data": bytes_data
        }
    ]
    return image_parts