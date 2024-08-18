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
def mark_job_complete(user_id,token_id,job_status):
    update_expression = "set #status = :status"
    expression_attribute_names = {"#status": "job_status"}
    expression_attribute_values = {":status": job_status}
    ddb_ops.update_item_ddb(ddb_usr,pk_name='user_id',pk_val = user_id, sk_name='token_id', sk_val=token_id,
        update_expression=update_expression,expression_attribute_names=expression_attribute_names,expression_attribute_values=expression_attribute_values)
queue_url = uf.get_secret('QUEUE_URL')

# 1 Get job from queue
msg,handle = q_ops.get_job(queue_url)
print(msg)
msg_json = uf.string_to_dict(msg)
bucket_name = msg_json['bucket']
object_key = msg_json['token_id']
# 2 Retrieve image from S3
print(bucket_name,object_key)
response = s3_ops.read_object_from_s3(bucket_name,object_key)

# 3 GenAI call
prompt = gai.get_prompt('data/prompt.txt')
input = gai.get_prompt('data/input.txt')
model = gai.gemini_config(uf.get_secret('GOOGLE_API_KEY'))

result = gai.get_genai_response(model,prompt,response,input)
res_dict = uf.string_to_dict(result)
# 4 Create DDB row in DDB_Results 
user_id = msg_json['user_id']
token_id = msg_json['token_id']
ddb_item = {
    'token_id' : token_id,
    'user_id' : user_id,
    'post_time' : msg_json['post_time'],
    'process_time' : datetime.datetime.now().strftime('%Y%m%d%H%M%S')
}
ddb_item.update(res_dict)
#print(ddb_item)
ddb_ops.put_item_ddb(uf.get_secret('DDB_RESULTS'),ddb_item)
# 5 Update Job status table
ddb_usr=uf.get_secret('DDB_USERS')
mark_job_complete(user_id,token_id,"Completed")
# 6 Delete processed message
q_ops.delete_msg(queue_url,handle)