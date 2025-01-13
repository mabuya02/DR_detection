from flask import Blueprint

blueprint = Blueprint(
    'image_blueprint',
    __name__,
    url_prefix='/images'
)

