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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)



class User(db.Model):
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
    descripcion = db.Column(db.String(500), nullable = False)


    def __repr__(self):
        return f"Productos('{self.nombre}', '{self.avatar}', '{self.precio}', '{self.descripcion }', '{self.categoria}')"

    def serialize(self):
        return {
            "id":self.id,
            "nombre": self.nombre,
            "avatar": self.avatar,
            "precio": self.precio,
            "categoria":self.categoria,
            "descripcion":self.descripcion,
        }  



