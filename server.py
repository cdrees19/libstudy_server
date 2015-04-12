import SimpleHTTPServer, SocketServer
import pymongo
import json
from pymongo import MongoClient

def get_user_groups(user):
    groups = []
    print "running get user groups"
    student = users.find_one({'username':user})
    if(student == None):
            return groups
    else:
        return student['groups']

def get_group_info(groupname):
    group = groups.find_one({'name': groupname})
    info = {}
    if(group == None):
            return "ho"
    else:
        info['name'] = group['name']
        info['description'] = group['description']
        return info

def path_data(self):
    paths=self.path.split('/')
    paths.remove('')
    if(paths[0] == 'groups') & (len(paths) == 2):
        return get_user_groups(paths[1])
    elif(paths[0] == 'group') & (len(paths) == 2):
        print "entered"
        return get_group_info(paths[1])
    else:
        return "no username present"

class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        print "entering get handler"
        self.send_response(200)
        self.send_header("Content-type", "text")
        self.end_headers()
        self.wfile.write(json.dumps(path_data(self)))


print "setting up db"
client = MongoClient()
users = client.test.users
groups = client.test.groups

PORT = 4050
httpd = SocketServer.ThreadingTCPServer(("", PORT), Handler)
print "serving at port", PORT
httpd.serve_forever()
