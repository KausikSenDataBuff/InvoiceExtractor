import pandas as pd
from components.data_store import ddb_ops 
from utils import util_functions as uf
from components.login import users
ddb_usr=uf.get_secret('DDB_USERS')
user_id=users.get_userid()
data = ddb_ops.query_ddb(ddb_usr, pk_name='user_id',pk_val=user_id)
data = pd.DataFrame(data)
for index,row in data.iterrows():
    print(row['job_status'])
# update_expression = "set #status = :status"
# expression_attribute_names = {"#status": "job_status"}
# expression_attribute_values = {":status": "Completed"}
# ddb_ops.update_item_ddb(ddb_usr,pk_name='user_id',pk_val=user_id,sk_name='token_id',sk_val='1723965201352-aeb8690b-911a-4a77-8a18-5d60fec93f13',
#         update_expression=update_expression,expression_attribute_names=expression_attribute_names,expression_attribute_values=expression_attribute_values)
# data = ddb_ops.query_ddb(ddb_usr, pk_name='user_id',pk_val=user_id)
# print(data)
# ddb_results = uf.get_secret('DDB_RESULTS') 
# token_id='1723959934577-1de93650-8d17-4894-919b-7d3fb576b8a9'
# row_data = ddb_ops.query_ddb(ddb_results,'token_id',token_id,sk_name='user_id',sk_val=user_id)
# print(row_data[0])