import requests
from rest_framework.decorators import api_view

API_URL = "http://127.0.0.1:8000/send/"
# api_key ="http://127.0.0.1:8000/get/"
user = {
    'fullname': 'jone',
    'email': 'jone@example.com',
    'phone_number': '1234567890',
    'work': '123 Main St',
    'date_of_birth':'2002.10.30'
}
response = requests.post(API_URL,data=user)

# get = requests.get(api_key)

# print(get.json())


# import requests
#
# api_url = 'http://127.0.0.1:8000/get/'
#
# data = requests.get(api_url)
# print(data.json())