from flask import Blueprint
from ..models import Permission

main = Blueprint('main',__name__)

from . import views, errors

@main.app_context_processor
def inject_permissions():
    """To avoid having to add a template
        argument in every render_template() call, a context processor can be used. Context
        processors make variables globally available to all templates"""
    return dict(Permissions=Permission)