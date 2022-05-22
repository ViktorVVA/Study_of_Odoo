
HOST = "localhost"
PORT = 8569
#url= "http://localhost:8569"
db = 'o15-learn'
username = 'admin'
password = 'admin'


import xmlrpc.client

root = 'http://%s:%d/xmlrpc/2/' % (HOST, PORT)
print(root)

uid = xmlrpc.client.ServerProxy(root + 'common').login(db, username, password)
print("Logged in as %s (uid: %d)" % (username, uid))

models = xmlrpc.client.ServerProxy(root + 'object')

sessions_ids = models.execute_kw(db, uid, password, 'openacademy.session', 'search',[[]])
sessions_rec = models.execute_kw(db, uid, password, 'openacademy.session', 'read', [sessions_ids], {'fields': ['name', 'seats']})
print("sessions_ids...", sessions_ids)
for session in sessions_rec:
    print(session)

sessions_search_read = models.execute_kw(db, uid, password, 'openacademy.session', 'search_read', [], {'fields':['name', 'seats']})
for session_s_r in sessions_search_read:
    print(session_s_r)
   
args = {'name': "New Session", 'duration': float(10), 'seats': int(5), 'instructor_id': 25, 'course_id': 14}
new_id = models.execute_kw(db, uid, password, 'openacademy.session', 'create', [args])
print(new_id)
