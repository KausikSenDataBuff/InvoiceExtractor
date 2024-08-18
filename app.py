import streamlit as st
from PIL import Image
import datetime
import time
from components.data_store import s3_ops
from utils import util_functions as uf
from application import processed_jobs as pj
from components.queue import q_ops
from components.login import users
from components.data_store import ddb_ops

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

##initialize our streamlit app
st.set_page_config(page_title="Invoice Extractor Demo")
st.header("Invoice Extractor Application")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Invoice to be analyzed.", use_column_width=True)
submit=st.button("Upload")

if submit:
    # 1 Upload to S3
    bucket_name = uf.get_secret('BUCKET_NAME')
    image_id = uf.generate_token_id()
    image_data = input_image_setup(uploaded_file)  
    st.subheader("Please wait....")  
    response=s3_ops.upload_image_to_s3(bucket_name, image_data, image_id)
    st.subheader("File uploaded with ID : "+image_id)
    st.subheader("Please check in the processed job after sometime")
    #st.write(response)
    # 2 Create job object
    job_obj = {}
    job_obj['bucket']=bucket_name
    job_obj['token_id']=image_id
    #Todo - to integrate with login components
    job_obj['user_id']='dummy'
    job_obj['post_time']=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    # 3 Push job to queue
    queue_url = uf.get_secret('QUEUE_URL')
    msg = q_ops.push_job(queue_url, job_obj)
    # 4 Push job to DDB for status
    ddb_table = uf.get_secret('DDB_USERS')
    ddb_item = { 
        'user_id' : users.get_userid(),
        'job_status' : 'Pending',
        'token_id' : image_id
    }
    ddb_ops.put_item_ddb(ddb_table,ddb_item)
if st.button("See Your Jobs"):
  pj.all_jobs_page()