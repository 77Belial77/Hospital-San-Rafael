from flask import Flask, render_template, flash, request, session, redirect, url_for
import os, utils
from db import get_db
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask (__name__)
app.secret_key = os.urandom(24)

@app.route('/')#1
def index():
    return render_template('login.html')
    
@app.route('/dashboard')#1
def dashboard():
    return render_template('dashboard.html')

@app.route('/dashboard', methods=['POST', 'GET'])#2
def login_btn():
    try:
        if request.method == 'POST':
            db = get_db()
            error = None
            username = request.form['username']
            password = request.form['password']

            if not username:
                error = 'Debes ingresar el usuario'
                flash( error )
                return render_template( 'login.html' )

            if not password:
                error = 'Contraseña requerida'
                flash( error )
                return render_template( 'login.html' )
            cur = db.execute(
                'SELECT * FROM usuarios WHERE nom_user = ?', (username,)
            ).fetchone()

            if cur is None:
                error = 'Usuario o contraseña inválidos'
                flash( error )
                return render_template( 'login.html' )
            else:
                if check_password_hash(cur[1], password):
                    session.clear()
                    session['nom_user'] = cur[0]
                    return render_template( 'dashboard.html' )
                else:
                    error = 'Usuario o contraseña inválidos'
                    flash( error )
        else:
            return render_template( 'login.html' )
    except:
        error = 'Usuario o contraseña inválidos'
        flash( error )
        return render_template( 'login.html' )   

@app.route('/registro')#3
def registro():
    return render_template("registro.html")

@app.route('/login', methods=['POST', 'GET'])#4
def registro_btn():
    try:
        if request.method == 'POST':
            nombres= request.form['nombres']
            apellidos = request.form['apellidos']
            tipo_doc = request.form.get('tipo_doc')
            num_doc = request.form['num_doc']
            fechanacimiento = request.form['fechanacimiento']
            sexo = request.form.get('sexo')
            email = request.form['email']
            departamento = request.form.get('departamento')
            ciudad_municipio = request.form.get('ciudad_municipio')
            direccion = request.form['direccion']
            celular = request.form['celular']
            telefono = request.form['telefono']   
            error = None

            if not nombres:
                error = 'Debes ingresar el nombre'
                flash( error )
                return render_template( 'registro.html' )

            if not apellidos:
                error = 'Debes ingresar el apellido'
                flash( error )
                return render_template( 'registro.html' )

            if not num_doc:
                error = 'Debes ingresar el numero de documento'
                flash( error )
                return render_template( 'registro.html' )

            if not fechanacimiento:
                error = 'Debes ingresar su fecha de nacimiento'
                flash( error )
                return render_template( 'registro.html' )
            
            if not sexo:
                error = 'Debes ingresar el sexo'
                flash( error )
                return render_template( 'registro.html' )

            if not utils.isEmailValid( email ):
                error = 'Correo invalido'
                flash( error )
                return render_template( 'registro.html' )

            if departamento == "Departamentoo":
                error = 'Debes ingresar un departamento valido'
                flash( error )
                return render_template( 'registro.html' )

            if ciudad_municipio == "ciudad-municipioo":
                error = 'Debes ingresar una ciudad o municipio valido'
                flash( error )
                return render_template( 'registro.html' )

            if not direccion:
                error = 'Debes ingresar una dirección'
                flash( error )
                return render_template( 'registro.html' )

            if not celular:
                error = 'Debes ingresar un número de celular'
                flash( error )
                return render_template( 'registro.html' )
            
            password_hashed = generate_password_hash(num_doc)
            db = get_db()
            cur = db.cursor()
            cur.executescript('''INSERT INTO registros 
            (nombre, apellido, tipo_documento, numero_documento, fecha_nacimiento, sexo, correo, departamento, ciudad_municipio, direccion, celular, tel_fijo) 
            VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')''' % (nombres, apellidos, tipo_doc, num_doc, fechanacimiento, sexo, email, departamento, ciudad_municipio, direccion, celular, telefono,))
            cur.executescript("INSERT INTO usuarios (nom_user, pass) VALUES ('%s', '%s')" % (num_doc, password_hashed))
            db.commit()
            flash('Usuario creado en la BD')
                           
            return render_template( 'login.html' )
        else:
            return render_template( 'index.html' )
    except:
        return render_template( 'index.html' )

@app.route('/perfil/<int:sesion>', methods=["GET","POST"])#5
def perfil(sesion):
    try:
        if request.method == 'GET':
            db = get_db()
            cur = db.cursor()
            cur.execute('SELECT * FROM registros WHERE numero_documento = {}'.format(sesion))
            db.commit()
            data = cur.fetchone()
        
            return render_template("perfil.html", contact = data)
    except:
        return render_template("index.html")

@app.route('/mostrar_citas/<int:sesion>', methods=["GET","POST"])#6
def mostrar_citas(sesion):
    try:
        if request.method == 'GET':
            db = get_db()
            cur = db.cursor()
            cur.execute('SELECT * FROM citas WHERE cedula = {}'.format(sesion))
            db.commit()
            data = cur.fetchall()
         
            return render_template("Mostrar_citas.html", contact = data)
    except:
        return render_template("dashboard.html")


@app.route('/detalles_de_cita/<int:id>', methods=["GET","POST"])#7
def detalles_de_cita(id):
    try:
        if request.method == 'GET':
            db = get_db()
            cur = db.cursor()
            cur.execute("SELECT * FROM citas WHERE id={}".format(id))
            db.commit()
            data = cur.fetchall()
            return render_template("detalles_de_cita.html", contact = data)
    except:
        return render_template("perfil.html")

@app.route("/Delete/<int:id>", methods=["GET","POST"])
def cancelar_cita(id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM citas WHERE id={}".format(id))
    db.commit()    
    print("hola mundo")
    return redirect(location='/mostrar_citas/{}'.format(session["nom_user"]))
    
@app.route('/cerrar_sesion')
def cerrar_sesion():
    session.clear()
    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug = True)