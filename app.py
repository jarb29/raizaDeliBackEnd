import os
from flask import Flask, render_template, jsonify, request, redirect, send_from_directory
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_cors import CORS
from models import db, Modelo, Nestic, Piezas, ModeloProduccion
from flask_mail import Mail, Message
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static')
ALLOWED_EXTENSIONS_IMG = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'jarb29@gmail.com'
app.config['MAIL_PASSWORD'] = 'Amesti2020'


JWTManager(app)
CORS(app)
bcrypt = Bcrypt(app)
db.init_app(app)
Migrate(app, db)
manager = Manager(app)
mail = Mail(app)
manager.add_command("db", MigrateCommand)



@app.route('/')
def root():
    return render_template('index.html')


@app.route("/api/cargarprograma", methods=['POST'])
def crearProgramas():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    if request.method == 'POST':

        numero_ot = request.json.get('numero_ot', None)
        nombre_programa = request.json.get('nombre_programa', None)
        cantiadUnidadesFabricarEnLaOt = request.json.get('cantiadUnidadesFabricarEnLaOt', None)
        if not numero_ot:
            return jsonify({"msg": "Falta introducir el numero OT"}), 400
        if not nombre_programa:
            return jsonify({"msg": "Falta introducir el nombre del programa"}), 400
        if not cantiadUnidadesFabricarEnLaOt:
            return jsonify({"msg": "Falta introducir la cantidad"}), 400
        
        usua = Modelo()
        usua.numero_ot = numero_ot
        usua.nombre_programa = nombre_programa
        usua.cantiadUnidadesFabricarEnLaOt = cantiadUnidadesFabricarEnLaOt
        db.session.add(usua)
        db.session.commit()

    data = {
        "Modelo": usua.serialize() 
    }
    return jsonify({'msg': 'Modelo agregado exitosamente'}),  200



@app.route('/api/modelodisponibles', methods=['GET'])
def modelosDisponibles():
    listaModelos = Modelo.query.all()
    listaModelos = list(map(lambda listaModelos: listaModelos.serialize(), listaModelos))
    return jsonify(listaModelos), 200


@app.route("/api/crearnesctic", methods=['POST'])
def crearNestic():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    if request.method == 'POST':
        
        modelo_elegido = request.json.get('modelo_elegido', None)
        programa_nestic = request.json.get('programa_nestic', None)
        numero_piezas_criticas = request.json.get('numero_piezas_criticas', None)
        tiempo_corte = request.json.get('tiempo_corte', None)
        espesor = request.json.get('espesor', None)
        longitud_nestic = request.json.get('longitud_nestic', None)
        
        if not modelo_elegido:
            return jsonify({"msg": "Falta introducir el modelo_elegido"}), 400
        if not programa_nestic:
            return jsonify({"msg": "Falta introducir el nombre del programa_nestic"}), 400
        if not numero_piezas_criticas:
            return jsonify({"msg": "Falta introducir el numero_piezas_criticas"}), 400
        if not tiempo_corte:
            return jsonify({"msg": "Falta introducir el tiempo_corte"}), 400
        if not espesor:
            return jsonify({"msg": "Falta introducir el espesor"}), 400
        if not longitud_nestic:
            return jsonify({"msg": "Falta introducir la longitud_nestic"}), 400
        
        usua = Nestic()
        usua.modelo_elegido = modelo_elegido
        usua.programa_nestic = programa_nestic
        usua.numero_piezas_criticas = numero_piezas_criticas
        usua.tiempo_corte = tiempo_corte
        usua.espesor = espesor
        usua.longitud_nestic = longitud_nestic
        db.session.add(usua)
        db.session.commit()

    data = {
        "Nestic": usua.serialize() 
    }
    return jsonify({'msg': 'Modelo agregado exitosamente'}),  200





@app.route("/api/crearpieza", methods=['POST'])
def crearPiezas():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    if request.method == 'POST':
        
        nombre_pieza = request.json.get('nombre_pieza', None)
        cantidadPiezasPorPlancha = request.json.get('cantidadPiezasPorPlancha', None)
        crearLongitudCortePieza = request.json.get('crearLongitudCortePieza', None)
        nesticElegido = request.json.get('nesticElegido', None)

        
        if not nombre_pieza:
            return jsonify({"msg": "Falta introducir el nombre de la pieza "}), 400
        if not cantidadPiezasPorPlancha:
            return jsonify({"msg": "Falta introducir el nombre la cantidad"}), 400
        if not crearLongitudCortePieza:
            return jsonify({"msg": "Falta introducirla longitud"}), 400
        if not nesticElegido:
            return jsonify({"msg": "Falta seleccionar el programa nestic"}), 400

        
        usua = Piezas()
        usua.nombre_pieza = nombre_pieza
        usua.cantidadPiezasPorPlancha = cantidadPiezasPorPlancha
        usua.crearLongitudCortePieza = crearLongitudCortePieza
        usua.nesticElegido = nesticElegido
        db.session.add(usua)
        db.session.commit()

    data = {
        "Piezas": usua.serialize() 
    }
    return jsonify({'msg': 'Pieza agregada exitosamente'}),  200


@app.route("/api/modelosproduccion", methods=['POST'])
def crearModeloProducion():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    if request.method == 'POST':
        
        modelo_produccion = request.json.get('modelo_produccion', None)
        ot_produccion = request.json.get('ot_produccion', None)
        cantidad_producir = request.json.get('cantidad_producir', None)
        nesticElegido = request.json.get('nesticElegido', None)

        
        if not modelo_produccion:
            return jsonify({"msg": "Falta introducir el modelo "}), 400
        if not ot_produccion:
            return jsonify({"msg": "Falta introducir OT"}), 400
        if not cantidad_producir:
            return jsonify({"msg": "Falta introducirla longitud"}), 400
        
        usua = ModeloProduccion.query.filter_by(ot_produccion=ot_produccion).first()
        if usua:
            return jsonify({"msg": "EL producto ya existe"}), 400

        
        usua = ModeloProduccion()
        usua.modelo_produccion = modelo_produccion
        usua.ot_produccion = ot_produccion
        usua.cantidad_producir = cantidad_producir
        db.session.add(usua)
        db.session.commit()

    data = {
        "Piezas": usua.serialize() 
    }
    return jsonify({'msg': 'Modelo a produccion agregada exitosamente'}),  200



@app.route('/api/Nesticsdisponibles', methods=['GET'])
def nesticsDisponibles():
    if request.method == 'GET':
        listaNestics = Nestic.query.all()
        listaNestics = list(map(lambda listaNestics: listaNestics.serialize(), listaNestics))
        return jsonify(listaNestics), 200


@app.route('/api/nesticsmodelar/<name>', methods=['GET'])
def nesticsModelar(name):
    if request.method == 'GET':
        listaNesticsModelar = Nestic.query.filter_by(modelo_elegido=name).all()
        listaNesticsModelar = list(map(lambda listaNesticsModelar: listaNesticsModelar.serialize(), listaNesticsModelar))
        return jsonify(listaNesticsModelar), 200

@app.route('/api/otProduccion', methods=['GET'])
def otProduccion():
    listaOt = ModeloProduccion.query.all()
    listaOt = list(map(lambda listaOt: listaOt.serialize(), listaOt))
    return jsonify(listaOt), 200


@app.route('/api/nesticProduccion/<int:id>', methods=['GET'])
def nesticProduccion(id):
    
    modelo_ot = Modelo.query.filter_by(numero_ot=id).first()
    print(modelo_ot)
    modelo_ot = modelo_ot.nombre_programa
    print(modelo_ot)
    nesti_ot = Nestic.query.filter_by(modelo_elegido=modelo_ot).all()
    nesti_ot = list(map(lambda nesti_ot: nesti_ot.serialize(), nesti_ot))
    return jsonify(nesti_ot), 200




if __name__ == '__main__':
    manager.run()

