from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView
from flask_admin.form import SecureForm
# First-party
from . import models as m


def init_app(app, **kwargs):
    """Initialises the admin dashboard for the app."""
    admin = Admin(app, name='flaskapp', template_mode='bootstrap3', **kwargs)
    admin.add_view(UserView(m.User))
    admin.add_view(ObjectView(m.Object))
    admin.add_view(PredicateView(m.Predicate))
    admin.add_view(TupleView(m.Tuple))
    return app


class SecureModelView(ModelView):
    """Base class which uses CSRF protection when generating forms."""
    form_base_class = SecureForm


class UserView(SecureModelView):
    # Don't display password in the list of users
    column_exclude_list = ('password',)


class ObjectView(SecureModelView):
    column_sortable_list = [('created_by', m.User.name), 'created_on',
                            ('deleted_by', m.User.name), 'deleted_on']
    column_searchable_list = [m.User.name]


class PredicateView(SecureModelView):
    column_sortable_list = [('created_by', m.User.name), 'created_on']
    column_searchable_list = ['name', m.User.name]


class TupleView(SecureModelView):
    column_sortable_list = ['subject_id', ('predicate', m.Predicate.name), 'object_id',
                            ('created_by', m.User.name), 'created_on']
    column_searchable_list = ['subject_id', m.Predicate.name, 'object_id', m.User.name]
