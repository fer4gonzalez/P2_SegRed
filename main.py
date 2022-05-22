from flask import Flask, jsonify, request
from flask_restful import reqparse
import flask_restful as rest
from uuid import uuid4
import function_token
import hashlib


app = Flask(__name__)
api = rest.Api(app)

VERSION = "1.0.0"
EXP_MIN = 5

dictionary_list=[]

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

        hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        content = username + " : " + hash + "\n"
        file.write(content)
        auth_token = uuid4()
        dictionary_list.append({'username':username, 'token': auth_token, 'exp': function_token.expire_date(5)})
        file.close()
        return jsonify(auth_token)

class Login(rest.Resource):
    def post(self):
        #breakpoint()
        args = parser.parse_args()
        username = args.username
        password = args.password
        hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        file = open(".shadow", 'r')
        counter = 0

        lines = file.readlines()
        for line in lines:
            if username in line:
                blocks = line.split()
                if(hash == blocks[3]):
                    file.close()
                    auth_token = uuid4()
                    if(len(dictionary_list)==0):
                        dictionary_list.append({'username':username, 'token': auth_token, 'exp': function_token.expire_date(5)})
                    else:
                        for i in range(0,len(dictionary_list)):
                            if username in dictionary_list[i].values():
                                dictionary_list[i].update({'token': auth_token})
                                counter = counter +1
                                print("Estoy dentro del if")
                        if counter == 0:
                            dictionary_list.append({'username':username, 'token': auth_token, 'exp': function_token.expire_date(5)})
                        
                    print(dictionary_list)
                    return jsonify(auth_token)
                else:
                    file.close()
                    return {"message": "Incorrect user or password"}, 403

        file.close()

        return {"message": "Incorrect user or password"}, 403


api.add_resource(Version, "/", "/version")
api.add_resource(Signup, "/signup")
api.add_resource(Login, "/login")

if __name__ == "__main__":
    app.run(debug=True)