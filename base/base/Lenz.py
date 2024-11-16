from flask import Flask, render_template, request, redirect, url_for
from base import app, db
import pymysql
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT

app = Flask(__name__)


#######################################################################################################

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/ver_establecimiento/<int:responsable_id>')
def ver_establecimiento(responsable_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Consulta para el responsable
    cursor.execute("SELECT * FROM RESPONSABLE_DE_ESTABLECIMIENTO WHERE id = %s", (responsable_id,))
    responsable = cursor.fetchone()

    # Consulta para las actividades del responsable
    cursor.execute("SELECT * FROM ACTIVIDAD_TURISTICA WHERE responsable_id = %s", (responsable_id,))
    actividades = cursor.fetchall()

    cursor.close()
    connection.close()
    return render_template('ver_establecimiento.html', responsable=responsable, actividades=actividades)


###################################################################################################


@app.route('/registrar_actividad', methods=['POST'])
def registrar_actividad():
    responsable_id = request.form['responsable_id']
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    fecha = request.form['fecha']

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO ACTIVIDAD_TURISTICA (responsable_id, nombre, descripcion, fecha)
        VALUES (%s, %s, %s, %s)
    """, (responsable_id, nombre, descripcion, fecha))

    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('ver_establecimiento', responsable_id=responsable_id))


###########################################################################################################


@app.route('/modificar_actividad/<int:id>', methods=['GET', 'POST'])
def modificar_actividad(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        fecha = request.form['fecha']

        cursor.execute("""
            UPDATE ACTIVIDAD_TURISTICA 
            SET nombre = %s, descripcion = %s, fecha = %s
            WHERE id = %s
        """, (nombre, descripcion, fecha, id))

        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('ver_establecimiento', responsable_id=request.form['responsable_id']))

    # Obtener los datos actuales de la actividad
    cursor.execute("SELECT * FROM ACTIVIDAD_TURISTICA WHERE id = %s", (id,))
    actividad = cursor.fetchone()

    cursor.close()
    connection.close()
    return render_template('modificar_actividad.html', actividad=actividad)


#######################################################################################################


@app.route('/eliminar_actividad/<int:id>', methods=['POST'])
def eliminar_actividad(id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Eliminar la actividad
    cursor.execute("DELETE FROM ACTIVIDAD_TURISTICA WHERE id = %s", (id,))
    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for('ver_establecimiento', responsable_id=request.form['responsable_id']))


########################################################################################################


@app.route('/reporte/<int:responsable_id>')
def reporte(responsable_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Consulta para obtener el responsable y las actividades
    cursor.execute("SELECT * FROM RESPONSABLE_DE_ESTABLECIMIENTO WHERE id = %s", (responsable_id,))
    responsable = cursor.fetchone()

    cursor.execute("SELECT * FROM ACTIVIDAD_TURISTICA WHERE responsable_id = %s", (responsable_id,))
    actividades = cursor.fetchall()

    cursor.close()
    connection.close()
    return render_template('reporte.html', responsable=responsable, actividades=actividades)


#######################################################################################################


def get_db_connection():
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )
    return connection
