from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Inicializa a aplicação Flask

app = Flask(__name__)

# Configura o banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'  # Caminho do seu banco de dados SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desativa o rastreamento de modificações

# Inicializa o SQLAlchemy
db = SQLAlchemy(app)

# Modelo para a tabela de Tarefas
class Tarefas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    deadline = db.Column(db.Date, nullable=False)  # Data de prazo para a tarefa
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Tarefas {self.title}>'

def criar_tarefa_no_banco(title, description, deadline):
    nova_tarefa = Tarefas(
        title=title,
        description=description,
        deadline=deadline,
        date_created=datetime.now()
    )
    db.session.add(nova_tarefa)
    db.session.commit()

def obter_tarefas_por_data(deadline):
    tarefas = Tarefas.query.filter_by(deadline=deadline).all()
    return tarefas


def excluir_tarefa(id):
    tarefa = Tarefas.query.get(id)
    if tarefa:
        db.session.delete(tarefa)
        db.session.commit()

# Função para criar as tabelas no banco de dados
def create_db():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    create_db()
