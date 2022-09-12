from urllib import request, parse
import requests
import json
# print(data)
data = {'horizontal':-1}
# data = "{'horizontal': -1}"
# data = parse.urlencode(data)
print(data)
# data= data.encode()
print(data)
# data = json.dumps(data)
# # Convert to String
# data = str(data)
print(data)
# print(data)

# data = 'data, {\"Vertical\":- 1}'
# print(data)
# data = data.encode('utf-8')
# print(data)

# req =  request.post('http://172.24.8.24:8082/Hrotation', data=data) # this will make the method "POST"
req =  requests.post('http://172.24.8.24:8080/Hrotation', json=data) # this will make the method "POST"
# resp = request.urlopen(req)
# print(resp)

# req = request.Request('http://172.24.8.24:8082/Vrotation', data=data, ) # this will make the method "POST"
# resp = request.urlopen(req)
# print(resp)
# try:
#         print(request.form)
#         data = json.loads(request.form.get('data'))
        
#     except:
#         return '1 error',202