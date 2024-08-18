#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 13:36:07 2024

@author: kausik
"""
from utils import util_functions as uf
from components.queue import q_ops
from components.data_store import s3_ops
from components.Gen_AI import GenResponse as gai
from components.data_store import ddb_ops
import datetime
#job_data = {"task": "process_data", "data": "some_data"}
queue_url = uf.get_secret('QUEUE_URL')

# try:    
#     msg = q_ops.push_job(queue_url, job_data)
#     print("Job created successfully."+msg)
# except Exception as e:
#     print(f"Error creating job: {e}")

msg,handle = q_ops.get_job(queue_url)
print(msg)
msg_json = uf.string_to_dict(msg)
bucket_name = msg_json['bucket']
object_key = msg_json['token_id']
print(bucket_name,object_key)
response = s3_ops.read_object_from_s3(bucket_name,object_key)
#print(response.keys)

#img = s3_ops.return_response_as_image(response)
#GenAI call
prompt = gai.get_prompt('data/prompt.txt')
input = gai.get_prompt('data/input.txt')
model = gai.gemini_config(uf.get_secret('GOOGLE_API_KEY'))

result = gai.get_genai_response(model,prompt,response,input)
res_dict = uf.string_to_dict(result)
# print(res_dict['Total_Amount'])
# Create DDB row
ddb_item = {
    'token_id' : msg_json['token_id'],
    'user_id' : msg_json['user_id'],
    'post_time' : msg_json['post_time'],
    'process_time' : datetime.datetime.now().strftime('%Y%m%d%H%M%S')
}
ddb_item.update(res_dict)
#print(ddb_item)
ddb_ops.put_item_ddb(uf.get_secret('DDB_RESULTS'),ddb_item)
q_ops.delete_msg(queue_url,handle)