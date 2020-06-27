import os
from flask import Flask, render_template, jsonify, request, redirect, send_from_directory
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_cors import CORS
from models import db, User, Productos, Factura, Detallefactura, UserAdmini
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://jarb29:Alexander29@servidor/jarb29.mysql.pythonanywhere-services.com'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db')
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

def allowed_file_images(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_IMG



@app.route('/api/admi/administrador', methods=['POST'])
def producto():

    nombre = request.form.get('nombreProducto', None)
    descripcion= request.form.get('descripcion', None)
    precio = request.form.get('precio', None)
    categoria = request.form.get('categoria', None)
    file = request.files['avatar']

  
    if file:
        if file.filename == '': 
            return jsonify({"msg": "Agregar nombre a la foto"}), 400
    if not nombre or nombre =='':
        return jsonify({"msg": "Falta el nombre del producto"}), 400
    if not descripcion or descripcion == '':
        return jsonify({"msg": "Falta la descripcion "}), 400
    if not precio or precio == '':
        return jsonify({"msg": "Falta el precio"}), 400

    if not categoria or categoria == '':
        return jsonify({"msg": "Falta la categoria"}), 400

    if file and allowed_file_images(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], 'img/avatars'), filename))

    usua = Productos.query.filter_by(nombre = nombre).first()
   
    if usua:
        return jsonify({"msg": "EL producto ya existe"}), 400
    usua = Productos()
    usua.nombre = nombre 
    usua.status = 'active'
    usua.descripcion = descripcion
    usua.precio = precio
    usua.categoria = categoria

    if file:
        usua.avatar = filename

    db.session.add(usua)
    db.session.commit()
    data = {
        "Producto": usua.serialize()
    }
    return jsonify({'msg': 'Producto agregado exitosamente'}), 200


@app.route('/api/tienda/tienda/', methods=['GET'])
def tiendaSeleccionada():
    listaProductos = Productos.query.filter_by(categoria='torta').all()
    listaProductos = list(map(lambda listaProductos: listaProductos.serialize(), listaProductos))
    return jsonify(listaProductos), 200


@app.route('/api/tienda/tienda/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], 'img/avatars'), filename)


@app.route('/api/tienda/salsas/', methods=['GET'])
def tiendaSeleccionad():
    listaProductos = Productos.query.filter_by(categoria='salsas').all()
    listaProductos = list(map(lambda listaProductos: listaProductos.serialize(), listaProductos))
    return jsonify(listaProductos), 200


@app.route('/api/tienda/salsas/<filename>')
def uploaded_fil(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], 'img/avatars'), filename)


@app.route("/api/tienda/loging", methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    if request.method == 'POST':
        clave = request.json.get('clave', None)
        email = request.json.get('email', None)


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

@app.route("/api/admini/loging", methods=['POST'])
def loginAdmi():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    if request.method == 'POST':
        clave = request.json.get('clave', None)
        email = request.json.get('email', None)


        if not email:
            return jsonify({"msg": "Falta el email"}), 400
        usua = UserAdmini.query.filter_by(email = email).first()
        if not usua:
            return jsonify({"msg": "Usuario no existe"}), 400
        if not clave:
            return jsonify({"msg": "Falta la clave"}), 400

        if bcrypt.check_password_hash(usua.clave, clave):
            access_token = create_access_token(identity = usua.nombre)
            data = {
                "access_token": access_token,
                "administrador": usua.serialize()
            }
            return jsonify(data), 200
        else:
            return jsonify({"msg": "email/ clave errados favor verificar"}), 401






@app.route('/api/tienda/register', methods=['POST'])
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

@app.route('/api/administrador/register', methods=['POST'])
def registerAdminis():
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
    usua = UserAdmini.query.filter_by(email = email).first()
    if usua:
        return jsonify({"msg": "Usuario existe por favor elegir diferente Email"}), 400
    if not clave:
        return jsonify({"msg": "Falta la clave"}), 400

    usua = UserAdmini()
    usua.nombre = nombre
    usua.clave = bcrypt.generate_password_hash(clave) 
    usua.email = email
    usua.apellido = apellido
    usua.telefono = telefono
    db.session.add(usua)
    db.session.commit()


    access_token = create_access_token(identity=usua.email)
     
    data = {
        "access_token": access_token,
        "Usuario": usua.serialize()
    }
    return jsonify(data),  200



@app.route('/api/tienda/checkout', methods=['PUT'])
def checkout():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    ItemCompradoId= request.json.get('ItemProductoCompradoId', None)
    CantidaProductoComprado = request.json.get('CantidaProductoComprado', None)
    precioProductoSeleccionado = request.json.get('precioProductoSeleccionado', None)
    usuario_id = request.json.get('usuario_id', None)
    totalFactura = request.json.get('totalFactura', None)
    usuarioActual = request.json.get('usuarioActual', None)
    email = User.query.filter_by(id = usuario_id).first().email
    usuario = User.query.filter_by(id = usuario_id).first()

    usua = Factura()
    usua.total = totalFactura
    usua.comprador = usuario 
    db.session.add(usua)
    db.session.commit()
    print(CantidaProductoComprado, "producto que se compro")
       

     #factura_id =Factura.query.filter_by(id = usuario_id).first()
    factura_id = Factura.query.order_by(Factura.id.desc()).first()
    productos = Productos.query.filter(Productos.id.in_(ItemCompradoId)).all()
    i=0
    for prod in productos:
        usua = Detallefactura()
        usua.productos_comprados = prod
        usua.productos_facturados= factura_id
        usua.cantidad_producto_comprado = int(CantidaProductoComprado[i])
        db.session.add(usua)
        db.session.commit()
        i=i+1
    
    # html = render_template('email-compraProductos.html', users=totalProductosComprados)
    # send_mail("Compra", "jarb29@gmail.com", email, html)
    # html = render_template('email-ProductosComprados.html', usuarioactual = usuarioActual, users=totalProductosComprados)
    # send_mail("Productos comprados", "jarb29@gmail.com", emailTiendaSeleccionada, html)
    
    return jsonify({'msg': 'Producto encargados exitamente en breve recibira un email con el detalle'}), 200



@app.route('/api/admi/orders', methods=['GET'])
def orders():
    listaFacturas = Factura.query.all()
    listaFacturas = list(map(lambda listaFacturas: listaFacturas.serialize(), listaFacturas))
    listaDetalleFactura = Detallefactura.query.all()
    listaDetalleFactura = list(map(lambda listaDetalleFactura: listaDetalleFactura.serialize(), listaDetalleFactura))
    return jsonify(listaFacturas, listaDetalleFactura), 200


@app.route('/api/editar/producto/<int:id>', methods=['PUT'])
def editarProducto(id):
    editProducto = Productos.query.get(id)
    status= request.json.get('newStatus', None)
    editProducto.status = status
    db.session.commit()

    return ({'msg': 'Producto actualizado'})  


@app.route('/api/admin/<int:id>', methods=['GET', 'DELETE'])
def productos(id):
    if request.method == 'GET':
        factura_id = Factura.query.filter_by(usuariof_id = id).all()
        listaFacturas = list(map(lambda listaProductos: listaProductos.serialize(), factura_id))
        detallesFacturas = list(map(lambda X: Detallefactura.query.filter_by(facturaf_id  = X.id).all(), factura_id))
        detallesPorFactura = []

        for each in listaFacturas:
            value = Detallefactura.query.filter_by(facturaf_id = each['factura_id']).all()
            for each in value:
                val = each.serialize()
                detallesPorFactura.append(val)
        return jsonify(listaFacturas, detallesPorFactura), 200

if __name__ == '__main__':
    manager.run()

