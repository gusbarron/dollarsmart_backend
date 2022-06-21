import json
from flask import Flask, abort, request
from about_me import me
from mock_data import catalog
from config import db
from bson import ObjectId 


app = Flask('dollarsmart')


@app.route("/", methods=['GET'])  # root
def home():
    return "This is the home page"


# create an about endpoint and show you name
@app.route("/about")
def about():
    return me["first"] + " " + me["last"]


@app.route("/myaddress")
def address():
    return f'{me["address"]["street"]}{me["address"]["number"]}'


#########################################################
##################### API ENDPOINTS #####################
#########################################################

@app.route("/api/catalog", methods=["GET"])
def get_catalog():
    results = []
    cursor = db.products.find({})

    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        results.append(prod)

    return json.dumps(results)

#POST method to create new products
@app.route("/api/catalog", methods=["POST"])
def save_product():
    product = request.get_json()
    db.product.insert_one(product)    
    product["_id"] = str(product["_id"])

    return json.dumps(product)



@app.route("/api/catalog/count", methods=["GET"])
def get_count():
    cursor = db.products.find({})
    num_items = 0
    for prod in cursor:
        num_items += 1

    return json.dumps(num_items)


@app.route("/api/product/<id>", methods=["GET"])
def get_product(id):

    for prod in catalog:
        if prod["_id"] == id:
            return json.dumps(prod)

    return abort(404, "Id does not match any product")


# create and endpoint that returns the sum of all the prices
@app.route("/api/catalog/total")
def get_total():
    total = 0
    cursor = db.products.find({})
    for prod in cursor:
        total += prod["price"]

    return json.dumps(total)


@app.get("/api/products/<category>")
def products_by_category(category):
    results = []
    category = category.lower()
    for prod in catalog:
        if prod["category"].lower == category:
            results.append(prod)

    return json.dumps(results)


@app.get("/api/categories")
def get_unique_categories():
    cursor = db.products.find({})
    results = []
    for prod in cursor:
        cat = prod["category"]
        if not cat in results:
            results.append(cat)

    return json.dumps(results)


@app.get("/api/product/cheapest")
def get_cheapest_product():
    cursor = db.products.find({})
    solution = cursor[0]
    for prod in cursor:
        if prod["price"] < solution["price"]:
            solution = prod

    solution["_id"] = str(solution["_id"])
    return json.dumps(solution)


@app.get("/api/exercise1")
def get_exe1():
    nums = [123, 123, 654, 124, 8865, 532, 4768, 8476, 45762,
            345, -1, 234, 0, -12, -456, -123, -865, 532, 4768]
    solution = {}

    # A: find the lowest number
    solution["a"] = 1

    # B: find how many numbers are lowe than 500
    solution["b"] = 1

    # C: sum all the negatives
    solution["c"] = 1

    # D: find the sum of numbers except negatives
    solution["d"] = 1

    return json.dumps(solution)


app.run(debug=True)
