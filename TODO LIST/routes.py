from flask import Flask, render_template, request, redirect, url_for
from models import db, Tarefas
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


# Rota para a página inicial com o calendário
@app.route('/')
def homepage():
    tarefas = Tarefas.query.all()  # Aqui você pode pegar todas as tarefas ou filtrar por data
    return render_template('homepage.html')

@app.route('/tarefas')
def tarefas():
    data_selecionada = request.args.get('date')  # Pega a data enviada pelo formulário
    tarefas = Tarefas.query.filter_by(deadline=data_selecionada).all()  # Filtra as tarefas por data
    return render_template('tarefas.html', tarefas=tarefas, data=data_selecionada)

@app.route('/tarefas', methods=['GET', 'POST'])
def criar_tarefa():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        deadline_str = request.args.get('date')  # Pegando a data selecionada na URL

        if not title or not deadline_str:
            return "Título e data são obrigatórios", 400

        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        except ValueError:
            return "Formato de data inválido", 400

        nova_tarefa = Tarefas(title=title, description=description, deadline=deadline)
        db.session.add(nova_tarefa)
        db.session.commit()

        return redirect(url_for('tarefas', date=deadline_str))

    # Se for GET, apenas carrega as tarefas normalmente
    data_selecionada = request.args.get('date')
    tarefas = Tarefas.query.filter_by(deadline=data_selecionada).all()
    return render_template('tarefas.html', tarefas=tarefas, data=data_selecionada)


@app.route('/complete/<int:id>', methods=['POST'])
def completar_tarefa(id):
    task = Tarefas.query.get(id)

    if not task:
        return "Tarefa não encontrada", 404

    task.completed = not task.completed  # Alterna entre True e False
    db.session.commit()

    return redirect(url_for('tarefas', date=task.deadline))


# Rota para deletar uma tarefa
@app.route('/delete/<int:id>')
def delete_task(id):
    task = Tarefas.query.get(id)
    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('homepage'))


if __name__ == '__main__':
    app.run(debug=True)
