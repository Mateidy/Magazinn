from db import db

class UserModel(db.Model):
    __tablename__="users"

    id=db.Column(db.Integer, primary_key=True,autoincrement=True)
    username=db.Column(db.String(80),unique=True,nullable=False)
    password=db.Column(db.String(256), unique=True,nullable=False)

    roles=db.relationship( "Role",secondary="user_roles",back_populates="users")

    def has_role(self , role):
        return any(r.slug== role for r in self.roles)

class Role(db.Model):
    __tablename__ = "roles"

    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(36),nullable=False)
    slug=db.Column(db.String(36),nullable=False,unique=True)

    users=db.relationship("UserModel",secondary="user_roles",back_populates="roles")

class UserRole(db.Model):
    __tablename__="user_roles"

    user_id=db.Column(db.Integer,db.ForeignKey("users.id"),primary_key=True)
    role_id=db.Column(db.Integer,db.ForeignKey("roles.id"),primary_key=True)

