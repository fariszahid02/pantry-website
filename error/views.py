# Authored by: Yat Nam
# This function routes user to relevant error pages
from flask import render_template

from app import create_app
app=create_app()


@app.errorhandler(400)  # Bad Request
def bad_request(error):
    return render_template('error.html', error_code=400, error_name='Bad Request'), 400


@app.errorhandler(403)  # Forbidden
def forbidden(error):
    return render_template('error.html', error_code=403, error_name='Forbidden'), 403


@app.errorhandler(404)  # Not Found
def page_not_found(error):
    return render_template('error.html', error_code=404, error_name='Not Found'), 404


@app.errorhandler(500)  # Internal Server Error
def internal_server_error(error):
    return render_template('error.html', error_code=500, error_name='Internal Server Error'), 500


@app.errorhandler(503)  # Service Unavailable
def service_unavailable(error):
    return render_template('error.html', error_code=503, error_name='Service Unavailable'), 503
