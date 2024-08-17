import boto3
def upload_image_to_s3(bucket_name, image_parts, image_id):
  """Pushes an image to an S3 bucket.

  Args:
    bucket_name: The name of the S3 bucket.
    image_parts: A list of image parts, each with a mime type and data.
    image_id: The ID to use for the uploaded image.
  """

  s3 = boto3.client('s3')

  try:
    s3.put_object(
        Bucket=bucket_name,
        Key=f'{image_id}.jpg',
        Body=image_parts[0]['data'],
        ContentType=image_parts[0]['mime_type']
    )
    print(f"Image '{image_id}.jpg' uploaded successfully to S3 bucket '{bucket_name}'.")
  except Exception as e:
    print(f"Error uploading image: {e}")