from flask import render_template


def page_not_found(error):
    return render_template('errors/error_404.html'), 404


def internal_error(error):
    return render_template('errors/error_500.html'), 500
