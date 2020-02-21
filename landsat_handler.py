# AWS Lambda function for returning list of landsat scenes ids for input path/row

import json
import boto3

def landsat_handler(event, context):

    # parse event
    path = event['path']
    row = event['row']
    
    # search landsat s3 bucket
    s3 = boto3.client('s3', region_name='us-west-2')
    params = {
        'Bucket': 'landsat-pds',
        'Prefix': f'c1/L8/{path}/{row}/',
        'Delimiter': '/'
    }
    dirs = []
    s3Response = s3.list_objects_v2(**params)
    prefixes = s3Response['CommonPrefixes']
    for prefix in prefixes:
        raw_dir = list(prefix.values())
        dirs.append(raw_dir[0])
    
    # construct body of response object
    landsatResponse = {}
    landsatResponse['Dirs'] = dirs
    landsatResponse['Message'] = 'Hello from lambda land'

    # construct http response object
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(landsatResponse)

    # return
    return responseObject

'''

TODOS
- parse landsat prefixes
- filter through metadata (dates, cloud_cover)

'''
