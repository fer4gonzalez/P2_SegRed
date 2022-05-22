import os
import json

def signup():
    print("Enter a new username")
    username = input()
    print("Enter your new password")
    password = input()
    jsonData = '{"username":{username}, "password":{password}}'
    jsonToPython = json.loads(jsonData)
    print(str)
    #os.system(curl http://myserver.local:5000/signup -d '{"username":"Iria SolerMaaasdfart", "password":"segred2022"}' -X POST -H 'Content-Type: application/json')

    return 0

def login():
    username = input('Username:')
    password = input('Password')
    return 0 

def main():
    #breakpoint()
    print("Practica 2 Seguridad en Redes 2022\nWhat do you want to do? \n1. Signup\n2. Login\n")
    option = input()
    if option == "1":
        signup()
    elif option == "2":
        login()

    return 0

if __name__ == "__main__":
    main()