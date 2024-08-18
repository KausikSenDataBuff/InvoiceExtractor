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


def query_ddb(table_name, pk_name,pk_val,sk_name=None,sk_val=None, filter_expr=None, scan_index_forward=True):
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
    expression_attribute_names = {"#pk": pk_name}
    expression_attribute_values = {":pk": pk_val}
    if sk_name is not None:
        key_condition_expression += " AND #sk = :sk"
        expression_attribute_names["#sk"] = sk_name
        expression_attribute_values[":sk"] = sk_val

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

def update_item_ddb(table_name, pk_name,pk_val, update_expression, expression_attribute_names, expression_attribute_values,
    sk_name=None,sk_val=None):
  """Updates an item in a DynamoDB table.

  Args:
    table_name: The name of the DynamoDB table.
    partition_key: The partition key value.
    sort_key: The sort key value (optional).
    update_expression: The update expression to apply to the item.
    expression_attribute_names: A dictionary mapping placeholders to attribute names.
    expression_attribute_values: A dictionary mapping placeholders to attribute values.
  """

  dynamodb = boto3.resource('dynamodb')
  table = dynamodb.Table(table_name)

  try:
    response = table.update_item(
        Key={
            pk_name : pk_val,
            sk_name : sk_val
        },
        UpdateExpression=update_expression,
        ExpressionAttributeNames=expression_attribute_names,
        ExpressionAttributeValues=expression_attribute_values  

    )
    #print("Item updated successfully:", response)
  except Exception as e:
    print("Error updating item:", e)