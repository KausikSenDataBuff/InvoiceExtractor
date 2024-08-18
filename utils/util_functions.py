import datetime
import uuid
from dotenv import load_dotenv
import os
import json
def generate_token_id():
  """Generates a unique token ID based on current date and time.

  Returns:
    A string representing the unique token ID.
  """

  # Get current timestamp in milliseconds
  timestamp = int(datetime.datetime.now().timestamp() * 1000)

  # Generate a random UUID
  random_uuid = str(uuid.uuid4())

  # Combine timestamp and UUID to create a unique token ID
  token_id = f"{timestamp}-{random_uuid}"

  return token_id
def get_secret(param):
    '''
    Fetches the value of param envirnment variable
    stored in .env
    '''
    load_dotenv()    
    return os.getenv(param)

def string_to_dict(string):
  """Converts a string to a Python dictionary.

  Args:
    string: The string to convert.

  Returns:
    The converted dictionary.
  """
  try:

    return json.loads(string.replace("'", '"'))
  except json.JSONDecodeError:
    print("Error: Invalid JSON string.")
    return None

if __name__ == "__main__":
  # Generate and print a token ID
  token_id = generate_token_id()
  print("Generated token ID:", token_id)
  print(get_secret('QUEUE_URL'))