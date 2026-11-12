from datetime import datetime

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Tarefa(db.Model):
    __tablename__ = "tarefas"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    deadline = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)


def parse_date(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI="sqlite:///todo.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    @app.route("/")
    def homepage():
        return render_template("homepage.html")

    @app.route("/tarefas", methods=["GET", "POST"])
    def tarefas():
        selected_date = parse_date(request.args.get("date"))

        if selected_date is None:
            if request.method == "POST":
                return "Data obrigatória ou em formato inválido", 400
            return redirect(url_for("homepage"))

        if request.method == "POST":
            title = request.form.get("title", "").strip()
            description = request.form.get("description", "").strip()

            if not title:
                return "Título é obrigatório", 400
            if len(title) > 100 or len(description) > 200:
                return "Título ou descrição excede o limite permitido", 400

            db.session.add(
                Tarefa(
                    title=title,
                    description=description,
                    deadline=selected_date,
                )
            )
            db.session.commit()
            return redirect(url_for("tarefas", date=selected_date.isoformat()))

        tasks = Tarefa.query.filter_by(deadline=selected_date).all()
        return render_template(
            "tarefas.html",
            tarefas=tasks,
            data=selected_date.isoformat(),
        )

    @app.post("/complete/<int:task_id>")
    def completar_tarefa(task_id):
        task = db.get_or_404(Tarefa, task_id)
        task.completed = not task.completed
        db.session.commit()
        return redirect(url_for("tarefas", date=task.deadline.isoformat()))

    @app.post("/delete/<int:task_id>")
    def delete_task(task_id):
        task = db.get_or_404(Tarefa, task_id)
        deadline = task.deadline.isoformat()
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for("tarefas", date=deadline))

    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run()
