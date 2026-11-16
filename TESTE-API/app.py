from os import getenv
from secrets import token_hex

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from con_sql_alchemy import bd
from models.user import UtilizadorModel
from models.tarefa import TarefaModel
from resources.user import UserLogin, UserRegister
from resources.tarefa import Tarefas, Tarefa


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tarefas.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = getenv("JWT_SECRET_KEY") or token_hex(32)

bd.init_app(app)
api = Api(app, errors={
    "NoAuthorizationError": {
        "message": "É necessário iniciar sessão.",
        "status": 401,
    },
    "InvalidSignatureError": {
        "message": "Token inválido. Inicia sessão novamente.",
        "status": 401,
    },
    "ExpiredSignatureError": {
        "message": "Token expirado. Inicia sessão novamente.",
        "status": 401,
    },
})
jwt = JWTManager(app)

api.add_resource(UserRegister, "/registo")
api.add_resource(UserLogin, "/login")
api.add_resource(Tarefas, "/tarefas")
api.add_resource(Tarefa, "/tarefas/<int:id>")


if __name__ == "__main__":
    with app.app_context():
        bd.create_all()

    app.run()