from mimetypes import init
from flask import Flask, jsonify, request
from flask_restful import reqparse
import flask_restful as rest
from uuid import uuid4
import json
import hashlib
import os
from datetime import datetime, timedelta


app = Flask(__name__)
api = rest.Api(app)

#Versión del programa
VERSION = "1.0.0"
#Tiempo de expiración del token en segundos (300s = 5min)
EXP_SEC = 300
#Caracteres especiales que no puede contener username y doc_id
SPECIAL_CHARS = " \ºª|@#~½¬!·$%&/()=?´`+ç{-,;:¨"
#Lista de diccionarios en los que se guardaran los tokens asociados a cada usuario junto con el tiempo de expiracion
dictionary_list=[]

#Argumentos para signup y login
parser = reqparse.RequestParser()
parser.add_argument('username', required=True, help="Username cannot be blank!")
parser.add_argument('password', required=True, help="Password cannot be blank!")

#Argumentos para FileManager
doc_parser = reqparse.RequestParser()
doc_parser.add_argument('doc_content',required=True)

#-------------------------------- INICIALIZACION --------------------------------#
        
def __init__():
    if not os.path.exists("users"):
        try:
            os.mkdir("users")
        except OSError:
            print("Error. The users directory could not be created")
            return -1
    #Código añadido para las pruebas, para que cada vez que se inicie la aplicacion se borre el contenido de .shadow      
    '''
    if not os.path.exists(".shadow"):
        file=open(".shadow","w")
        file.close()
    else:
        file = open(".shadow", "w")
        file.write("")
        file.close()
    '''

#-------------------------------- MÉTODOS ÚTILES --------------------------------#
#Método que comprueba si hay caracteres especiales en la cadena que se le pasa por parametro
def chk_string(string):
    if any(c in SPECIAL_CHARS for c in string):
        return True
    else:
        return False

#Método que comprueba si existe el usuario pasado por parámetros en el archivo .shadow.
def exists_user(username,file):
    count = 0
    lines = file.readlines()
    for line in lines:
        if username in line:
            file.close()
            count=count+1
            return True
    if(count == 0):
        return False

#Método que obtiene el token del usuario en la lista de diccionarios "dictionary_list".
def get_user_token(username):
    for i in range(0,len(dictionary_list)):
        if username in dictionary_list[i].values():
            return dictionary_list[i]["token"], i
        else:
            return None

#Método que calcula la hora en la que el token expirará
def expire_date(sec:int):
    #Fecha actual:
    now = datetime.now()
    #Cálculo de la duración del token en segundos
    new_date = now + timedelta(seconds=sec)
    return new_date

#Método que añade a la lista de diccionarios el diccionario de un usuario con su token y el tiempo de caducidad de este
def dictionary_adder(username,auth_token):
    counter = 0
    if(len(dictionary_list)==0):
        dictionary_list.append({'username':username, 'token': auth_token, 'exp': expire_date(EXP_SEC)})
    else:
        for i in range(0,len(dictionary_list)):
            if username in dictionary_list[i].values():
                dictionary_list[i].update({'token': auth_token})
                dictionary_list[i].update({'exp': expire_date(EXP_SEC)})
                counter = counter +1
                
        if counter == 0:
            dictionary_list.append({'username':username, 'token': auth_token, 'exp': expire_date(EXP_SEC)})
    return 0

#Método que comprueba la petición, orientado sobre todo a la validez del token
def chk_request(username,doc_id):
    if(username == "" or doc_id == ""):
            return {"message":"None values are not supported"}, 400
    if (chk_string(username)):
        return {"message":"Error, username cannot contain special characters"}, 400
    if (chk_string(doc_id)):
        return {"message":"Error, doc_id cannot contain special characters"}, 400

    file = open(".shadow",'r')
    auth=request.headers.get('Authentication')
    if auth != None:
        type,token = auth.split(" ",1)
        if(exists_user(username,file)==True):
            if(type=="token"):
                st_token,pos = get_user_token(username)
                if(str(st_token) == None):
                    return {"message":"Invalid token"}
                    file.close()
                if(st_token == token):
                    now = datetime.now()
                    token_expiration_date = dictionary_list[pos]['exp']
                    time_diff = token_expiration_date - now
                    if(time_diff.seconds < EXP_SEC):
                        return True
                        file.close()
                    else:
                        return ({"message":"Error. Token expired"}), 410
                        file.close()
                else:
                    return ({"message":"Error. Token does not match user"}), 400
                    file.close()
            else:
                return ({"message":"Error on request header"}), 400
                file.close()
        else:
            return ({"message":"Error. User not found"}), 404
            file.close()
    else:
        return ({"message":"Error. Missing authentication header"}), 401
        file.close()


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

#Métoo que escribe el contenido pasado en la variable content en el archivo indicado en path
def file_wr(path,content):
        with open(path, 'w') as outfile:
            json.dump(content, outfile)
            return outfile.tell()


#-------------------------------- API RESOURCES --------------------------------#

class Version(rest.Resource):
    #GET: devuelve la versión del programa.
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
        if(username == "" or password == ""):
            return {"message":"None values are not supported"}, 400
        if(chk_string(username)):
            return {"message":"Error, username cannot contain special characters"}, 400
        file =open(".shadow",'+r') #Apertura del archivo

        if(exists_user(username,file)==False):
            hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
            content = username + " : " + hash + "\n"
            file.write(content)
            auth_token = str(uuid4())
            token_msg = {"access_token": auth_token}
            dictionary_list.append({'username':username, 'token': auth_token, 'exp': expire_date(EXP_SEC)})
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

        if(username == "" or password == ""):
            return {"message":"None values are not supported"}, 400
        if(chk_string(username)):
            return {"message":"Error, username cannot contain special characters"}, 400

        lines = file.readlines()
        for line in lines:
            if username in line:
                blocks = line.split()
                if(hash == blocks[2]):
                    file.close()
                    auth_token = str(uuid4())
                    token_msg = {"access_token": auth_token}
                    dictionary_adder(username,auth_token)
                    return jsonify(token_msg)
                else:
                    file.close()
                    return {"message": "Incorrect user or password"}, 403

        file.close()

        return {"message": "Incorrect user or password"}, 403

class FileManager(rest.Resource):
    '''
    Todas las operaciones requieren autenticación mediante la cabecera Authentication cuyo valor debe tener el formato: 
    token <token-del-usuario>. 
    
    GET: obtiene el contenido del documento doc_id del usuario username.Si todo va bien, devuelve el contenido íntegro 
    del documento en formato JSON.
    '''
    def get(self,username,doc_id):
        #breakpoint()
        #dictionary_list.append({'username':"aaron", 'token': "12345a", 'exp': api_functions.expire_date(EXP_SEC)})
        valid_rq = chk_request(username,doc_id)
        if(valid_rq == True):
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
            return valid_rq

    '''
    POST: crea un nuevo documento con identificador doc_id en el usuario username. Necesita los siguientes argumentos:
    -doc_content: el contenido del documento a crear en formato JSON.
    Si todo va bien, devuelve el número de bytes escritos en disco con el formato: {"size": <total_bytes>}
    '''
    def post(self,username,doc_id):
        #breakpoint()
        valid_rq = chk_request(username,doc_id)
        if(valid_rq==True):
            path="users/"+username+"/"+doc_id
            if(os.path.exists(path)==False):
                root, extension = os.path.splitext(path)
                if(extension != ".json"):
                    return  {"message":"File extension must be .json"}, 400

                args=doc_parser.parse_args()
                doc_content=args['doc_content']
                if(os.path.exists("users/"+username)==False):
                    os.mkdir('users/'+username)
                    return {"size": file_wr(path,doc_content)}
                else:
                    return {"size": file_wr(path,doc_content)}

            else:
                return {"message":"Error. File already exists"},406
        else: 
            return valid_rq

                
        return 0

    '''
    PUT: actualiza el contenido del documento doc_id del usuario username.Necesita los siguientes argumentos:
    -doc_content: nuevo contenido del documento en formato JSON.
    Si todo va bien, devuelve el número de bytes escritos en disco con el formato: {"size": <total_bytes>}
    '''
    def put(self,username,doc_id):
        valid_rq=chk_request(username,doc_id)
        if(valid_rq==True):
            path="users/"+username+"/"+doc_id
            if(os.path.exists(path)==True):
                args=doc_parser.parse_args()
                doc_content=args['doc_content']
                file_wr(path,"")
                return {"size": file_wr(path,doc_content)}
            else:
                return {"message":"File not found. Can not update"},404
        else:
            return valid_rq

    '''
    DELETE: borra el documento doc_id del usuario username. Si todo va bien, devuelve una respuesta vacía:
    {}
    '''
    def delete(self,username,doc_id):
        valid_rq=chk_request(username,doc_id)
        if(valid_rq==True):
            path = "users/"+username+"/"+doc_id
            if(os.path.exists(path)):
                os.remove(path)
                return {}
            else:
                return {"message":"Error. File not found"}, 404
        else:
            return valid_rq


api.add_resource(Version, "/", "/version")
api.add_resource(Signup, "/signup")
api.add_resource(Login, "/login")
api.add_resource(FileManager, "/<string:username>/<string:doc_id>")

if __name__ == "__main__":
    __init__()
    app.run(debug=True,ssl_context=("cert.pem","key.pem"))