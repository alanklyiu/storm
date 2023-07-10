from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

# Try naming classes w/ regular nouns (plurals are formed by adding 's'/'es')
#
# If a __tablename__ isn't specified but a primary key is, Flask-SQLAlchemy 2.x
# auto-generates a name for the table. It's derived from the class name
# converted to lowercase & with "CamelCase" converted to "camel_case".
#
# A __init__ method isn't defined on all classes because SQLAlchemy adds an
# implicit constructor to all model classes which accept keyword arguments
# for all the columns & relationships.

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, index=True)
    staff_number = db.Column(db.String(10))
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    is_enabled = db.Column(db.Boolean, default=True)

    #username = db.Column(db.String(80), index=True, unique=True)
    #surname = db.Column(db.String(30))
    #given_name = db.Column(db.String(60))
    #nickname = db.Column(db.String(60))

    #def __init__(self, **kwargs):
    #    super(User, self).__init__(**kwargs)
    #    if self.role is None:
            #self.role = Role.query.filter_by(name='Administrator').first()
    #        self.role = Role.query.filter_by(default=True).first()

    # @property lets a method be accessed as an attribute
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'User: {self.email}'


# Set up user_loader
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(8), unique=True)
    name = db.Column(db.String(30))
    is_enabled = db.Column(db.Boolean, default=False)

    # One-to-many relationship
    # backref defines the field name that will be added to the objects of the
    # "many" class (User) that points back at the "one" object (Account),
    # meaning a property/field 'account' is declared on the model class 'User'
    users = db.relationship('User', backref='account', lazy='dynamic')

    def __repr__(self):
        return f'Account: {self.name}'


class Region(db.Model):
    __tablename__ = 'regions'

    id = db.Column(db.Integer, primary_key=True)
    # ISO 3166-1 alpha-2
    code = db.Column(db.String(2), unique=True)
    # ISO 3166 Short name
    name = db.Column(db.String(30))

    def __repr__(self):
        return f'Region: {self.code}'


class Site(db.Model):
    __tablename__ = 'sites'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(30))
    address = db.Column(db.String(60))
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'))
    account_id = db.Column(
        db.Integer,
        db.ForeignKey('accounts.id'),
        nullable=False
        )
    # A tuple that contains only the item, the constraint instance
    __table_args__ = (
        db.UniqueConstraint('account_id', 'code', name='_unique_account_site'),
        )

    rooms = db.relationship('Room', backref='site', lazy='dynamic')

    def __repr__(self):
        return f'Site: {self.name}'


class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(60))
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'))
    account_id = db.Column(
        db.Integer,
        db.ForeignKey('accounts.id'),
        nullable=False
        )
    cost = db.Column(db.Integer)
    __table_args__ = (
        db.UniqueConstraint('account_id', 'name', name='_unique_account_room'),
        )

    meetings = db.relationship('Meeting', backref='room', lazy='dynamic')

    def __repr__(self):
        return f'Room: {self.name}'


class Meeting(db.Model):
    __tablename__ = 'meetings'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    host_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    booker_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.DateTime, nullable=False)
    start_time = db.Column(db.Integer, nullable=False)
    end_time = db.Column(db.Integer, nullable=False) # calculated
    duration = db.Column(db.Integer, nullable=False)
    is_private = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'Meeting {self.id} for {self.id} last for {self.duration}'


class Permission:
    READ = 1
    ADMIN = 512


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

    users = db.relationship('User', backref='role', lazy='dynamic')

    # Default values are only set after an INSERT/UPDATE is issued, i.e. after
    # a session is flushed to the database. Before that, by default, SQLAlchemy
    # sets like 'permissions' to None if an initial value isn't provided in the
    # constructor arguments. A class constructor is added that overrides the
    # implicit one and sets the field to 0.
    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.READ],
            'Administrator': [Permission.READ, Permission.ADMIN],
            }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return f'Role: {self.name}'