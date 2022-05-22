
import json
import random
import urllib.request

HOST = "localhost"
PORT = 8569
#url= "http://localhost:8569"

DB = 'o15-learn'
USER = 'admin'
PASS = 'admin'

def json_rpc(url, method, params):
    data = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": random.randint(0, 1000000000),
    }
    req = urllib.request.Request(url=url, data=json.dumps(data).encode(), headers={
        "Content-Type": "application/json",
    })
    reply = json.loads(urllib.request.urlopen(req).read().decode('UTF-8'))
    if reply.get("error"):
        raise Exception(reply["error"])
    return reply["result"]

def call(url, service, method, *args):
    return json_rpc(url, "call", {"service": service, "method": method, "args": args})

# log in the given database
url = "http://%s:%s/jsonrpc" % (HOST, PORT)
uid = call(url, "common", "login", DB, USER, PASS)

print("uid...", uid)
print("url...", url)


sessions_ids = call(url, "object", "execute", DB, uid, PASS, 'openacademy.session', 'search',[])
print(sessions_ids)

for i in range(len(sessions_ids)):
    sessions_read = call(url, "object", "execute", DB, uid, PASS, 'openacademy.session', 'read', [sessions_ids[i]])
    name = sessions_read[0].get('name')
    seats = sessions_read[0].get('seats')
    print("Name: %s, seats: %d" % (name, seats))

args = {'name': "New Session", 'duration': float(10), 'seats': int(5), 'instructor_id': 25, 'course_id': 14}
new_id = call(url, "object", "execute", DB, uid, PASS, 'openacademy.session', 'create', args)
print(new_id)



