import json
from flask import Flask, Response, abort, request
from about_me import me
from mock_data import catalog
from config import db
from bson import ObjectId
from flask_cors import CORS


app = Flask('dollarsmart')
CORS(app)


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

# POST method to create new products


@app.route("/api/catalog", methods=["POST"])
def save_product():
    try:
        product = request.get_json()
        errors = ""

        if not "title" in product or len(product["title"]) < 5:
            errors = "Title is required and should have at least 5 characters"

        if not "image" in product:
            errors += ", Image is required"

        if not "price" in product or product["price"] < 1:
            errors += ", Price is required and should be >= 1"

        if errors:
            return abort(400, errors)

        db.product.insert_one(product)
        product["_id"] = str(product["_id"])

        return json.dumps(product)

    except Exception as ex:
        return abort(500, F"Unexpected error: {ex}")


@app.route("/api/catalog/count", methods=["GET"])
def get_count():
    cursor = db.products.find({})
    num_items = 0
    for prod in cursor:
        num_items += 1

    return json.dumps(num_items)


@app.route("/api/product/<id>", methods=["GET"])
def get_product(id):
    try:
        if not ObjectId.is_valid(id):
            return abort(400, "Invalid ID")

        product = db.products.find_one({"_id": ObjectId(id)})

        if not product:
            abort(404, "Product not found")

        product["_id"] = str(product["_id"])
        return json.dumps(product)

    except:
        return abort(500, "Unexpected error")


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
    cursor = db.products.find({"category": category})
    category = category.lower()
    for prod in cursor:
        prod["_id"] = str(prod["_id"])
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

######################################################################
####################### COUPON CODES #################################
######################################################################


@app.route("/api/coupons", methods=["GET"])
def get_all_coupons():
    cursor = db.coupons.find({})
    results = []
    for cc in cursor:
        cc["_id"] = str(cc["_id"])
        results.append(cc)

    return json.dumps(results)


@app.route("/api/coupons", methods=["POST"])
def save_coupn():
    try:
        coupon = request.get_json()

        errors = ""
        if not "code" in coupon or len(coupon["code"]) < 5:
            errors += "Coupon should have at least 5 charcters, "

        if not "discount" in coupon or coupon["discount"] < 1 or coupon["discount"] > 50:
            errors += "Discount is required and should be between 1 and 50, "

        if errors:
            return Response(errors, status=400)

        exist = db.coupons.find_one({"code": coupon["code"]})
        if exist:
            return Response("A coupon already exists for that Code", status=400)

        db.coupons.insert_one(coupon)

        coupon["_id"] = str(coupon["_id"])
        return json.dumps(coupon)

    except Exception as ex:
        print(ex)
        return Response("Unexpected error", status=500)


@app.route("/api/coupons/<code>", methods=["GET"])
def get_coupon_by_code(code):

    coupon = db.coupons.find_one({"code": code})
    if not coupon:
        return abort(404, "Coupon not found")

    coupon["_id"] = str(coupon["_id"])
    return json.dumps(coupon)


app.run(debug=True)
