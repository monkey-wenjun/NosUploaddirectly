#-*coding:utf-8-*-
import nos

access_key = ""
secret_key = ""
end_point = "nos-eastchina1.126.net"
bucket = "net"
object = "test111.jpg"
file_name = "/Users/wenjun/PycharmProjects/Test/test.jpg"

client = nos.Client(access_key, secret_key, end_point=end_point)

try:
  client.put_object(bucket, object,open(file_name, "rb"))
except nos.exceptions.ServiceException as e:
  print (
    "ServiceException: %s\n"
    "status_code: %s\n"
    "error_type: %s\n"
    "error_code: %s\n"
    "request_id: %s\n"
    "message: %s\n"
  ) % (
  e,
  e.status_code,  # 错误 http 状态码
  e.error_type,   # NOS 服务器定义错误类型
  e.error_code,   # NOS 服务器定义错误码
  e.request_id,   # 请求 ID，有利于 nos 开发人员跟踪异常请求的错误原因
  e.message       # 错误描述信息
  )
except nos.exceptions.ClientException as e:
  print (
  "ClientException: %s\n"
  "message: %s\n"
  ) % (
  e,
  e.message       # 客户端错误信息
  )