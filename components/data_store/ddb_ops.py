import boto3

def put_item_ddb(ddb_table,item_data):
  """Puts an item into a DynamoDB table.

  Args:
    token_id: The partition key of the item.
    user_id: The sort key of the item.
    item_data: The item data to be put into the table.
  """

  dynamodb = boto3.resource('dynamodb')
  table = dynamodb.Table(ddb_table)

  try:
    response = table.put_item(Item=item_data)
    #print("Item put successfully:", response)
  except Exception as e:
    print("Error putting item:", e)


def query_dynamodb(table_name, partition_key, sort_key=None, filter_expr=None, scan_index_forward=True):
  """Queries a DynamoDB table for items matching the specified partition key and sort key.

  Args:
    table_name: The name of the DynamoDB table.
    partition_key: The partition key value.
    sort_key: The sort key value (optional).
    filter_expr: A filter expression to further refine the query (optional).
    scan_index_forward: Whether to scan the index in forward or backward order (optional).

  Returns:
    A list of items that match the query.
  """

  dynamodb = boto3.resource('dynamodb')
  table = dynamodb.Table(table_name)

  key_condition_expression = "#pk = :pk"
  expression_attribute_names = {"#pk": partition_key}
  expression_attribute_values = {":pk": partition_key}

  if sort_key is not None:
    key_condition_expression += " AND #sk = :sk"
    expression_attribute_names["#sk"] = sort_key
    expression_attribute_values[":sk"] = sort_key

  if filter_expr is not None:
    key_condition_expression += " AND " + filter_expr

  try:
    response = table.query(
        KeyConditionExpression=key_condition_expression,
        ExpressionAttributeNames=expression_attribute_names,
        ExpressionAttributeValues=expression_attribute_values,
        ScanIndexForward=scan_index_forward
    )
    return response['Items']
  except Exception as e:
    print("Error querying DynamoDB:", e)
    return []

if __name__ == '__main__':
    # Example usage:
    table_name = "your_table_name"
    partition_key_value = "your_partition_key"
    sort_key_value = "your_sort_key"
    filter_expr = "attribute_name > :value"
    filter_value = 100

    items = query_dynamodb(table_name, partition_key_value, sort_key_value, filter_expr, filter_value)

    for item in items:
    print(item)