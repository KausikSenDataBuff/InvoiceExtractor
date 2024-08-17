import boto3
def push_job(queue_url, job_object):
  """Creates a job in a specified AWS queue.

  Args:
    queue_url: The URL of the queue.
    job_object: The job object to be added to the queue.
  """

  sqs = boto3.client('sqs')
  response = sqs.send_message(
      QueueUrl=queue_url,
      MessageBody=str(job_object)
  )
  #print(f"Job created. Message ID: {response['MessageId']}")
  return response['MessageId']
  

