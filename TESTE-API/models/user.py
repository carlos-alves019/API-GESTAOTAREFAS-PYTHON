from con_sql_alchemy import bd


class UtilizadorModel(bd.Model):
    __tablename__ = "utilizadores"

    id = bd.Column(bd.Integer, primary_key=True)
    username = bd.Column(bd.String(80), nullable=False)
    email = bd.Column(bd.String(120), unique=True, nullable=False)
    password = bd.Column(bd.String(255), nullable=False)
    tipo = bd.Column(bd.String(20), nullable=False, default="utilizador")