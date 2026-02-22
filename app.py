from flask import Flask, render_template, request, redirect, url_for  # Flask tools
import sqlite3  # DB built-in Python

app = Flask(__name__)  # App principal (busca templates/static aquí)

# Helper: conexión DB segura
def get_db():
    conn = sqlite3.connect('tasks.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Rows como dict: task['title']
    return conn

# Inicializa tabla (tu SQL!)
def init_db():
    db = get_db()
    db.execute('''CREATE TABLE IF NOT EXISTS tasks
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Auto ID
                   title TEXT NOT NULL,
                   description TEXT,
                   done BOOLEAN DEFAULT 0)''')
    db.commit()  # Guarda cambios
    db.close()
    print("✅ DB lista: tasks.db creada")

# Ruta home: lista tasks
@app.route('/')
def index():
    db = get_db()
    tasks = db.execute('SELECT * FROM tasks ORDER BY id DESC').fetchall()
    db.close()
    return render_template('index.html', tasks=tasks)  # Pasar data HTML

# Ruta agregar
@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['description']
        db = get_db()
        db.execute('INSERT INTO tasks (title, description) VALUES (?, ?)',
                   (title, desc))  # ? anti-SQL injection
        db.commit()
        db.close()
        return redirect(url_for('index'))
    return render_template('add_task.html')

@app.route('/toggle/<int:task_id>')
def toggle(task_id):
    db = get_db()
    db.execute('UPDATE tasks SET done = NOT done WHERE id = ?', (task_id,))
    db.commit()
    db.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    db = get_db()
    db.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    db.commit()
    db.close()
    return redirect(url_for('index'))


if __name__ == '__main__':  # Solo si ejecutas directo
    init_db()
    app.run(debug=True)  # debug=reload auto, puerto 5000


