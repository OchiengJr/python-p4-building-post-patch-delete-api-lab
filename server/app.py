#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json_encoder = None  # Resetting JSON encoder to default for clarity

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET/POST/PATCH/DELETE API</h1>'

@app.route('/bakeries')
def get_bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(jsonify(bakeries), 200)

@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH'])
def update_bakery(id):
    bakery = Bakery.query.get_or_404(id)

    if request.method == 'PATCH':
        for attr, value in request.form.items():
            setattr(bakery, attr, value)
        
        db.session.commit()

        return make_response(jsonify(bakery.to_dict()), 200)

@app.route('/baked_goods', methods=['GET', 'POST'])
def manage_baked_goods():
    if request.method == 'GET':
        baked_goods = [bg.to_dict() for bg in BakedGood.query.all()]
        return make_response(jsonify(baked_goods), 200)
    
    elif request.method == 'POST':
        data = request.form
        baked_good = BakedGood(
            name=data.get("name"),
            price=data.get("price"),
            bakery_id=data.get("bakery_id")
        )

        db.session.add(baked_good)
        db.session.commit()

        return make_response(jsonify(baked_good.to_dict()), 201)

@app.route('/baked_goods/<int:id>', methods=['GET', 'DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get_or_404(id)

    if request.method == 'DELETE':
        db.session.delete(baked_good)
        db.session.commit()
        return make_response(jsonify({'message': 'Record successfully deleted'}), 200)

@app.route('/baked_goods/by_price')
def get_baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_serialized = [bg.to_dict() for bg in baked_goods]
    return make_response(jsonify(baked_goods_serialized), 200)

@app.route('/baked_goods/most_expensive')
def get_most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    most_expensive_serialized = most_expensive.to_dict() if most_expensive else {}
    return make_response(jsonify(most_expensive_serialized), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
