from flask import render_template

from . import errors_bp
from .. import db


# Like Flask.errorhandler() but for a blueprint. app_errorhandler(code) is
# used for all requests, even if outside of the blueprint.
#
# The errorhandler decorator is for errors that originate in the routes defined by the
# blueprint while the app_errorhandler decorator is for application-wide errors
@errors_bp.app_errorhandler(403)
def forbidden(error):
    return render_template('errors/403.html', title="Forbidden"), 403

@errors_bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html', title="Page Not Found"), 404

#@errors_bp.app_errorhandler(500)
#def internal_server_error(error):
#    db.session.rollback()
#    return render_template('errors/500.html', title="Server Error"), 500