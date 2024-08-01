from models import db
from models.roles import Role
def create_roles():
    admin=Role(id=4, name='Admin')
    user=Role(id=5, name='User')

    db.session.add(admin)
    db.session.add(user)

    db.session.commit()

create_roles()

