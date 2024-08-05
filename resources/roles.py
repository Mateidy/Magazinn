from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError


from db import db
from models import RoleModel , UserModel
from schemas import RoleSchema

blp=Blueprint("Role",__name__, description="Operations on roles")


@blp.route("/role/<int:role_id>")
class Role(MethodView):
    @jwt_required()
    @blp.response(200,RoleSchema)

    def get(self,role_id):
        role=RoleModel.query.get_or_404(role_id)
        return role

    @jwt_required()
    def delete(self,role_id):
        jwt=get_jwt()
        if not jwt.get("is_admin"):
            abort(401, "Admin privilege required.")
        try:
            role=RoleModel.query.get_or_404(role_id)
            db.session.delete(role)
            db.session.commit()
            return {"message":"Role deleted."}
        except Exception as e:
            print(f"Error occured:{e}")
            abort(500, message="An error occured while deleting the role")

@blp.route("/role")
class RoleList(MethodView):
    @jwt_required()
    @blp.response(200,RoleSchema(many=True))

    def get(self):
        roles=RoleModel.query.all()
        return roles

    @jwt_required()
    @blp.response(200,RoleSchema)
    def put(self,role_data,role_id):
        jwt=get_jwt()
        if not jwt.get("is_admin"):
            abort (401,"Admin privilege requried.")

        try:
            role=RoleModel.query.get_or_404(role_id)
            role.name=role_data['name']
            db.session.commit()
            return role
        except Exception as e:
            print(f"Error occured:{e}")
            abort(500, message="An error occured while updating the role")









