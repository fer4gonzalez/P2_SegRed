import os
import json
import httplib2
from wsgiref import headers
import requests
import shutil
import urllib3

urllib3.disable_warnings()

URL = 'https://myserver.local:5000'
PORT = '5000'
URL_SIGNUP = 'https://myserver.local:5000/signup'
URL_LOGIN = 'https://myserver.local:5000/login'
HEADERS = {'Content-Type': 'application/json'}

CONTINUE = True

def version():
    resp = requests.get(URL+"/version", verify = False)
    print("\n\n")
    print(resp.json())
    print("\n\n")

def signup():
    print("Enter a new username")
    username = input()
    print("Enter your new password")
    password = input()
    print("\n")
    data = '{"username":"'+username+'", "password":"'+password+'"}'
    
    try:
        resp = requests.post( URL_SIGNUP, headers = HEADERS, data = data, verify = False)
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
    print("\n")
    data = '{"username":"'+username+'", "password":"'+password+'"}'
    
    try:
        resp = requests.post( URL_LOGIN, headers = HEADERS, data = data, verify=False)
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
        print("\n")
        get_url = URL + "/"+username+"/"+doc_id
        string_auth= "token "+token
        auth_header = {'Authentication': string_auth}
        global HEADERS
        HEADERS = {**HEADERS,**auth_header}

        try:
            resp = requests.get( get_url, headers = HEADERS, verify = False)
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
        print("\n")
        data = '{"doc_content":{"message": "'+content+'"}}'
        post_url = URL + "/"+username+"/"+doc_id
        string_auth= "token "+token
        auth_header = {'Authentication': string_auth}
        global HEADERS
        HEADERS = {**HEADERS,**auth_header}

        try:
            resp = requests.post( post_url, headers = HEADERS, data = data, verify = False)
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
        print("\n")
        data = '{"doc_content":{"message": "'+content+'"}}'
        put_url = URL + "/"+username+"/"+doc_id
        string_auth= "token "+token
        auth_header = {'Authentication': string_auth}
        global HEADERS
        HEADERS = {**HEADERS,**auth_header}

        try:
            resp = requests.put( put_url, headers = HEADERS, data = data, verify = False)
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
        print("\n")
        delete_url = URL + "/"+username+"/"+doc_id
        string_auth= "token "+token
        auth_header = {'Authentication': string_auth}
        global HEADERS
        HEADERS = {**HEADERS,**auth_header}

        try:
            resp = requests.delete(delete_url, headers = HEADERS, verify = False)
            print(resp.json())
            print("\n\n")

        except Exception as e:
            print( 'Exception >> ' + type(e).__name__ )
            raise e 
def resetAPI():
    
    if not os.path.exists("users"):
        try:
            os.mkdir("users")
        except OSError:
            print("Error. The users directory could not be created")
            return -1
    else:
        try:
            shutil.rmtree("users")
            os.mkdir("users")
        except OSError as e:
            print(e)
        else:
            print("Directory is deleted successfully")


    if not os.path.exists(".shadow"):
        file=open(".shadow","w")
        file.close() 
    else:
        file = open(".shadow", "w")
        file.write("")
        file.close()

def main():
    #breakpoint()
    print("Practica 2 Seguridad en Redes 2022\nWhat do you want to do? \n0. Show app version\n1. Signup\n2. Login\n3. Get the contents of a file \n4. Create a file \n5. Change the contents of a file \n6. Delete file \n7. Reset API \n8. Exit")
    option = input()
    if option == "0":
        version()
    elif option == "1":
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
        resetAPI()
    elif option == "8":
        global CONTINUE
        CONTINUE = False
        print("Script finished")
    return 0

if __name__ == "__main__":
    #breakpoint()
    while(CONTINUE==True):
        main()