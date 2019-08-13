# -*- coding: utf-8 -*-
from bottle import Bottle, request
from tinydb import where
import jwt
from datetime import datetime, timedelta
from generic_rest_app import GenericRestApp, get_filtered_dict_data, json_response
from settings import db, JWT_SECRET, JWT_ALGORITHM, JWT_EXP_DELTA_SECONDS

# Bottle app
user_bottle_app = Bottle()

# Default user data
default_user = {
    'username': 'admin',
    'password': '1234',
    'name': 'User Name',
    'email': 'user@name.com'
}

# User table
user_table = db.table('users')
if user_table.get(doc_id=1) is None:
    user_table.insert(default_user)
main_user = user_table.get(doc_id=1)


# User Rest App
class UserRestApp(GenericRestApp):

    def __init__(self, bottle_app, db_table, default_data):
        super().__init__(bottle_app, db_table, default_data)

        # Extra rest route methods
        self._bottle_app.post('/login', callback=self._post_login)

    def _post_new_doc(self):
        if request.json:
            json_data = request.json

            # Verify already existing user with same login data
            for key in ['username', 'email']:
                if key in json_data:
                    other_user = self._db_table.get(where(key) == json_data[key])
                    if other_user:
                        return json_response({'message': 'Already Existing User \'%s\'' % json_data[key]}, status=400)

        return super()._post_new_doc()

    def _delete_doc(self, doc_id):
        # Default user cannot be deleted
        if doc_id == 1:
            return json_response({'message': 'Default User Cannot be Deleted'}, status=400)

        super()._delete_doc(doc_id)

    def _put_doc(self, doc_id):
        if request.json:
            json_data = request.json

            # Verify current user
            user = self._db_table.get(doc_id=doc_id)
            if user:
                # Verify already existing user with same login data
                for key in ['username', 'email']:
                    if key in json_data:
                        # Verify other user
                        other_user = self._db_table.get(where(key) == json_data[key])
                        if other_user:
                            if user != other_user:
                                return json_response({'message': 'Already Existing User \'%s\'' % json_data[key]},
                                                     status=400)

        return super()._put_doc(doc_id)

    def _post_login(self):
        # Verify json data
        if request.json:
            json_data = request.json
        else:
            return json_response({'message': 'Not Valid JSON'}, status=400)

        # Verify all data according default keys
        default_keys = ['username', 'password']
        filtered_json_data = get_filtered_dict_data(json_data, default_keys)
        if len(default_keys) != len(filtered_json_data):
            return json_response({'message': 'Not Valid JSON'}, status=400)

        # Verify user
        username = filtered_json_data['username']
        password = filtered_json_data['password']
        user = self._db_table.get((where('username') == username) & (where('password') == password))
        if user:
            # Logged in
            payload = {
                'user_id': user.doc_id,
                'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
            }
            jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
            return json_response({'is_logged_in': True, 'logged_token': jwt_token.decode('utf-8')})
        else:
            return json_response({'message': 'Unauthorized'}, status=401)


# Create User Rest App
user_rest_app = UserRestApp(user_bottle_app, user_table, default_user)
