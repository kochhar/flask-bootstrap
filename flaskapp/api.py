from flask_potion import Api, ModelResource
from flask_potion.contrib.peewee import PeeweeManager
# First-party
from . import models as m


def init_app(app, models=None):
    api = Api(app, default_manager=PeeweeManager)
    api.add_resource(ObjectResource)
    api.add_resource(TupleResource)
    return app


class ObjectResource(ModelResource):
    class Meta:
        model = m.Object


class TupleResource(ModelResource):
    class Meta:
        model = m.Tuple
