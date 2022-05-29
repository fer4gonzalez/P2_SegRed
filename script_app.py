import os
import json
import httplib2
from wsgiref import headers
import requests

URL = 'http://myserver.local:5000'
PORT = '5000'
URL_SIGNUP = 'http://myserver.local:5000/signup'
URL_LOGIN = 'http://myserver.local:5000/login'
HEADERS = {'Content-Type': 'application/json'}

CONTINUE = True

def signup():
    print("Enter a new username")
    username = input()
    print("Enter your new password")
    password = input()
    print("\n\n")
    data = '{"username":"'+username+'", "password":"'+password+'"}'
    
    try:
        resp = requests.post( URL_SIGNUP, headers = HEADERS, data = data)
        print(resp.json())
        print("\n\n")

    except Exception as e:
        print( 'Exception >> ' + type(e).__name__ )
        raise e


def login():
    print("Enter your username")
    username = input()
    print("Enter your password")
    password = input()
    print("\n\n")
    data = '{"username":"'+username+'", "password":"'+password+'"}'
    
    try:
        resp = requests.post( URL_LOGIN, headers = HEADERS, data = data)
        print(resp.json())
        print("\n\n")

    except Exception as e:
        print( 'Exception >> ' + type(e).__name__ )
        raise e 


class FileManager():
    def get():
        #breakpoint()
        print("Enter your username")
        username = input()
        print("Enter the document id")
        doc_id = input()
        print("Enter your token")
        token = input()
        get_url = URL + "/"+username+"/"+doc_id
        string_auth= "token "+token
        auth_header = {'Authentication': string_auth}
        global HEADERS
        HEADERS = {**HEADERS,**auth_header}

        try:
            resp = requests.get( get_url, headers = HEADERS)
            print(resp.json())
            print("\n\n")

        except Exception as e:
            print( 'Exception >> ' + type(e).__name__ )
            raise e 

    
    def post():
        print("Enter your username")
        username = input()
        print("Enter the document id")
        doc_id = input()
        print("Enter your token")
        token = input()
        print("Enter file content")
        content = input()
        data = '{"doc_content":{"message": "'+content+'"}}'
        post_url = URL + "/"+username+"/"+doc_id
        string_auth= "token "+token
        auth_header = {'Authentication': string_auth}
        global HEADERS
        HEADERS = {**HEADERS,**auth_header}

        try:
            resp = requests.post( post_url, headers = HEADERS, data = data)
            print(resp.json())
            print("\n\n")

        except Exception as e:
            print( 'Exception >> ' + type(e).__name__ )
            raise e 
        
    def put():
        print("Enter your username")
        username = input()
        print("Enter the document id")
        doc_id = input()
        print("Enter your token")
        token = input()
        print("Enter new file content")
        content = input()
        data = '{"doc_content":{"message": "'+content+'"}}'
        put_url = URL + "/"+username+"/"+doc_id
        string_auth= "token "+token
        auth_header = {'Authentication': string_auth}
        global HEADERS
        HEADERS = {**HEADERS,**auth_header}

        try:
            resp = requests.put( put_url, headers = HEADERS, data = data)
            print(resp.json())
            print("\n\n")

        except Exception as e:
            print( 'Exception >> ' + type(e).__name__ )
            raise e 
        
    def delete():
        print("Enter your username")
        username = input()
        print("Enter the document id")
        doc_id = input()
        print("Enter your token")
        token = input()
        delete_url = URL + "/"+username+"/"+doc_id
        string_auth= "token "+token
        auth_header = {'Authentication': string_auth}
        global HEADERS
        HEADERS = {**HEADERS,**auth_header}

        try:
            resp = requests.delete(delete_url, headers = HEADERS)
            print(resp.json())
            print("\n\n")

        except Exception as e:
            print( 'Exception >> ' + type(e).__name__ )
            raise e 

def main():
    #breakpoint()
    print("Practica 2 Seguridad en Redes 2022\nWhat do you want to do? \n1. Signup\n2. Login\n3. Obtener contenido de un archivo \n4. Crear un archivo \n5. Cambiar el contenido de un archivo \n6. Borrar archivo \n7.Exit")
    option = input()
    if option == "1":
        signup()
    elif option == "2":
        login()
    elif option == "3":
        FileManager.get()
    elif option == "4":
        FileManager.post()
    elif option == "5":
        FileManager.put()
    elif option == "6":
        FileManager.delete()
    elif option == "7":
        global CONTINUE
        CONTINUE = False
        print("Programa finalizado")
    return 0

if __name__ == "__main__":
    #breakpoint()
    while(CONTINUE==True):
        main()