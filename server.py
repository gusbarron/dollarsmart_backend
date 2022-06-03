import json
from flask import Flask, abort
from about_me import me
from mock_data import catalog

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
    return json.dumps(catalog)


@app.route("/api/catalog/count", methods=["GET"])
def get_count():
    counts = len(catalog)
    return json.dumps(counts)


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
    for prod in catalog:
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
    results = []
    for prod in catalog:
        cat = prod["category"]
        if not cat in results:
            results.append(cat)

    return json.dumps(results)


@app.get("/api/product/cheapest")
def get_cheapest_product():
    solution = catalog[0]
    for prod in catalog:
        if prod["price"] < solution["price"]:
            solution = prod

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
