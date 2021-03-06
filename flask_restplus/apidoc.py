# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import url_for, Blueprint, render_template, current_app


class Apidoc(Blueprint):
    '''
    Allow to know if the blueprint has already been registered
    until https://github.com/mitsuhiko/flask/pull/1301 is merged
    '''
    def __init__(self, *args, **kwargs):
        self.registered = False
        super(Apidoc, self).__init__(*args, **kwargs)

    def register(self, *args, **kwargs):
        super(Apidoc, self).register(*args, **kwargs)
        self.registered = True

apidoc = Apidoc('apidoc', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/swaggerui',
)


@apidoc.add_app_template_global
def swagger_static(filename):
    return url_for('apidoc.static', filename='bower/swagger-ui/dist/{0}'.format(filename))


def ui_for(api):
    '''Render a SwaggerUI for a given API'''
    if not apidoc.registered:
        current_app.register_blueprint(apidoc)
    return render_template('swagger-ui.html', specs_url=api.specs_url)
