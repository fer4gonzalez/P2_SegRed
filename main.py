from flask import Flask, jsonify, request
from auth_token import AuthToken
from flask_restful import reqparse
import flask_restful as rest
from uuid import uuid4
from dotenv import load_dotenv
from function_token import write_token
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
        #breakpoint()
        args = parser.parse_args() #Parseo de los argumentos
        username = args.username
        password = args.password
        file =open(".shadow",'+r') #Apertura del archivo

        lines = file.readlines()
        for line in lines:
            if username in line:
                file.close()
                return {"message": "User already exists"}, 409

        auth = AuthToken(username, EXP_MIN, password)
        #token = auth.encode()
        hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        content = username + " : " + hash + "\n"
        file.write(content)
        auth_token = jsonify(uuid4())
        file.close()
        return auth_token

class Login(rest.Resource):
    def post(self):
        #breakpoint()
        args = parser.parse_args()
        username = args.username
        password = args.password
        hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        file = open(".shadow", 'r')

        lines = file.readlines()
        for line in lines:
            if username in line:
                blocks = line.split()
                if(hash == blocks[3]):
                    file.close()
                    return {"message": "Login success"}, 200
                else:
                    file.close()
                    return {"message": "Incorrect user or password"}, 403

        file.close()
        return {"message": "Incorrect user or password"}, 403

        '''
        FERNANDO:
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
        '''


api.add_resource(Version, "/", "/version")
api.add_resource(Signup, "/signup")
api.add_resource(Login, "/login")

if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True)