import json
from flask import request
from app import app
from models import db, Bakery, BakedGood

class TestApp:
    '''Test suite for the Flask application.'''

    def setup_method(self, method):
        '''Setup method to initialize the test environment.'''
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def teardown_method(self, method):
        '''Teardown method to clean up the test environment.'''
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def create_baked_good(self, name, price, bakery_id):
        '''Helper method to create a new baked good.'''
        return BakedGood(
            name=name,
            price=price,
            bakery_id=bakery_id
        )

    def test_creates_baked_goods(self):
        '''Test case: can POST new baked goods through "/baked_goods" route.'''
        with app.app_context():
            # Create a test bakery if it doesn't exist
            bakery = Bakery.query.filter_by(id=5).first()
            if not bakery:
                bakery = Bakery(id=5, name="Test Bakery")
                db.session.add(bakery)
                db.session.commit()

            response = self.app.post(
                '/baked_goods',
                data=json.dumps({
                    "name": "Apple Fritter",
                    "price": 2,
                    "bakery_id": 5,
                }),
                content_type='application/json'
            )

            assert response.status_code == 201
            assert response.content_type == 'application/json'

    def test_updates_bakeries(self):
        '''Test case: can PATCH bakeries through "/bakeries/<int:id>" route.'''
        with app.app_context():
            # Create a test bakery if it doesn't exist
            bakery = Bakery.query.filter_by(id=1).first()
            if not bakery:
                bakery = Bakery(id=1, name="Main Bakery")
                db.session.add(bakery)
                db.session.commit()

            response = self.app.patch(
                '/bakeries/1',
                data=json.dumps({
                    "name": "Your Bakery",
                }),
                content_type='application/json'
            )

            assert response.status_code == 200
            assert response.content_type == 'application/json'
            assert bakery.name == "Your Bakery"

    def test_deletes_baked_goods(self):
        '''Test case: can DELETE baked goods through "/baked_goods/<int:id>" route.'''
        with app.app_context():
            # Create a test baked good
            baked_good = self.create_baked_good("Apple Fritter", 2, 5)
            db.session.add(baked_good)
            db.session.commit()

            response = self.app.delete(f'/baked_goods/{baked_good.id}')

            assert response.status_code == 200
            assert response.content_type == 'application/json'
            assert not BakedGood.query.filter_by(name="Apple Fritter").first()
