from app import app
from models import db, Bakery, BakedGood

def seed_database():
    with app.app_context():
        # Delete existing records to ensure a clean slate
        BakedGood.query.delete()
        Bakery.query.delete()
        
        # Create bakery instances
        bakeries = [
            Bakery(name='Delightful Donuts'),
            Bakery(name='Incredible Crullers')
        ]
        db.session.add_all(bakeries)
        db.session.commit()

        # Create baked good instances
        baked_goods = [
            BakedGood(name='Chocolate Dipped Donut', price=2.75, bakery=bakeries[0]),
            BakedGood(name='Apple-Spice Filled Donut', price=3.50, bakery=bakeries[0]),
            BakedGood(name='Glazed Honey Cruller', price=3.25, bakery=bakeries[1]),
            BakedGood(name='Chocolate Cruller', price=3.40, bakery=bakeries[1])
        ]
        db.session.add_all(baked_goods)
        db.session.commit()

if __name__ == "__main__":
    seed_database()
