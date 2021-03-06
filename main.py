# -*- coding: utf-8 -*-
from bottle import Bottle, static_file, ServerAdapter
import os
import ssl
from settings import base_dir
from site_app import main_site, site_bottle_app
from user_app import user_bottle_app
from portfolio_app import portfolio_bottle_app


# Bottle app
main_bottle_app = Bottle()


# Route assets according main_site configuration template_assets
@main_bottle_app.route('/<asset:re:(%s)>/<filepath:path>' % '|'.join(main_site['template_assets']))
def route_static_asset(asset, filepath):
    template_dir = os.path.join(base_dir, main_site['template_dir'])
    asset_dir = os.path.join(template_dir, asset)
    return static_file(filepath, root=asset_dir)


# Get main according main_site configuration template_file
@main_bottle_app.get(['/', '/index.html', '/index.htm'])
def get_home():
    template_file = main_site['template_file']
    template_dir = os.path.join(base_dir, main_site['template_dir'])
    return static_file(template_file, root=template_dir)


# Route admin assets
@main_bottle_app.route('/admin/<filepath:path>')
def route_static_asset_admin(filepath):
    admin_dir = os.path.join(base_dir, 'admin-dist')
    return static_file(filepath, root=admin_dir)


# Route main admin page
@main_bottle_app.get(['/admin', '/admin/index.html', '/admin/index.htm'])
def get_admin_home():
    admin_dir = os.path.join(base_dir, 'admin-dist')
    return static_file('index.html', root=admin_dir)


# Mount apps
main_bottle_app.mount('/sites', site_bottle_app)
main_bottle_app.mount('/users', user_bottle_app)
main_bottle_app.mount('/portfolios', portfolio_bottle_app)

# Main entry
if __name__ == "__main__":
    main_bottle_app.run(host='0.0.0.0', port=8080)

# App
app = main_bottle_app
