#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 13:36:07 2024

@author: kausik
"""
from utils import util_functions
from components.queue import q_ops
job_data = {"task": "process_data", "data": "some_data"}
queue_name = "my-queue"  # Replace with your actual queue name

try:
    queue_url = util_functions.get_secret('QUEUE_URL')
    msg = q_ops.push_job(queue_url, job_data)
    print("Job created successfully."+msg)
except Exception as e:
    print(f"Error creating job: {e}")