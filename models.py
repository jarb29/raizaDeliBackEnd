import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql:jarb29.mysql.pythonanywhere-services.com'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)



class User(db.Model):
    _tablename_ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    clave = db.Column(db.String(100), nullable = False)
    apellido = db.Column(db.String(100), nullable = False)
    telefono = db.Column(db.String(100), nullable = False)
    factura_detalle = db.relationship('Factura',  backref= 'comprador', lazy = True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    

    def __repr__(self):
        return f"usuarios('{self.nombre }', '{self.email}', '{self.clave}', '{self.apellido}', '{self.telefono}', '{self.date_created}')"

    def serialize(self):
        return {
            "id":self.id,
            "nombre": self.nombre,
            "email": self.email,
            "apellido": self.apellido,
            "telefono": self.telefono,
            "date_created": self.date_created
        }

class UserAdmini(db.Model):
    _tablename_ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    clave = db.Column(db.String(100), nullable = False)
    apellido = db.Column(db.String(100), nullable = False)
    telefono = db.Column(db.String(100), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    

    def __repr__(self):
        return f"usuarios('{self.nombre }', '{self.email}', '{self.clave}', '{self.apellido}', '{self.telefono}', '{self.date_created}')"

    def serialize(self):
        return {
            "id":self.id,
            "nombre": self.nombre,
            "email": self.email,
            "apellido": self.apellido,
            "telefono": self.telefono,
            "date_created": self.date_created
        }


class Productos(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable = False)
    avatar = db.Column(db.String(100), nullable = False, default = 'favicon.ico')
    precio = db.Column(db.String(100), nullable = False)
    categoria = db.Column(db.String(100), nullable = False)
    descripcion = db.Column(db.String(500), nullable = False, default = 'active')
    status = db.Column(db.String(100), nullable = False)
    producto_detalle = db.relationship('Detallefactura',  backref= 'productos_comprados', lazy = True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    


    def __repr__(self):
        return f"Productos('{self.nombre}', '{self.avatar}', '{self.precio}', '{self.descripcion }', '{self.categoria}')"

    def serialize(self):
        return {
            "id":self.id,
            "nombre": self.nombre,
            "avatar": self.avatar,
            "precio": self.precio,
            "status": self.status,
            "categoria":self.categoria,
            "descripcion":self.descripcion,
        }  



class Factura(db.Model):
    __tablename__ = 'factura'
    id = db.Column(db.Integer, primary_key=True)
    usuariof_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    total = db.Column(db.String(100), nullable = False)
    factura_detalle = db.relationship('Detallefactura',  backref= 'productos_facturados', lazy = True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"factura('{self.id}', '{self.total}', '{self.date_created}')"

    def serialize(self):
        return {
            "factura_id": self.id,
             "usuario_id": self.comprador.id,
             "usuario_nombre": self.comprador.nombre,
             "usuario_email": self.comprador.email,
             "usuario_apellido": self.comprador.apellido,
             "usuario_telefono": self.comprador.telefono,
             "dia_usuario_abrio_cuenta": self.comprador.date_created,
             "total": self.total,
             "factura_creada": self.date_created ,
        }  


class Detallefactura(db.Model):
    __tablename__ = 'detallefactura'
    id = db.Column(db.Integer, primary_key=True)
    facturaf_id = db.Column(db.Integer, db.ForeignKey('factura.id'), nullable=True)
    productof_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=True)
    cantidad_producto_comprado = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Detallefactura('{self.id}', '{self.facturaf_id}', '{self.productof_id}', '{self.cantidad_producto_comprado}', '{self.date_created}')"

    def serialize(self):
        return {
            "detalle_factura_id": self.id,
            "productos_usuario_id": self.productos_facturados.usuariof_id,
            "factura_id": self.productos_facturados.id,
            "total_factura": self.productos_facturados.total,
            "productos_id": self.productos_comprados.id,
            "producto_nombre": self.productos_comprados.nombre,
            "productos_precio": self.productos_comprados.precio,
            "productos_categoria": self.productos_comprados.categoria,
            "productos_descripcion": self.productos_comprados.descripcion,
            "cantidad_producto_comprado": self.cantidad_producto_comprado,
            "date_created": self.date_created,
        }  
