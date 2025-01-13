from flask import Blueprint

blueprint = Blueprint(
    'test_blueprint',
    __name__,
    url_prefix='/tests' 
)
