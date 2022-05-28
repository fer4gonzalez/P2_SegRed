from mimetypes import init
from flask import Flask, jsonify, request
from flask_restful import reqparse
import flask_restful as rest
from uuid import uuid4
import json
import api_functions
import hashlib
import os
from datetime import datetime, timedelta


app = Flask(__name__)
api = rest.Api(app)

VERSION = "1.0.0"
EXP_SEC = 300


#Lista de diccionarios en los que se guardaran los tokens asociados a cada usuario junto con el tiempo de expiracion
dictionary_list=[]

parser = reqparse.RequestParser()
parser.add_argument('username', required=True, help="Username cannot be blank!")
parser.add_argument('password', required=True, help="Password cannot be blank!")
#parser.add_argument('token', location='headers')

doc_parser = reqparse.RequestParser()
doc_parser.add_argument('doc_content',required=True)

#--------------------------------MÉTODOS ÚTILES--------------------------------#
def exists_user(username):
    count = 0
    file =open(".shadow",'+r') #Apertura del archivo
    lines = file.readlines()
    for line in lines:
        if username in line:
            file.close()
            count=count+1
            return True
    if(count == 0):
        return False

def get_user_token(username):
    for i in range(0,len(dictionary_list)):
        if username in dictionary_list[i].values():
            return dictionary_list[i]["token"], i
        else:
            return None

def chk_request(username,doc_id):
    auth=request.headers.get('Authentication')
    if auth != None:
        type,token = auth.split()
        if(exists_user(username)==True):
            if(type=="token"):
                st_token,pos = get_user_token(username)
                if(str(st_token) == None):
                    return {"message":"Invalid token"}
                if(st_token == token):
                    now = datetime.now()
                    token_expiration_date = dictionary_list[pos]['exp']
                    time_diff = token_expiration_date - now
                    if(time_diff.seconds < EXP_SEC):
                        return True
                    else:
                        return ({"message":"Error.Token expired"}), 410
                else:
                    return ({"message":"Error.Invalid token"}), 400
            else:
                return ({"message":"Error on request header"}), 400
        else:
            return ({"message":"Error. User not found"}), 404
    else:
        return ({"message":"Error. Missing authentication header"}), 401

    return 0

#Método que devuelve todos los archivos de un usuario
def get_all_docs(username):
    all_docs={}
    path = "users/"+username
    content = os.listdir(path)
    if len(content) > 0:
        for doc in content:
            doc_path = path + "/" + doc
            data = json.load(open(doc_path))
            all_docs[doc] = data
        return all_docs
    else:
        return None

'''
def json_validator(data):
    try:
        json.loads(data)
        return True
    except ValueError as error:
        print("invalid json: %s" % error)
        return False
'''
def chk_json_extension(doc_id):
    try:
        y=doc_id.split(".")
        if len(y) == 2 and y[1] == "json":
            return True
    except:
        return False
    return False

def file_wr(path,content):
        with open(path, 'w') as outfile:
                json.dump(content, outfile)
                return outfile.tell()

# ----- INICIALIZACION -----
        
def __init__():
    if not os.path.exists("users"):
        try:
            os.mkdir("users")
        except OSError:
            print("Error. The users directory could not be created")
            return -1
            
    if not os.path.exists(".shadow"):
        file=open(".shadow","w")
        file.close()
    else:
        file = open(".shadow", "w")
        file.write("")
        file.close()
#--------------------------------API RESOURCES--------------------------------#

class Version(rest.Resource):
    def get(self):
        return {"version":VERSION}

class Signup(rest.Resource):
    def post(self):
        #breakpoint()
        '''
        Esta funcion extrae los parametros que se pasan a traves de curl "usuario y contraseña", recorre el archivo .shadow para 
        comprobar si ya existe un usuario con el mismo nombre. Si no lo hay, se aplica un hash a la contraseña y se escribe en el
        archivo el nuevo usuario y su hash con la siguiente estructura: "username : hash". A continuacion, se crea un token de auten-
        ticacion que se almacenara junto con el nombre de usuario y la hora en la que caduca en un diccionario dentro de dictionary_list
        y por ultimo lo devuelve.
        '''

        args = parser.parse_args() #Parseo de los argumentos
        username = args.username
        password = args.password
        file =open(".shadow",'+r') #Apertura del archivo

        if(exists_user(username)==False):
            hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
            content = username + " : " + hash + "\n"
            file.write(content)
            auth_token = str(uuid4())
            token_msg = {"access_token": auth_token}
            dictionary_list.append({'username':username, 'token': auth_token, 'exp': api_functions.expire_date(EXP_SEC)})
            file.close()
        else:
            return {"message": "User already exists"}, 409

        return jsonify(token_msg)

class Login(rest.Resource):
    def post(self):
        #breakpoint()
        '''
        Esta funcion extrae los parametros que se pasan a traves de curl "usuario y contraseña", aplica el hash a la contraseña
        y recorre el archivo .shadow en busca del usuario introducido. Si lo encuentra, compara el hash de la contraseña proporcionada
        con la asociada a ese usuario en el archivo, y si coinciden se crea el token de autenticacion. Si en la misma sesion
        se ha hecho login con el mismo usuario, solamente actualizamos el token en el diccionario correspondiente de la lista 
        de diccionarios, pero si no se ha hecho login con ese usuario, añadimos la informacion de username, token y tiempo de expiracion
        al diccionario.
        '''

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
                    auth_token = str(uuid4())
                    token_msg = {"access_token": auth_token}
                    if(len(dictionary_list)==0):
                        dictionary_list.append({'username':username, 'token': auth_token, 'exp': api_functions.expire_date(EXP_SEC)})
                    else:
                        for i in range(0,len(dictionary_list)):
                            if username in dictionary_list[i].values():
                                dictionary_list[i].update({'token': auth_token})
                                counter = counter +1
                                
                        if counter == 0:
                            dictionary_list.append({'username':username, 'token': auth_token, 'exp': api_functions.expire_date(EXP_SEC)})
                        
                    print(dictionary_list)
                    return jsonify(token_msg)
                else:
                    file.close()
                    return {"message": "Incorrect user or password"}, 403

        file.close()

        return {"message": "Incorrect user or password"}, 403

class FileManager(rest.Resource):
    def get(self,username,doc_id):
        breakpoint()
        dictionary_list.append({'username':"aaron", 'token': "12345a", 'exp': api_functions.expire_date(EXP_SEC)})
        valid = chk_request(username,doc_id)
        if(valid == True):
            path="users/"+username+"/"+doc_id
            if(doc_id=="_all_docs"):
                all_docs = get_all_docs(username)
                if(all_docs != None):
                    return all_docs
                else:
                    return {"message":"No docs found in this user directory"},404
            try:
                with open(path) as file:
                    data = json.load(file)
                    return data
            except FileNotFoundError:
                return {"message":"Error. File not found"}, 404
        else:
            return valid


    def post(self,username,doc_id):
        breakpoint()
        valid = chk_request(username,doc_id)
        if(valid==True):
            path="users/"+username+"/"+doc_id
            if(os.path.exists(path)==False):
                root, extension = os.path.splitext(path)
                if(extension != ".json"):
                    return  {"message":"File extension must be .json"}, 400
                args=doc_parser.parse_args()
                doc_content=args['doc_content']
                if(os.path.exists("users/"+username)==False):
                    os.mkdir('users/'+username)
                else:
                    return {"size": file_wr(path,doc_content)}
            else:
                return {"message":"Error. File already exists"},406
        else: 
            return valid

                
        return 0
    def put(self):
        return 0
    def delete(self):
        return 0

api.add_resource(Version, "/", "/version")
api.add_resource(Signup, "/signup")
api.add_resource(Login, "/login")
api.add_resource(FileManager, "/<string:username>/<string:doc_id>")

if __name__ == "__main__":
    __init__()
    app.run(debug=True)