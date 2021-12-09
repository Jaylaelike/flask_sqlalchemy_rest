from flask import Flask, request, jsonify
from sqlalchemy.sql.expression import desc
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import datetime
from sqlalchemy import Column, Integer, DateTime
from flask_marshmallow import Marshmallow

import os

tz = datetime.datetime.utcnow
print(tz)
# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)



# Product Class/Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chp_margin_main = db.Column(db.String(100))  #, unique=True
    chp_emmis_main = db.Column(db.String(100))
    chp_margin_res = db.Column(db.String(100))  #, unique=True
    chp_emmis_res = db.Column(db.String(100))
    created_date = db.Column(DateTime(timezone=True), default=datetime.datetime.now)
  

    def __init__(self, chp_margin_main, chp_emmis_main, chp_margin_res, chp_emmis_res):
        self.chp_margin_main = chp_margin_main
        self.chp_emmis_main = chp_emmis_main
        self.chp_margin_res = chp_margin_res
        self.chp_emmis_res = chp_emmis_res

# Product Schema


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'chp_margin_main', 'chp_emmis_main', 'chp_margin_res', 'chp_emmis_res', 'created_date')


# Init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Create a Product
@app.route('/product', methods=['POST'])
def add_product():
    chp_margin_main = request.json['chp_margin_main']
    chp_emmis_main = request.json['chp_emmis_main']
    chp_margin_res = request.json['chp_margin_res']
    chp_emmis_res = request.json['chp_emmis_res']

    new_product = Product(chp_margin_main, chp_emmis_main, chp_margin_res, chp_emmis_res)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

# Get All Products
@app.route('/product/', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

# Get limit
@app.route('/product/limit/<limits>', methods=['GET'])
def get_products_limit(limits):
    all_products = Product.query.order_by(Product.id.desc()).limit(limits)
    result = products_schema.dump(all_products)
    return jsonify(result)

# Get Single Products
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

# # Update a Product
# @app.route('/product/<id>', methods=['PUT'])
# def update_product(id):
#     product = Product.query.get(id)

#     name = request.json['name']
#     description = request.json['description']
#     price = request.json['price']
#     qty = request.json['qty']

#     product.name = name
#     product.description = description
#     product.price = price
#     product.qty = qty

#     db.session.commit()

#     return product_schema.jsonify(product)

# # Delete Product
# @app.route('/product/<id>', methods=['DELETE'])
# def delete_product(id):
#     product = Product.query.get(id)
#     db.session.delete(product)
#     db.session.commit()

#     return product_schema.jsonify(product)


# Run Server
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
