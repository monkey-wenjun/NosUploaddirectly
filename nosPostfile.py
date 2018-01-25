#!/usr/bin/python
# -*- coding: utf-8 -*-

import base64
import hmac
import hashlib
import time
import requests
import json


# 计算token

def token(accesskey,secretkey):
	
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

	querystring = {"offset":offset,"complete":complete,"version":1.0}

	headers = {'Host':host,'Content-Length':contentlength,
				'x-nos-token':xnostoken,'Content-type':contenttype}
	
	requestaddress = getnode(bucketname)
	
	requestaddress = str(requestaddress)
	
	url = requestaddress+'/'+bucketname+'/'+objectname

	with open(filepath, 'r') as f:

		r = requests.post(url,params=querystring,headers=headers,data=f)
		
		print(r.json())

if __name__ == '__main__':
	
	bucketname = 'netease01'
	
	objectname = '12344.jpg'
	
	accesskey = ""
	
	secretkey = ""
	
	xnostoken = token(accesskey,secretkey)
	
	offset = 0
	
	complete = True
	
	host = 'nos-eastchina1.126.net'
	
	contenttype = 'image/jpeg'
	
	contentlength = '200000'
	
	filepath = '/Users/wenjun/PycharmProjects/Test/test.jpg'
	
	postfile(xnostoken,bucketname,objectname,offset,complete,host,contentlength,contenttype,filepath)
