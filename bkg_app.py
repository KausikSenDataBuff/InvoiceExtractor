# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 13:36:07 2024

@author: kausik
Background application for processing jobs
"""
from utils import util_functions as uf
from components.queue import q_ops
from components.data_store import s3_ops
from components.Gen_AI import GenResponse as gai
from components.data_store import ddb_ops
from components.login import users
import datetime
import time
def mark_job_complete(user_id,token_id,job_status):
    ddb_users = uf.get_secret('DDB_USERS')
    update_expression = "set #status = :status"
    expression_attribute_names = {"#status": "job_status"}
    expression_attribute_values = {":status": job_status}
    ddb_ops.update_item_ddb(ddb_users,pk_name='user_id',pk_val = user_id, sk_name='token_id', sk_val=token_id,
        update_expression=update_expression,expression_attribute_names=expression_attribute_names,expression_attribute_values=expression_attribute_values)

def process_packets():
    # This will run in loop for each job packet retrieved from the queue.
    queue_url = uf.get_secret('QUEUE_URL')
    sleep_counter = 1
    while(True):
        # 1 Get job from queue
        msg,handle = q_ops.get_job(queue_url)
        if len(msg)==0:
            # No messages currently, sleep for 10 mins
            print(f'No jobs, sleep for {int(sleep_counter*10)} mins')
            time.sleep(600)
            sleep_counter+=1

        else:
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
    

# TODO Need to find a work around of SQS polling through DDB/SNS
# #Poll the users table to find if there is any new pending cases
# ddb_users = uf.get_secret('DDB_USERS')
# pk_name = 'user_id'
# pk_val = users.get_userid() # TODO : This will later run for all user IDs 
# # Or may directly poll the queue for messages
# pending = ddb_ops.query_ddb(ddb_users, pk_name,pk_val, filter_expr=None,filter_value=filter_value)
# print(pending)

process_packets()