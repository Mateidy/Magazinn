from db import db

roles_users=db.Table("roles_users",
                     db.Column("user_id",db.Integer(),db.ForeignKey("users.id")),
                     db.Column("role_id",db.Integer(),db.ForeignKey("roles.id")))
class RoleModel(db.Model):
    __tablename__="roles"

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80),nullable=False,unique=True)

    users=db.relationship("UserModel",secondary="roles_users" ,backref="roles")


