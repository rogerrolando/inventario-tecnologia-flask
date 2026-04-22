import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('inventario.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db()
    productos = conn.execute('SELECT * FROM productos').fetchall()
    conn.close()
    return render_template('index.html', productos=productos)

@app.route('/create', methods=['GET'])
def create_form():
    return render_template('create.html')

@app.route('/create', methods=['POST'])
def create_product():
    nombre = request.form['nombre']
    categoria = request.form['categoria']
    precio = float(request.form['precio'])
    stock = int(request.form['stock'])
    conn = get_db()
    conn.execute('INSERT INTO productos (nombre, categoria, precio, stock) VALUES (?, ?, ?, ?)',
                 (nombre, categoria, precio, stock))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET'])
def edit_form(id):
    conn = get_db()
    producto = conn.execute('SELECT * FROM productos WHERE id = ?', (id,)).fetchone()
    conn.close()
    if producto is None:
        return "Producto no encontrado", 404
    return render_template('edit.html', producto=producto)

@app.route('/edit/<int:id>', methods=['POST'])
def edit_product(id):
    nombre = request.form['nombre']
    categoria = request.form['categoria']
    precio = float(request.form['precio'])
    stock = int(request.form['stock'])
    conn = get_db()
    conn.execute('UPDATE productos SET nombre = ?, categoria = ?, precio = ?, stock = ? WHERE id = ?',
                 (nombre, categoria, precio, stock, id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_product(id):
    conn = get_db()
    conn.execute('DELETE FROM productos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)