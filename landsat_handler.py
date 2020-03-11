# AWS Lambda function for returning list of landsat scenes ids for input path/row

import json
import boto3

event = {
  "queryStringParameters": {
    "path": "143",
    "row": "37"
  }
}

def bad_request():
    error = {}
    error['Message'] = 'Bad request'
    badResponse = {}
    badResponse['statusCode'] = 200
    badResponse['headers'] = {}
    badResponse['headers']['Content-Type'] = 'application/json'
    badResponse['body'] = json.dumps(error)

    return badResponse

def landsat_handler(event):

    # parse event
    path = event['queryStringParameters']['path']
    row = event['queryStringParameters']['row']
    path = path.zfill(3)
    row = row.zfill(3)
    if int(path) > 233 or int(row) > 233:
        return bad_request()

    # search landsat s3 bucket
    s3 = boto3.client('s3', region_name='us-west-2')
    params = {
        'Bucket': 'landsat-pds',
        'Prefix': f'c1/L8/{path}/{row}/',
        'Delimiter': '/'
    }
    dirs = []
    s3Response = s3.list_objects_v2(**params)
    try:
        prefixes = s3Response['CommonPrefixes']
    except:
        return bad_request()
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

responseObject = add_zero(path)
print(responseObject)


'''

TODOS
- parse landsat prefixes
- filter through metadata (dates, cloud_cover)

'''
