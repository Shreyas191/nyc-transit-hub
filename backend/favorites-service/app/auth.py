import firebase_admin
from firebase_admin import auth, credentials
from flask import request, jsonify

from functools import wraps
from flask import request

cred = credentials.Certificate('path/to/serviceAccountKey.json')
firebase_admin.initialize_app(cred)

def verify_token(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Missing token"}), 401
        try:
            decoded_token = auth.verify_id_token(token)
            request.firebase_uid = decoded_token['uid']
        except:
            return jsonify({"error": "Invalid token"}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper
