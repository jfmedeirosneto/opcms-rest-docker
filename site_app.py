# -*- coding: utf-8 -*-
from bottle import Bottle
from generic_rest_app import GenericRestApp, json_response
from settings import db

# Bottle app
site_bottle_app = Bottle()

# Default site data
default_site = {
    'name': 'Site Name',
    'title': 'Site Title',
    'info': 'Site Info',
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

    def _delete_doc(self, doc_id):
        # Default site cannot be deleted
        if doc_id == 1:
            return json_response({'message': 'Default Site Cannot be Deleted'}, status=400)
        super()._delete_doc(doc_id)


# Create Site Rest App
site_rest_app = SiteRestApp(site_bottle_app, site_table, default_site)
