import simplejson
import requests

json_raw_data = open('example_form_json.txt','r').read()
json_data = simplejson.loads(json_raw_data)
#print json_data

r = requests.post("http://localhost:9292/typeformize", json = json_data)

print r.text
