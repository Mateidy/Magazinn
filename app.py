import os
import secrets

from flask import Flask , jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv

from db import db
from blocklist import BLOCKLIST
from models import StoreModel, ItemModel, TagModel, ItemTags, UserModel, RoleModel


from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint
from resources.roles import blp as RoleBlueprint


def create_roles():
    admin_role = RoleModel.query.filter_by(name="admin").first()
    customer_role = RoleModel.query.filter_by(name="customer").first()

    if not admin_role:
        admin_role = RoleModel(name="admin")
        db.session.add(admin_role)
    if not customer_role:
        customer_role = RoleModel(name="customer")
        db.session.add(customer_role)

    try:
        db.session.add(admin_role)
        db.session.add(customer_role)
        db.session.commit()
    except Exception as e:
        print(f"Error creating roles:{e}")
        return None , None

    return admin_role, customer_role


def assign_roles_to_users(admin_role, customer_role):
    users = UserModel.query.all()
    for user in users:
        if user.id == 4:
            user.roles.append(admin_role)
        else:
            user.roles.append(customer_role)

    db.session.commit()


def create_app(db_url=None):
    app=Flask (__name__)
    load_dotenv()

    app.config["PROPAGATE_EXCEPTIONS"]= True
    app.config["API_TITLE"]= "Stores REST API"
    app.config["API_VERSION"]="v1"
    app.config["OPENAPI_VERSION"]="3.0.3"
    app.config["OPENAPI_URL_PREFIX"]="/"
    app.config["OPENAPI_SWAGGER_UI_PATH"]="/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"]="https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"]=db_url or os.getenv("DATABASE_URL" ,"sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
    db.init_app(app)

    migrate= Migrate(app,db)

    api=Api(app)

    app.config["JWT_SECRET_KEY"]="295040099478539289169991040315992286316"
    jwt=JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header,jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header,jwt_payload):
        return (
            jsonify(
                {"description":"The token has been revoked." , "error":"token_revoked"}
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header,jwt_payload):
        return (
            jsonify(
                {
                    "description":"The token is not fresh.",
                    "error":"fresh_token_required",
                }
            ),
            401,
        )
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity== 4:
            return {"is_admin":True}
        return {"is_admin":False}


    @jwt.expired_token_loader
    def expired_token_loader(jwt_header,jwt_payload):
        return (
            jsonify({"message": "The token has expired." , "error": "token_expired"}),401,
        )
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message":"Signature verification failed." , "error":"invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {"description":"Request does not contain an acces token .",
                 "error": "authorization_required" ,}
            ),
            401,
        )

    def create_tables():
        try:db.create_all()

        except Exception as e:
            print(f"Eroare :{e}")

    with app.app_context():
        create_tables()
        admin_role, customer_role = create_roles()
        assign_roles_to_users(admin_role, customer_role)

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(RoleBlueprint)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)





