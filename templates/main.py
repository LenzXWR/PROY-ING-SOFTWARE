from flask import Flask, render_template, request, redirect, url_for
import pymysql
from datetime import datetime

app = Flask(__name__)
# Conexión a nuestra base  base de datos bd_establecimeintos
def conexion():
    return pymysql.connect(host="localhost", user="root", password="", db="BD_ESTABLECIMIENTO")

# ------------------ Módulo de Usuarios ------------------

# Registrar usuario
@app.route("/usuario/registrar", methods=["GET", "POST"])
def usuario_registrar():
    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        contraseña = request.form["contraseña"]
        tipo_usuario = request.form["tipo_usuario"]

        conn = conexion()
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO usuario(nombre, correo, contraseña, tipo_usuario) VALUES(%s, %s, %s, %s)",
                           (nombre, correo, contraseña, tipo_usuario))
        conn.commit()
        conn.close()
        return redirect("/usuario/mostrar")
    return render_template("registroUsuario.html")

# Mostrar usuarios
@app.route("/usuario/mostrar")
def usuario_mostrar():
    conn = conexion()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM usuario")
        usuarios = cursor.fetchall()
    conn.close()
    return render_template("mostrarUsuario.html", usuarios=usuarios)

# ------------------ Módulo de Establecimientos ------------------

# Registrar establecimiento
@app.route("/establecimiento/registrar", methods=["GET", "POST"])
def establecimiento_registrar():
    if request.method == "POST":
        nombre = request.form["nombre"]
        ubicacion = request.form["ubicacion"]
        descripcion = request.form["descripcion"]
        id_responsable = request.form["id_responsable"]

        conn = conexion()
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO establecimiento(nombre, ubicacion, descripcion, id_responsable) VALUES(%s, %s, %s, %s)",
                           (nombre, ubicacion, descripcion, id_responsable))
        conn.commit()
        conn.close()
        return redirect("/establecimiento/mostrar")
    return render_template("registroEstablecimiento.html")

# Mostrar establecimientos
@app.route("/establecimiento/mostrar")
def establecimiento_mostrar():
    conn = conexion()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM establecimiento")
        establecimientos = cursor.fetchall()
    conn.close()
    return render_template("mostrarEstablecimiento.html", establecimientos=establecimientos)

# ------------------ Módulo de Actividades de Turismo ------------------

# Registrar actividad de turismo
@app.route("/actividad/registrar", methods=["GET", "POST"])
def actividad_registrar():
    if request.method == "POST":
        nombre_actividad = request.form["nombre_actividad"]
        descripcion_actividad = request.form["descripcion_actividad"]
        fecha = request.form["fecha"]
        id_establecimiento = request.form["id_establecimiento"]

        conn = conexion()
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO actividad_turismo(nombre_actividad, descripcion_actividad, fecha, id_establecimiento) VALUES(%s, %s, %s, %s)",
                           (nombre_actividad, descripcion_actividad, fecha, id_establecimiento))
        conn.commit()
        conn.close()
        return redirect("/actividad/mostrar")
    return render_template("registroActividad.html")

# Mostrar actividades de turismo
@app.route("/actividad/mostrar")
def actividad_mostrar():
    conn = conexion()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM actividad_turismo")
        actividades = cursor.fetchall()
    conn.close()
    return render_template("mostrarActividad.html", actividades=actividades)

# ------------------ Módulo de Inscripción a Actividades ------------------

# Registrar inscripción a actividad
@app.route("/inscripcion/registrar/<int:id_actividad>", methods=["GET", "POST"])
def inscripcion_registrar(id_actividad):
    if request.method == "POST":
        id_turista = request.form["id_turista"]
        fecha_inscripcion = datetime.now().strftime("%Y-%m-%d")

        conn = conexion()
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO inscripcion_actividad(id_turista, id_actividad, fecha_inscripcion) VALUES(%s, %s, %s)",
                           (id_turista, id_actividad, fecha_inscripcion))
        conn.commit()
        conn.close()
        return redirect("/inscripcion/mostrar")
    return render_template("registroInscripcion.html", id_actividad=id_actividad)

# Mostrar inscripciones
@app.route("/inscripcion/mostrar")
def inscripcion_mostrar():
    conn = conexion()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM inscripcion_actividad")
        inscripciones = cursor.fetchall()
    conn.close()
    return render_template("mostrarInscripcion.html", inscripciones=inscripciones)

# Iniciar la aplicación
if __name__ == "__main__":
    app.run(debug=True)
