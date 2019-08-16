from bottle import response, request
import json
import jwt
from settings import JWT_SECRET, JWT_ALGORITHM


def json_response(value, status=200):
    response.status = status
    response.content_type = 'application/json'
    return json.dumps(value)


def check_jwt_authorization(success_func):
    """
    Check JWT authorization wrapper
    :param success_func: Success callback function
    :return: ERROR 401 or callback success function return
    """

    def wrapper(*a, **ka):
        jwt_token = request.headers.get('Authorization', None)
        if jwt_token:
            try:
                jwt.decode(jwt_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                return json_response({'message': 'Unauthorized'}, status=401)
        else:
            return json_response({'message': 'Unauthorized'}, status=401)
        return success_func(*a, **ka)

    return wrapper


def get_filtered_dict_data(dict_data, default_keys):
    """
    Get json data filter by default data keys
    :param dict_data: Dict data
    :param default_keys: Default dict keys
    :return: Filtered dict data by default data keys
    """
    return {key: value for (key, value) in dict_data.items() if key in default_keys}


class GenericRestApp:
    def __init__(self, bottle_app, db_table, default_data):
        self._bottle_app = bottle_app
        self._db_table = db_table
        self._default_data = default_data

        # CORS
        self._bottle_app.add_hook('after_request', self._enable_cors)
        self._bottle_app.route('/<:re:.*>', method='OPTIONS', callback=self._options_generic)

        # Rest route methods
        self._bottle_app.get('/', callback=check_jwt_authorization(self._get_docs))
        self._bottle_app.post('/', callback=check_jwt_authorization(self._post_new_doc))
        self._bottle_app.get('/<doc_id:int>', callback=check_jwt_authorization(self._get_doc))
        self._bottle_app.delete('/<doc_id:int>', callback=check_jwt_authorization(self._delete_doc))
        self._bottle_app.put('/<doc_id:int>', callback=check_jwt_authorization(self._put_doc))
        self._bottle_app.get('/<doc_id:int>/<doc_key>', callback=check_jwt_authorization(self._get_doc_data))
        self._bottle_app.put('/<doc_id:int>/<doc_key>', callback=check_jwt_authorization(self._put_doc_data))

    @staticmethod
    def _enable_cors():
        """Add headers to enable CORS"""
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
        response.headers[
            'Access-Control-Allow-Headers'] = 'Authorization, Origin, Accept, Content-Type, X-Requested-With'
        response.headers['Access-Control-Expose-Headers'] = 'X-Total-Count, Content-Range'
        response.headers['Allow'] = 'PUT, GET, POST, DELETE, OPTIONS'

    @staticmethod
    def _options_generic():
        """
        Generic options request
        :return: 200 OK response
        """
        return json_response({})

    def _get_docs(self):
        """
        Get all docs request
        :return: OK 200 all docs data response
        """
        docs = self._db_table.all()
        response.add_header('X-Total-Count', len(docs))
        response.add_header('Content-Range', len(docs))
        return json_response([{'id': doc.doc_id, **doc} for doc in docs])

    def _post_new_doc(self):
        """
        Post new doc request
        :return: ERROR 400 or OK 200 new doc data response
        """
        # Verify json data
        if request.json:
            json_data = request.json
        else:
            return json_response({'message': 'Not Valid JSON'}, status=400)

        # Verify data according default data
        filtered_json_data = get_filtered_dict_data(json_data, self._default_data.keys())
        if len(self._default_data) != len(filtered_json_data):
            return json_response({'message': 'Not Valid JSON'}, status=400)

        doc_id = self._db_table.insert(filtered_json_data)
        doc = self._db_table.get(doc_id=doc_id)
        return json_response({'id': doc.doc_id, **doc})

    def _get_doc(self, doc_id):
        """
        Get single doc request
        :param doc_id: Doc id
        :return: ERROR 400 or OK 200 doc data response
        """
        # Verify doc
        doc = self._db_table.get(doc_id=doc_id)
        if doc:
            return json_response({'id': doc.doc_id, **doc})
        else:
            return json_response({'message': 'Doc \'%d\' Not Found' % doc_id}, status=404)

    def _delete_doc(self, doc_id):
        """
        Delete single doc request
        :param doc_id: Doc id
        :return: ERROR 400 or OK 200 empty data response
        """
        # Verify doc
        doc = self._db_table.get(doc_id=doc_id)
        if doc:
            self._db_table.remove(doc_ids=[doc_id])
        else:
            return json_response({'message': 'Doc \'%d\' Not Found' % doc_id}, status=404)

        return json_response({})

    def _put_doc(self, doc_id):
        """
        Put single doc data request
        :param doc_id: Doc id
        :return: ERROR 400, 404 or OK 200 doc data response
        """
        # Verify json data
        if request.json:
            json_data = request.json
        else:
            return json_response({'message': 'Not Valid JSON'}, status=400)

        # Verify doc
        doc = self._db_table.get(doc_id=doc_id)
        if doc:
            filtered_json_data = get_filtered_dict_data(json_data, self._default_data.keys())
            self._db_table.update(filtered_json_data, doc_ids=[doc_id])
        else:
            return json_response({'message': 'Doc \'%d\' Not Found' % doc_id}, status=404)

        return json_response({'id': doc.doc_id, **filtered_json_data})

    def _get_doc_data(self, doc_id, doc_key):
        """
        Get single doc data by key request
        :param doc_id: Doc id
        :param doc_key: Doc data
        :return: ERROR 404 or OK 200 doc data by key response
        """
        # Verify doc
        doc = self._db_table.get(doc_id=doc_id)
        if doc is None:
            return json_response({'message': 'Doc \'%d\' Not Found' % doc_id}, status=404)

        # Verify doc key
        if doc_key not in doc:
            return json_response({'message': 'Key \'%s\' Not Found in Doc \'%d\'' % (doc_key, doc_id)}, status=404)

        return json_response({'id': doc.doc_id, doc_key: doc[doc_key]})

    def _put_doc_data(self, doc_id, doc_key):
        """
        Put single doc data by key request
        :param doc_id: Doc id
        :param doc_key: Doc data
        :return: ERROR 400, 404 or OK 200 doc data by key response
        """
        # Verify json data
        if request.json:
            json_data = request.json
        else:
            return json_response({'message': 'Not Valid JSON'}, status=400)

        # Verify doc
        doc = self._db_table.get(doc_id=doc_id)
        if doc is None:
            return json_response({'message': 'Doc \'%d\' Not Found' % doc_id}, status=404)

        # Verify doc key in doc
        if doc_key not in doc:
            return json_response({'message': 'Key \'%s\' Not Found in Doc \'%d\'' % (doc_key, doc_id)}, status=404)

        # Verify doc key in json data
        filtered_json_data = get_filtered_dict_data(json_data, self._default_data.keys())
        if doc_key not in filtered_json_data:
            return json_response({'message': 'Key \'%s\' Not Found in JSON \'%d\'' % (doc_key, doc_id)}, status=404)

        self._db_table.update({doc_key: filtered_json_data[doc_key]}, doc_ids=[doc_id])
        return json_response({'id': doc.doc_id, doc_key: filtered_json_data[doc_key]})
