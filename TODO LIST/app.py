from flask import Flask, render_template, request, redirect, url_for
import os
from your_database_module import criar_tarefa_no_banco, obter_tarefas_por_data


app = Flask(__name__)

@app.route('/tarefas/<data>', methods=['GET', 'POST'])
def tarefas(data):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        # Função para salvar a tarefa no banco de dados
        criar_tarefa_no_banco(title, description, data)
        return redirect(url_for('tarefas', data=data))

    tarefas = obter_tarefas_por_data(data)  # Função para buscar tarefas por data
    return render_template('tarefas.html', tarefas=tarefas, data=data)

if __name__ == '__main__':


    app.run(debug=True)