import pprint
import boto3

def set_aws_default_region_in_env():
    import os
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

def list_all_aws_apigatway_keys_paginated():
    client = boto3.client('apigateway')
    response = client.get_api_keys()
    keys = response["items"]
    while "position" in response:
        response = client.get_api_keys(position=response["position"])
        keys += response["items"]
    return keys

def list_all_aws_apigatway_usage_plans_paginated():
    client = boto3.client('apigateway')
    response = client.get_usage_plans()
    plans = response["items"]
    while "position" in response:
        response = client.get_usage_plans(position=response["position"])
        plans += response["items"]
    return plans

def list_all_aws_apigatway_keys_in_usage_plan_paginated(usage_plan_id):
    client = boto3.client('apigateway')
    response = client.get_usage_plan_keys(
        usagePlanId=usage_plan_id
    )
    keys = response["items"]
    while "position" in response:
        response = client.get_usage_plan_keys(
            usagePlanId=usage_plan_id,
            position=response["position"]
        )
        keys += response["items"]
    return keys

def delete_all_apigateway_keys_in_usage_plan(usage_plan_id):
    keys = list_all_aws_apigatway_keys_in_usage_plan_paginated(usage_plan_id)
    client = boto3.client('apigateway')
    for key in keys:
        print("Deleting key: {}".format(key["name"]))
        client.delete_usage_plan_key(
            usagePlanId=usage_plan_id,
            keyId=key["id"]
        )

def delete_all_apigateway_keys():
    keys = list_all_aws_apigatway_keys_paginated()
    client = boto3.client('apigateway')
    for key in keys:
        print("Deleting key: {}".format(key["name"]))
        client.delete_api_key(
            apiKey=key["id"]
        )

def create_api_key(api_key_name,description):
    client = boto3.client('apigateway')
    response = client.create_api_key(
        name=api_key_name,
        description = description,
        enabled=True,
        generateDistinctId=True       
    )
    return response["id"],response["value"]

def add_api_key_to_usage_plan(api_key_id, usage_plan_id):
    client = boto3.client('apigateway')
    client.create_usage_plan_key(
        usagePlanId=usage_plan_id,
        keyId=api_key_id,
        keyType="API_KEY"
    )

def get_usage_plan_id_by_name(usage_plan_name):
    plans = list_all_aws_apigatway_usage_plans_paginated()
    for plan in plans:
        if plan["name"] == usage_plan_name:
            return plan["id"]
    return None


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(depth=6)
    set_aws_default_region_in_env()
    keys = list_all_aws_apigatway_usage_plans_paginated()
    print(keys)

    # pp.pprint(keys)
    # delete_all_apigateway_keys()

