from flask import Flask, jsonify
#from auth_token import AuthToken
from flask_restful import reqparse
import flask_restful as rest
from uuid import uuid4
import hashlib


app = Flask(__name__)
api = rest.Api(app)

VERSION = "1.0.0"
EXP_MIN = 5

USERS = {}

luser = []
lpasswd = []

parser = reqparse.RequestParser()
parser.add_argument('username', required=True, help="Username cannot be blank!")
parser.add_argument('password', required=True, help="Password cannot be blank!")

class Version(rest.Resource):
    def get(self):
        return {"version":VERSION}

class Signup(rest.Resource):
    def post(self):
        args = parser.parse_args()
        username = args.username
        password = args.password
        #auth = AuthToken(username, EXP_MIN, password)
        #token = auth.encode("utf-8")
        hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        auth_token = uuid4()
        return token

class Login(rest.Resource):
    def post(self):
        for u in USERS:
            luser.append(u)
            lpasswd.append(USERS[u])
        
        args = parser.parse_args()
        username = args["username"]
        password = args["password"]

        if username in luser:
            if lpasswd[luser.index(username)] == password:
                auth = AuthToken(username, EXP_MIN, password)
                token = auth.encode()
                return {token.token:username}



api.add_resource(Version, "/", "/version")
api.add_resource(Signup, "/signup")
api.add_resource(Login, "/login")

if __name__ == "__main__":
    app.run(debug=True)