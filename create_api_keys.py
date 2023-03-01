import excel_helper
import json
import api_keys_managements

data = excel_helper.read_excel_file("Namelist.xlsx", "Name")
prefix = "AiVirtualAssistant"

api_keys_managements.set_aws_default_region_in_env()
plan = api_keys_managements.get_usage_plan_id_by_name(prefix)
print(plan)
results = []
for student in data:
    print(json.dumps(student))
    keyId, KeyValue= api_keys_managements.create_api_key((prefix +"_"+ str(student["StudendId"])),json.dumps(student))
    api_keys_managements.add_api_key_to_usage_plan(keyId, plan)
    result = {
        "StudentId": student["StudendId"],
        "Name": student["Name"],
        "KeyId": keyId,
        "KeyValue": KeyValue,
        "Email": str(student["StudendId"])+"@stu.vtc.edu.hk",
    }
    results.append(result)

results = json.dumps(results);
def save_json_to_file(filename, json_data): 
    with open(filename, 'w') as outfile:
        json.dump(json_data, outfile)

save_json_to_file("Key.json", results)
excel_helper.export_json_to_excel_file("Key.xlsx", "Key", results)
