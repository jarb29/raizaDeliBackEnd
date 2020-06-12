import os
from flask import Flask, render_template, jsonify, request, redirect, send_from_directory
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_cors import CORS
from models import db, User
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


@app.route("/api/loging", methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    if request.method == 'POST':
        nombre = request.json.get('nombre', None)
        clave = request.json.get('clave', None)
        email = request.json.get('email', None)

        if not nombre:
            return jsonify({"msg": "Falta el nombre"}), 400
        if not email:
            return jsonify({"msg": "Falta el email"}), 400
        usua = User.query.filter_by(email = email).first()
        if not usua:
            return jsonify({"msg": "Usuario no existe"}), 400
        if not clave:
            return jsonify({"msg": "Falta la clave"}), 400

        if bcrypt.check_password_hash(usua.clave, clave):
            access_token = create_access_token(identity = usua.nombre)
            data = {
                "access_token": access_token,
                "Usuario": usua.serialize()
            }
            return jsonify(data), 200
        else:
            return jsonify({"msg": "email/ clave errados favor verificar"}), 401




@app.route('/api/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    nombre = request.json.get('nombre', None)
    clave = request.json.get('clave', None)
    email = request.json.get('email', None)
    apellido = request.json.get('apellido', None)
    telefono = request.json.get('telefono', None)

    if not nombre:
        return jsonify({"msg": "Falta el nombre"}), 400
    if not email:
        return jsonify({"msg": "Falta el email"}), 400
    if not apellido:
        return jsonify({"msg": "Falta el apellido"}), 400
    if not telefono:
        return jsonify({"msg": "Falta el telefono"}), 400
    usua = User.query.filter_by(email = email).first()
    if usua:
        return jsonify({"msg": "Usuario existe por favor elegir diferente Email"}), 400
    if not clave:
        return jsonify({"msg": "Falta la clave"}), 400

    usua = User()
    usua.nombre = nombre
    usua.clave = bcrypt.generate_password_hash(clave) 
    usua.email = email
    usua.apellido = apellido
    usua.telefono = telefono
    db.session.add(usua)
    db.session.commit()
    # html = render_template('email-registerCliente.html', user=usua)
    # send_mail("Registro", "jarb29@gmail.com", usua.email, html)

    access_token = create_access_token(identity=usua.email)
     
    data = {
        "access_token": access_token,
        "Usuario": usua.serialize()
    }
    return jsonify(data),  200



























if __name__ == '__main__':
    manager.run()

