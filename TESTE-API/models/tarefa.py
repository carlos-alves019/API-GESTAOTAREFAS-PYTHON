from con_sql_alchemy import bd


class TarefaModel(bd.Model):
    __tablename__ = "tarefas"

    id = bd.Column(bd.Integer, primary_key=True)
    titulo = bd.Column(bd.String(120), nullable=False)
    descricao = bd.Column(bd.Text)
    estado = bd.Column(bd.String(20), nullable=False, default="Pendente")
    utilizador_id = bd.Column(
        bd.Integer, bd.ForeignKey("utilizadores.id"), nullable=False
    )

    utilizador = bd.relationship("UtilizadorModel", backref="tarefas")