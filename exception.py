from flask import Blueprint

exception = Blueprint('exception', __name__)

@exception.errorhandler(Exception)
def all_exception_handler(error):
   return 'Internal server error', 500

@exception.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404