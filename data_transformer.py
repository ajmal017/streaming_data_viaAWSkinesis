import json
import base64

def lambda_handler(event, context):
    output_records = []
    for record in event["records"]:
        output_records.append({
        "recordId": record['recordId'],
        "result": "Ok",
        "data": record["data"] + "Cg==" # this is the key here
    })
    return { "records": output_records }