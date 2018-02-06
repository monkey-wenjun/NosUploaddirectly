#!/usr/bin/python
# -*- coding: utf-8 -*-

import base64
import hmac
import hashlib
import time
import requests
import json
import datetime


# 计算签名

		
def sign(accesskey,secretkey,bucketname,objectname):

    expirestime = int(time.time()+6000)

    json_data = {"Bucket":bucketname,"Object":objectname,"Expires":expirestime}

    putpolicy = json.dumps(json_data)

    encodedputpolicy = base64.b64encode(putpolicy)

    signature = hmac.new(secretkey, encodedputpolicy, digestmod=hashlib.sha256).digest();

    encodedsign = base64.b64encode(signature)

    token = "UPLOAD " + accesskey + ":" + encodedsign + ":" + encodedputpolicy

    return token

# 获取最佳节点

def getnode(bucketname):
	
    url ='http://lbs-eastchina1.126.net/lbs?version=1.0'+'&bucketname='+bucketname

    node = requests.get(url)

    nodeValue= node.json()

    return nodeValue['upload'][0]

# 分块上传

def postfile(xnostoken,bucketname,
			objectname,offset,
			complete,host,contentlength,
			contenttype,filepath):
    gmtformat = '%a, %d %b %Y %H:%M:%S GMT'
    gmtdate = datetime.datetime.utcnow().strftime(gmtformat)
    querystring = {"offset":offset,"complete":complete,"version":1.0}

    headers = {'Host':host,'Content-Length':contentlength,
			'x-nos-token':xnostoken,'Content-type':contenttype,'Date':gmtdate}

    requestaddress = getnode(bucketname)

    requestaddress = str(requestaddress)

    url = requestaddress+'/'+bucketname+'/'+objectname

    with open(filepath, 'r') as f:

	    requestapi = requests.post(url,params=querystring,headers=headers,data=f)
	
	    print(requestapi.json())


# 各必传参数

def main():

    bucketname = 'netease01' 

    objectname = '5.jpg' 

    accesskey = "" 

    secretkey = ""

    offset = 0

    complete = True

    host = 'nos-eastchina1.126.net' 

    contenttype = 'image/jpeg'

    contentlength = '34771'

    filepath = '/Users/wenjun/PycharmProjects/Test/test.jpg'

    xnostoken = sign(accesskey,secretkey,bucketname,objectname)

    postfile(xnostoken,bucketname,objectname,offset,complete,host,contentlength,contenttype,filepath)


if __name__ == '__main__':
	
    main()
