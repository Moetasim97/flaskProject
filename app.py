from flask import  Response, jsonify, request
import json
from models import *

response_structure= {
    "results":[],
    "success":False,
    "message":''
}





@app.route('/products',methods=["POST"])
def add_product():
    request_data = request.get_json()
    try:
        Product.add_product(request_data['name'],request_data['price'],request_data['imgUrl'],request_data['quantity'],request_data['category_id'])
        response_structure['results']=request_data
        response_structure['success']=True
        return response_structure
    except:
        response_structure["message"]= "The request body was not valid"
        return response_structure


@app.route("/products/<int:product_id>",methods=["PUT"])
def edit_product(product_id):
    request_data=request.get_json()
    try:
        Product.update_product(product_id,request_data)
        response_structure['results']= Product.get_products()
        response_structure['success']=True
        return response_structure
    except:
        response_structure['message'] = "The structure of the request body is not valid"

@app.route('/products')
def get_categorized_product():
    category_id=request.args.get('categoryId')
    if category_id:
            categorized_products=Product.get_products(category_id)
            response_structure['results']=categorized_products
            response_structure['success']=True
            return response_structure
    else:
            response_structure['results'] = Product.get_products() 
            response_structure['success'] = True
            return response_structure

@app.route('/category')
def get_categories():
    categories= Category.get_categories()
    response_structure['results']=categories
    response_structure['success']=True
    return response_structure




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run()