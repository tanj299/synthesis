import requests

# payload = {'arduino': "" , 'error': "", 'make_request': "", 'on_off': "", 'pin': "", 'plant_id': "", "timestamp": ""}
r = requests.get('http://localhost:5000/requests/1')
print(r.text)