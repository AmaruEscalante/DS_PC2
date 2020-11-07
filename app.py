from flask import Flask, render_template, request, redirect, flash, url_for, sessions
import sqlite3

app = Flask(__name__)
app.secret_key = 'super secret key'


conn = sqlite3.connect('libreria.db')
conn.execute('CREATE TABLE IF NOT EXISTS libro (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, disponible TEXT, isbn TEXT, categoria TEXT)')
conn.execute('CREATE TABLE IF NOT EXISTS autor (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, edicion TEXT, fecha TEXT, pais TEXT)')

secretkey = "secretkey"

@app.route('/')
def index():
    conn = sqlite3.connect('libreria.db')
    print('Opened db succesfully')
    cur = conn.cursor()
    cur.execute('select * from libro')
    libros = cur.fetchall()
    cur.execute('select * from autor')
    autor = cur.fetchall()
    return render_template('index.html', libros=libros, autor=autor)


@app.route('/add_book', methods=['POST', 'GET'])
def add_book():
    if request.method == 'POST':
        try:
            nomb = request.form['nombre']
            disp = request.form['disponible']
            isbn = request.form['isbn']
            cat = request.form['categoria']

            with sqlite3.connect("libreria.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO libro (nombre, disponible, isbn, categoria) VALUES (?,?,?,?)", (nomb, disp, isbn, cat))
                con.commit()
                msg = "Record succesfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            flash(msg)
            return redirect(url_for('index'))
            con.close()

    return redirect(url_for('index'))


@app.route('/add_autor', methods=['POST', 'GET'])
def add_autor():
    if request.method == 'POST':
        try:
            nomb = request.form['nombre']
            edicion = request.form['edicion']
            fecha = request.form['fecha']
            pais = request.form['pais']

            with sqlite3.connect("libreria.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO autor (nombre, edicion, fecha, pais) VALUES (?,?,?,?)", (nomb, edicion, fecha, pais))
                con.commit()
                msg = "Record succesfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            flash(msg)
            return redirect(url_for('index'))
            con.close()

    return redirect(url_for('index'))



@app.route('/edit/<id>')
def edit_book(id):
    conn = sqlite3.connect('libreria.db')
    print('Opened db succesfully')
    cur = conn.cursor()
    cur.execute("SELECT * FROM libro WHERE id = ?",(id,))
    data = cur.fetchall()
    print(data[0])
    return render_template('edit.html', libro=data[0])


@app.route('/edit_autor/<id>')
def edit_autor(id):
    conn = sqlite3.connect('libreria.db')
    print('Opened db succesfully')
    cur = conn.cursor()
    cur.execute("SELECT * FROM autor WHERE id = ?",(id,))
    data = cur.fetchall()
    print(data[0])
    return render_template('edit_autor.html', autor=data[0])


@app.route('/delete/<string:id>')
def delete_book(id):
    conn = sqlite3.connect('libreria.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM libro where id = ?", (id,))
    conn.commit()
    flash('Contact deleted succesfully')
    return redirect(url_for('index'))


@app.route('/delete_autor/<string:id>')
def delete_autor(id):
    conn = sqlite3.connect('libreria.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM autor where id = ?", (id,))
    conn.commit()
    flash('Contact deleted succesfully')
    return redirect(url_for('index'))


@app.route('/update/<id>', methods=['POST'])
def update_libro(id):
    if request.method == 'POST':
        nom = request.form['nombre']
        disp = request.form['disponible']
        isbn = request.form['isbn']
        cat = request.form['categoria']
        print('UPDATE', id, nom, disp, isbn, cat)
        conn = sqlite3.connect('libreria.db')
        print('Opened db succesfully')
        cur = conn.cursor()
        cur.execute("update libro set nombre = ?,disponible = ?,isbn = ?, categoria = ? where id = ?",(nom,disp,isbn,cat, id))
        conn.commit()
        flash('Book modified succesfully')
        return redirect(url_for('index'))


@app.route('/update_autor/<id>', methods=['POST'])
def update_autor(id):
    if request.method == 'POST':
        nomb = request.form['nombre']
        edicion = request.form['edicion']
        fecha = request.form['fecha']
        pais = request.form['pais']
        conn = sqlite3.connect('libreria.db')
        print('Opened db succesfully')
        cur = conn.cursor()
        cur.execute("update autor set nombre = ?,edicion = ?,fecha = ?, pais = ? where id = ?",(nomb,edicion,fecha,pais, id))
        conn.commit()
        flash('Autor modified succesfully')
        return redirect(url_for('index'))


@app.route('/search', methods=['GET','POST'])
def search_results():
    conn = sqlite3.connect('libreria.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        cursor.execute('select * from libro where nombre LIKE ?',[request.form['nombre']])
        results = cursor.fetchall()

    if len(results) == 0:
        return render_template('result.html', results=results)
    else:
        return render_template('result.html', results=results[0])

if __name__ == '__main__':
    app.run()
