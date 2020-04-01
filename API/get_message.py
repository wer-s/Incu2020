import requests

roomId = 'Y2lzY29zcGFyazovL3VzL1JPT00vYTViOGRhYjItMzljNC0zNWIyLTkyZjktMjJiZjNhZjE2NDIy'
token = 'Mzg0N2ViYjgtMDhmZC00Yzc2LTk4YzAtM2MxYmQwNjE4YmU0MmJjZmM4YzQtYjI4_PF84_consumer'

url = "https://api.ciscospark.com/v1/messages?roomId=" + roomId

header = {"content-type": "application/json; charset=utf-8", 
		  "authorization": "Bearer " + token}

response = requests.get(url, headers = header, verify = True)

print(response.json())
