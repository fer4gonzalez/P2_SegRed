import json
import hashlib
import json
from datetime import datetime, timedelta
from flask import jsonify

def expire_date(min: int):
    #Fecha actual:
    now = datetime.now()
    #Cálculo de la duración del token en segundos
    new_date = now + timedelta(minutes=min)
    return new_date


