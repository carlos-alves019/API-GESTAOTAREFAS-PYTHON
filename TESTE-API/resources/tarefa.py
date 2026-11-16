from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse

from con_sql_alchemy import bd
from models.tarefa import TarefaModel


class Tarefas(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument(
        "titulo", type=str, required=True, nullable=False, location="json"
    )
    argumentos.add_argument("descricao", type=str, location="json")
    argumentos.add_argument(
        "estado",
        type=str,
        choices=("Pendente", "Em curso", "Concluída"),
        default="Pendente",
        nullable=False,
        location="json",
    )

    @jwt_required()
    def post(self):
        dados = self.argumentos.parse_args()
        titulo = dados["titulo"].strip()

        if not titulo:
            return {"mensagem": "O título é obrigatório."}, 400

        tarefa = TarefaModel(
            titulo=titulo,
            descricao=dados["descricao"],
            estado=dados["estado"],
            utilizador_id=int(get_jwt_identity()),
        )

        bd.session.add(tarefa)
        bd.session.commit()

        return {
            "id": tarefa.id,
            "titulo": tarefa.titulo,
            "descricao": tarefa.descricao,
            "estado": tarefa.estado,
            "utilizador_id": tarefa.utilizador_id,
        }, 201

    @jwt_required()
    def get(self):
        utilizador_id = int(get_jwt_identity())

        if get_jwt().get("tipo") == "admin":
            tarefas = TarefaModel.query.all()
        else:
            tarefas = TarefaModel.query.filter_by(
                utilizador_id=utilizador_id
            ).all()

        return [
            {
                "id": tarefa.id,
                "titulo": tarefa.titulo,
                "descricao": tarefa.descricao,
                "estado": tarefa.estado,
                "utilizador_id": tarefa.utilizador_id,
            }
            for tarefa in tarefas
        ], 200


class Tarefa(Resource):
    @jwt_required()
    def get(self, id):
        tarefa = bd.session.get(TarefaModel, id)

        if tarefa is None:
            return {"mensagem": "Tarefa não encontrada."}, 404

        utilizador_id = int(get_jwt_identity())
        tipo = get_jwt().get("tipo")

        if tipo != "admin" and tarefa.utilizador_id != utilizador_id:
            return {"mensagem": "Não tens permissão para consultar esta tarefa."}, 403

        return {
            "id": tarefa.id,
            "titulo": tarefa.titulo,
            "descricao": tarefa.descricao,
            "estado": tarefa.estado,
            "utilizador_id": tarefa.utilizador_id,
        }, 200