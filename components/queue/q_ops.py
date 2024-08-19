import boto3
from utils import util_functions as uf
def push_job(queue_url, job_object):
  """Creates a job in a specified AWS queue.

  Args:
    queue_url: The URL of the queue.
    job_object: The job object to be added to the queue.
  """

  sqs = boto3.client('sqs',region_name = uf.get_secret('AWS_DEFAULT_REGION'))
  response = sqs.send_message(
      QueueUrl=queue_url,
      MessageBody=str(job_object)
  )
  #print(f"Job created. Message ID: {response['MessageId']}")
  return response['MessageId']
  
def get_job(queue_url):
  sqs = boto3.client('sqs',region_name = uf.get_secret('AWS_DEFAULT_REGION'))
  response = sqs.receive_message(
      QueueUrl=queue_url,
      MaxNumberOfMessages=1,
      WaitTimeSeconds=20
  )
  message_body = receipt_handle = []
  if 'Messages' in response:
    for message in response['Messages']:
      message_body = message['Body']
      message_id = message['MessageId']
      receipt_handle=message['ReceiptHandle']
  return message_body,receipt_handle 

def delete_msg(queue_url, receipt_handle):
  """Deletes a message from an SQS queue.

  Args:
    queue_url: The URL of the SQS queue.
    receipt_handle: The receipt handle of the message to delete.
  """
  sqs = boto3.client('sqs',region_name = uf.get_secret('AWS_DEFAULT_REGION'))
  try:
    response = sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    #print("Message deleted successfully:", response)
  except Exception as e:
    print("Error deleting message:", e) 