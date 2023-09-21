
from flask_sqlalchemy import SQLAlchemy
import json
from flask import Flask
from flask_migrate import Migrate
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app,db)

class Product(db.Model):
    __tablename__="Product"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    price = db.Column(db.Integer,nullable=False)
    imgUrl = db.Column(db.String(200),nullable=False)
    quantity = db.Column(db.Integer,nullable=False)
    category_id = db.Column(db.Integer,db.ForeignKey('Category.id'),nullable=True)
    category = db.relationship('Category',backref=db.backref('products',lazy=True))

    def json(self):

        return {
            "Name":self.name,"Price":self.price,"Quantity":self.quantity,
            "Image Url":self.imgUrl,"Id":self.id
                }

    def add_product(_name,_price,_imgUrl,_quantity,_category=None):
        if _category == None:
             new_product = Product(name=_name,price=_price,imgUrl=_imgUrl,quantity=_quantity)
        else:
             new_product = Product(name=_name,price=_price,imgUrl=_imgUrl,quantity=_quantity,category_id=_category)
       
        db.session.add(new_product)
        db.session.commit()

    def get_products(_category_id=None):
        if _category_id==None:
            return [Product.json(product) for product in Product.query.all()]
        else:
            return [Product.json(categorized_product) for categorized_product in Product.query.filter_by(category_id=_category_id)]
    
    def get_product_by_name(_name):
        return Product.json(Product.query.filter_by(name=_name).first())
    
    
    def update_product(id,_dict):
        targetProduct = Product.query.filter_by(id=id)
        targetProduct.update(_dict)
        db.session.commit()
        



class Category(db.Model):
    __tablename__="Category"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=False)



    def json(self):
        return {
            "Name":self.name,"Id":self.id
                }

    def add_category(_name):
        new_category= Category(name = _name)
        db.session.add(new_category)
        db.session.commit()

    def get_categories():
        categories= Category.query.all()
        return [Category.json(category) for category in categories]

