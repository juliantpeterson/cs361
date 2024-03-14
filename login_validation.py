import time
import zmq
import json

account_list = []
logins_dict = dict()

with open("Login.json", 'r') as file:
    json_file = json.load(file)

print(json_file)

#with open("Login.json", 'w') as file:
#    file.write(json.dumps(sample))
