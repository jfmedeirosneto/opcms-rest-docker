# -*- coding: utf-8 -*-
from bottle import Bottle, request, BaseRequest, static_file
from PIL import Image, ImageOps
from io import BytesIO
import base64
import os
import uuid
from generic_rest_app import GenericRestApp, json_response, get_filtered_dict_data
from settings import db, app_data_dir

# Set MEMFILE_MAX to upload rawFile in body (10Mb)
BaseRequest.MEMFILE_MAX = 10 * 1024 * 1024

# Image size
THUMB_SIZE = (650, 350)

# Image path
image_dir = os.path.join(app_data_dir, 'images')
if not os.path.exists(image_dir):
    os.makedirs(image_dir)

# Bottle app
portfolio_bottle_app = Bottle()

# Default portfolio data
default_portfolio = {
    'category': 'Category',
    'project_name': 'Project Name',
    'pictures': [
        {
            'id': 'id1',
            'fullsize_url': '/portfolios/public/picture/id1_full.jpg',
            'thumbnail_url': '/portfolios/public/picture/id1_thumb.jpg',
            'title': 'Title'
        },
        {
            'id': 'id2',
            'fullsize_url': '/portfolios/public/picture/id2_full.jpg',
            'thumbnail_url': '/portfolios/public/picture/id2_thumb.jpg',
            'title': 'Title'
        }
    ],
}

# Portfolio table
portfolio_table = db.table('portfolios')


# Find picture by id
def find_picture_by_id(picture_list, picture_id):
    for picture in picture_list:
        if picture['id'] == picture_id:
            return picture
    return None


# Buffer64 to Image
def buffer64_to_image_object(buffer64_data):
    buff = BytesIO(base64.b64decode(buffer64_data))
    return Image.open(buff)


# Portfolio Rest App
class PortfolioRestApp(GenericRestApp):

    def __init__(self, bottle_app, db_table, default_data):
        super().__init__(bottle_app, db_table, default_data)

        # Extra rest route methods
        self._bottle_app.get('/public', callback=self._get_docs)
        self._bottle_app.get('/public/<doc_id:int>', callback=self._get_doc)
        self._bottle_app.route('/public/picture/<filepath:path>', callback=self._route_picture)

    @staticmethod
    def _route_picture(filepath):
        return static_file(filepath, root=image_dir)

    @staticmethod
    def _delete_picture_list(picture_list):
        for picture in picture_list:
            picture_id = picture['id']
            fullsize_file = os.path.join(image_dir, picture_id + '_full.jpg')
            thumbnail_file = os.path.join(image_dir, picture_id + '_thumb.jpg')
            if os.path.exists(fullsize_file):
                os.remove(fullsize_file)
            if os.path.exists(thumbnail_file):
                os.remove(thumbnail_file)

    def _post_new_doc(self):
        # Verify json data
        if request.json:
            json_data = request.json
        else:
            return json_response({'message': 'Not Valid JSON'}, status=400)

        # Verify simple json data
        if ('category' not in json_data) or ('project_name' not in json_data):
            return json_response({'message': 'Not Valid JSON'}, status=400)

        # Initialize empty picture list
        json_data = {'pictures': [], **json_data}

        doc_id = self._db_table.insert(json_data)
        doc = self._db_table.get(doc_id=doc_id)
        return json_response({'id': doc.doc_id, **doc})

    def _put_doc(self, doc_id):
        # Verify json data
        if request.json:
            json_data = request.json
        else:
            return json_response({'message': 'Not Valid JSON'}, status=400)

        # Verify data according default data
        filtered_json_data = get_filtered_dict_data(json_data, self._default_data.keys())
        if len(self._default_data) != len(filtered_json_data):
            return json_response({'message': 'Not Valid JSON'}, status=400)

        # Verify doc
        portfolio_doc = self._db_table.get(doc_id=doc_id)
        if not portfolio_doc:
            return json_response({'message': 'Portfolio \'%d\' Not Found' % doc_id}, status=404)

        # Verify pictures in json_data
        if isinstance(filtered_json_data['pictures'], list):
            # Actual picture list in portfolio_doc
            actual_picture_list = portfolio_doc['pictures']

            # New picture list in json_data
            new_picture_list = [picture for picture in filtered_json_data['pictures'] if 'src' in picture]

            # Retain picture list in json_data
            retain_picture_list = [picture for picture in filtered_json_data['pictures'] if 'id' in picture]

            # Verify deleted pictures
            deleted_picture_list = [picture for picture in actual_picture_list
                                    if not find_picture_by_id(retain_picture_list, picture['id'])]
            self._delete_picture_list(deleted_picture_list)

            # Verify image type and image size
            image_object_list = []
            for picture in new_picture_list:
                # Check image type
                image_type, image_b64 = picture['src'].split(',')
                if (image_type != 'data:image/jpeg;base64') or (image_type == 'data:image/png;base64'):
                    return json_response({'message': 'Image Type \'%s\' Not Supported' % image_type}, status=400)

                # Check image size
                image_object = buffer64_to_image_object(image_b64)
                image_w, image_h = image_object.size
                thumb_w, thumb_h = THUMB_SIZE
                if (image_w < thumb_w) and (image_h < thumb_h):
                    return json_response(
                        {'message': 'Small Image Size (%d x %d) < (%d x %d)' %
                                    (image_w, image_h, thumb_w, thumb_h)}, status=400)

                # Retain image object
                image_object_list.append(image_object)

            # Save image objects
            created_picture_list = []
            for image_object in image_object_list:
                # Save images
                picture_id = uuid.uuid4().hex
                fullsize_file_name = picture_id + '_full.jpg'
                thumbnail_file_name = picture_id + '_thumb.jpg'
                fullsize_file = os.path.join(image_dir, fullsize_file_name)
                thumbnail_file = os.path.join(image_dir, thumbnail_file_name)
                try:
                    # Save images fullsize and thumbnail
                    image_object.save(fullsize_file, "JPEG")
                    thumbnail_image_object = ImageOps.fit(image_object, THUMB_SIZE, Image.ANTIALIAS)
                    thumbnail_image_object.save(thumbnail_file, "JPEG")

                    # Append new picture data
                    created_picture_list.append({
                        'id': picture_id,
                        'fullsize_url': 'portfolios/public/picture/' + fullsize_file_name,
                        'thumbnail_url': 'portfolios/public/picture/' + thumbnail_file_name,
                        'title': '%s - %s' % (filtered_json_data['category'], filtered_json_data['project_name'])
                    })
                except IOError:
                    # Delete all created pictures
                    if os.path.exists(fullsize_file):
                        os.remove(fullsize_file)
                    if os.path.exists(thumbnail_file):
                        os.remove(thumbnail_file)
                    self._delete_picture_list(created_picture_list)

                    return json_response({'message': 'Save Images Failed'}, status=400)

            # New pictures list (retain + created)
            filtered_json_data['pictures'] = [*retain_picture_list, *created_picture_list]
        else:
            filtered_json_data['pictures'] = []

        self._db_table.update(filtered_json_data, doc_ids=[doc_id])
        return json_response({'id': portfolio_doc.doc_id, **filtered_json_data})

    def _delete_doc(self, doc_id):
        # Verify doc
        portfolio_doc = self._db_table.get(doc_id=doc_id)
        if portfolio_doc:
            # Delete all pictures
            self._delete_picture_list(portfolio_doc['pictures'])

        return super()._delete_doc(doc_id)


# Create Portfolio Rest App
portfolio_rest_app = PortfolioRestApp(portfolio_bottle_app, portfolio_table, default_portfolio)
