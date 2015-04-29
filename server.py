import SimpleHTTPServer, SocketServer
import pymongo
import json
from pymongo import MongoClient
import string

#{"name": (name), "username": (username), "email": (email), 
# "groups": [(group1), ..., (groupN)], "numgroups": (int),
# "school": (school)
#}

def get_user_info(username):
    info = {}
    print "running get user info"
    student = users.find_one({'username': username})
    if(student == None):
            return "NULL"
    else:
        info['name'] = student['name']
        info['groups'] = student['groups']
        info['username'] = student['username']
        info['email'] = student['email']
        info['numgroups'] = len(info['groups'])
        info['school'] = "University of Wisconsin - Madison"
        return info

#{"groupid": (groupid), "name": (name), "description": (description), 
# "members": [(member1), (member2), (member3), (member4)...(memberN)], 
# "pastMeetings": [(meeting1), ... , (meetingN)], 
# "futureMeetings": [(meeting1),..., (meetingN)]
#}
def get_group_info(groupid):
    groupid = string.replace(groupid, "%20", " ")
    print groupid
    group = groups.find_one({'name':groupid})
    info = {}
    if(group == None):
            return "NULL"
    else:
        info['name'] = group['name']
        info['description'] = group['description']
        info['members'] = group['members']
        info['pastMeetings'] = group['pastMeetings']
        info['futureMeetings'] = group['futureMeetings']
        return info


#{"subject": (subject), "instructor": (instructor), "name": (name), 
# "number": (number), "term" (term)}

def get_one_course_info(subject, courseno):
    course = courses.find_one({'subject': subject, 'number': courseno})
    info = {}
    if(course == None):
            return "NULL"
    else:
        info['subject'] = course['subject']
        info['instructor'] = course['instructor']
        info['name'] = course['name']
        info['number'] = course['number']
        info['term'] = course['term']
        return info

#[{course1 info}, {course2 info}, ... , {course3 info}] 

def get_all_subject_courses(subject):
    course = courses.find({'subject': subject}, {'_id': 0})
    courselist = []
    if(course == None):
        return "NULL"
    for x in range(0, course.count()):
        courselist.append(course[x])
    return courselist

def get_all_courses():
    course = courses.find({}, {'_id': 0})
    courselist = []
    if(course == None):
        return "NULL"
    print "about to loop courses"
    for x in range(0, course.count()):
        courselist.append(course[x])
        print "LOOP"
        print courselist
    return courselist

def get_course_groups(subject, courseno):
    group = groups.find({'subject': subject, 'number': courseno}, {'_id': 0})
    grouplist = []
    if(group == None):
        return "NULL"
    else:
        for x in range(0, group.count()):
            grouplist.append(group[x])

        return grouplist

def path_data(self):
    paths=self.path.split('/')
    paths.remove('')
    print len(paths)
    if(paths[0] == 'users') & (len(paths) == 1):
        print "getting user info"
        return get_user_info(paths[1])
    elif(paths[0] == 'groups') & (len(paths) == 1):
        print "getting all groups"
        return get_all_groups())
    elif(paths[0] == 'groups') & (len(paths) == 2):
        print "getting group info"
        return get_group_info(paths[1])
    elif(paths[0] == 'posts') & (len(paths) == 1):
        print "getting all posts"
        return get_all_posts()
    else:
        return "incorrect path"

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
courses = client.test.courses

PORT = 4050
httpd = SocketServer.ThreadingTCPServer(("", PORT), Handler)
print "serving at port", PORT
httpd.serve_forever()

