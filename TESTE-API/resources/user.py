from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from werkzeug.security import check_password_hash, generate_password_hash

from con_sql_alchemy import bd
from models.user import UtilizadorModel


class UserRegister(Resource):
    def post(self):
        dados = request.get_json(silent=True)

        if not isinstance(dados, dict) or not all(
            isinstance(dados.get(campo), str) and dados[campo].strip()
            for campo in ("username", "email", "password")
        ):
            return {"mensagem": "Preenche username, email e password."}, 400

        email = dados["email"].strip().lower()

        if UtilizadorModel.query.filter_by(email=email).first():
            return {"mensagem": "Este email já está registado."}, 400

        utilizador = UtilizadorModel(
            username=dados["username"].strip(),
            email=email,
            password=generate_password_hash(dados["password"]),
            tipo="utilizador",
        )

        bd.session.add(utilizador)
        bd.session.commit()

        return {"mensagem": "Utilizador registado com sucesso."}, 201


class UserLogin(Resource):
    def post(self):
        dados = request.get_json(silent=True)

        if not isinstance(dados, dict) or not all(
            isinstance(dados.get(campo), str) and dados[campo].strip()
            for campo in ("email", "password")
        ):
            return {"mensagem": "Preenche email e password."}, 400

        email = dados["email"].strip().lower()
        utilizador = UtilizadorModel.query.filter_by(email=email).first()

        if utilizador is None or not check_password_hash(
            utilizador.password, dados["password"]
        ):
            return {"mensagem": "Email ou palavra-passe incorretos."}, 401

        token = create_access_token(
            identity=str(utilizador.id),
            additional_claims={"tipo": utilizador.tipo},
        )

        return {"access_token": token}, 200