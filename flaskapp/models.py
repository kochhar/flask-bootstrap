import datetime
from flask import g
from flask_security import UserMixin, RoleMixin
import peewee as pwee
from playhouse.flask_utils import FlaskDB

# wrapper object. the actual database is in db.database.
db = FlaskDB()


def initdb():
    """Initialise the tables."""
    db.database.create_tables([User, Role, UserRoles,
                               Predicate, Object, Tuple], safe=True)
    return db


class User(db.Model, UserMixin):
    """User model. Users cannot be deleted.

    Needed for
      - authentication."""
    name = pwee.CharField(null=False, index=True)
    email = pwee.CharField(null=False, index=True)
    password = pwee.CharField(null=False, index=True)
    status = pwee.IntegerField(null=False, default=1, index=True)
    created_by = pwee.CharField(null=False, default='root', index=True)
    created_on = pwee.DateTimeField(null=False, default=datetime.datetime.now, index=True)

    @property
    def is_active(self):
        return self.status == 1

    @property
    def is_deleted(self):
        return self.status == 0


class Role(db.Model, RoleMixin):
    """Role class for defining roles in the db."""
    name = pwee.CharField(null=False, unique=True)
    description = pwee.TextField(null=True)


class UserRoles(db.Model):
    """Relationship entity associating a user with roles. Peewee doesn't support many2many
    relations, so an intermediate is required."""
    user = pwee.ForeignKeyField(User, related_name='roles')
    role = pwee.ForeignKeyField(Role, related_name='users')
    name = property(lambda self: self.role.name)
    description = property(lambda  self: self.role.description)


class Predicate(db.Model):
    """Simplest possible assertion type."""
    name = pwee.CharField(primary_key=True)
    created_by = pwee.ForeignKeyField(User)
    created_on = pwee.DateTimeField(null=False, default=datetime.datetime.now, index=True)


class Object(db.Model):
    """Simplest possible thing."""
    created_by = pwee.ForeignKeyField(User, related_name='objects')
    created_on = pwee.DateTimeField(null=False, default=datetime.datetime.now, index=True)
    deleted_by = pwee.ForeignKeyField(User, related_name='objects_deleted', null=True, default=None)
    deleted_on = pwee.DateTimeField(null=True, default=None, index=True)


class Tuple(db.Model):
    """Simplest possible record."""
    subject_id = pwee.CharField(null=False, index=True)
    predicate = pwee.ForeignKeyField(Predicate)
    object_id = pwee.CharField(null=False, index=True)
    created_by = pwee.ForeignKeyField(User, related_name='tuples')
    created_on = pwee.DateTimeField(null=False, default=datetime.datetime.now, index=True)
    deleted_by = pwee.ForeignKeyField(User, related_name='tuples_deleted', null=True, default=None)
    deleted_on = pwee.DateTimeField(null=False, default=datetime.datetime.now, index=True)

