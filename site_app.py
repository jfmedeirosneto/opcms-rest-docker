# -*- coding: utf-8 -*-
from bottle import Bottle
from generic_rest_app import GenericRestApp, json_response
from settings import db

# Bottle app
site_bottle_app = Bottle()

# Default site data
default_site = {
    'name': 'Name',
    'site_title': 'Title',
    'site_description': 'Description\nDescription\nDescription',
    'site_copyright': 'Copyright',
    'page_title': 'Page',
    'page_content': 'Content\nContent\nContent',
    'owner_name': 'Owner Name',
    'owner_email': 'Owner Email',
    'owner_address': 'Address\nAddress\nAddress',
    'owner_map_url': 'https://goo.gl/maps/Fxpy9',
    'owner_phones': ['+001(12)12345-1234', '+55(12)12345-1234'],
    'owner_whatsapp_phones': ['+001(12)12345-1234', '+55(12)12345-1234'],
    'owner_facebook_url': 'https://www.facebook.com/facebook',
    'owner_twitter_url': 'https://twitter.com/twitter',
    'owner_instagram_url': 'https://www.instagram.com/instagram/',
    'template_dir': 'templates/startbootstrap-creative-gh-pages',
    'template_file': 'template.html',
    'template_assets': ['css', 'img', 'js', 'vendor']
}

# Site table
site_table = db.table('sites')
if site_table.get(doc_id=1) is None:
    site_table.insert(default_site)
main_site = site_table.get(doc_id=1)


# Site Rest App
class SiteRestApp(GenericRestApp):

    def __init__(self, bottle_app, db_table, default_data):
        super().__init__(bottle_app, db_table, default_data)

        # Extra rest route methods
        self._bottle_app.get('/public/<doc_id:int>', callback=self._get_doc)

    def _post_new_doc(self):
        return json_response({'message': 'New Site Cannot be Added'}, status=400)

    def _delete_doc(self, doc_id):
        # Default site cannot be deleted
        if doc_id == 1:
            return json_response({'message': 'Default Site Cannot be Deleted'}, status=400)
        super()._delete_doc(doc_id)


# Create Site Rest App
site_rest_app = SiteRestApp(site_bottle_app, site_table, default_site)
