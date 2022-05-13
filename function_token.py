from jwt import encode, decode
from jwt import exceptions
from os import getenv
from datetime import datetime, timedelta
from flask import jsonify


def expire_date(seconds: int):
    #Fecha actual:
    now = datetime.now()
    #Cálculo de la duración del token en segundos
    new_date = now + timedelta.seconds(seconds)

def write_token(data:dict):
    token = encode(payload={**data,"exp": expire_date(5)}, key=getenv("SECRET"),algorithm="HS256")
    return token.encode("UF-8)")

def validate_token(token, output = False):
    try:
        if output:
            return decode(token,key=getenv("SECRET"),algorithms="HS256")
        decode(token,key=getenv("SECRET"),algorithms="HS256")
    except exceptions.DecodeError:
        response = jsonify({"message": "Invalid Token"})
        response.status_code = 401
        return response
    except exceptions.ExpiredSignatureError:
        response = jsonify({"message": "Token Expired"})
        response.status_code = 401
        return response
