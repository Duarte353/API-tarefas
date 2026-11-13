from con_sql import bd
from werkzeug.security import generate_password_hash, check_password_hash


class UserModel(bd.Model):
    __tablename__ = "utilizadores"
    id = bd.Column(bd.Integer, primary_key=True)
    username = bd.Column(bd.String(80), nullable=False)
    email = bd.Column(bd.String(120), unique=True, nullable=False)
    password = bd.Column(bd.String(255), nullable=False)  # guarda o hash, nunca a password
    tipo = bd.Column(bd.String(20), nullable=False, default="utilizador")  # admin ou utilizador

    # Um utilizador pode ter várias tarefas
    tarefas = bd.relationship("TarefaModel", back_populates="utilizador",
                              cascade="all, delete-orphan")

    def __init__(self, username, email, password, tipo="utilizador"):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.tipo = tipo

    def json(self):
        # A password nunca é devolvida
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "tipo": self.tipo,
        }

    def verificar_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def find_user(cls, id_user):
        return cls.query.filter_by(id=id_user).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def save_user(self):
        bd.session.add(self)
        bd.session.commit()

    def delete_user(self):
        bd.session.delete(self)
        bd.session.commit()
