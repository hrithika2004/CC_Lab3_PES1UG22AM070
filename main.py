import json

import flask
import jwt
from flask import render_template, request, redirect, url_for
from functools import wraps  #added this for cart optimization
import products
from auth import do_login, sign_up
from products import list_products
#from cart import add_to_cart as ac, get_cart, remove_from_cart, delete_cart
from cart import get_cart, add_to_cart, remove_from_cart, delete_cart
from checkout import checkout as chk, complete_checkout
import os

app = flask.Flask(__name__)
app.template_folder = 'templates'
SRN = "PES1UG22AM070"

if(SRN[-3:]=="XXX"):
    print("Please update your SRN on line 15")
    os._exit(1)

@app.route('/')
def index():
    return redirect(url_for('browse'))

#for cart opti
# Helper function for decoding JWT and retrieving username
def get_username_from_token():
    token = request.cookies.get('token')
    if token is None:
        return None
    try:
        decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
        return decoded.get('sub')
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Decorator to ensure the user is authenticated
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        username = get_username_from_token()
        if not username:
            return redirect(url_for('login'))
        return f(username, *args, **kwargs)
    return decorated_function

#optimized cart
@app.route('/cart')
@login_required
def cart(username):
    cart_items = get_cart(username)  # Fetch the cart items for the user
    return render_template('cart.jinja', cart=cart_items, srn=SRN)

@app.route('/cart/remove/<id>', methods=['POST'])
@login_required
def remove_cart_item(username, id):
    try:
        remove_from_cart(username, int(id))  # Remove the specific item from the user's cart
    except ValueError:
        return "Invalid product ID", 400  # Handle invalid IDs gracefully
    return redirect(url_for('cart'))

@app.route('/cart/delete', methods=['GET'])
@login_required
def delete_cart_item(username):
    delete_cart(username)  # Delete all items in the user's cart
    return redirect(url_for('cart'))

@app.route('/cart/<id>', methods=['POST'])
@login_required
def add_to_cart(username, id):
    try:
        add_to_cart(username, int(id))  # Add the item to the user's cart
    except ValueError:
        return "Invalid product ID", 400  # Handle invalid IDs gracefully
    return redirect(url_for('cart'))


@app.route('/product/<product_id>')
def product(product_id):
    product = products.get_product(product_id)
    return flask.render_template('product_view.jinja', product=product,srn=SRN)


@app.route("/product", methods=['GET', 'POST'])
def product_page():
    if request.method == 'POST':
        print(request.form)
        product_name = request.form['product_name']
        product_cost = request.form['product_cost']
        product_quantity = request.form['product_quantity']
        product_description = request.form['product_description']
        products.add_product({"name": product_name, "cost": product_cost, "qty": product_quantity,
                              "description": product_description})
        # return "Success", 200, {"Access-Control-Allow-Origin": "*"}
        return 'ok'
    else:
        return flask.render_template('product.jinja',srn=SRN)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # handle the login form submission
        username, password = request.form['username'], request.form['password']
        try:
            token = do_login(username, password)
            resp = flask.make_response(redirect(url_for('browse')))
            resp.set_cookie('token', token)
            return resp
        except ValueError as e:
            response = flask.make_response({'error': str(e)})
            response.status_code = 401
            return response
    else:
        # render the login page with a form
        return render_template('login.jinja',srn=SRN)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # handle the register form submission
        username, password = request.form['username'], request.form['password']
        try:
            sign_up(username, password)
            return redirect(url_for('login'))
        except ValueError as e:
            response = flask.make_response({'error': str(e)})
            response.status_code = 400
            return response
    return render_template('signup.jinja',srn=SRN)


#optimising for /browse
@app.route("/browse")
def browse():
    """
    Render the /browse page with a list of products.
    """
    # Fetch all products using the optimized list_products function
    items = list_products()
    
    # Pass the items to the template for rendering
    return render_template('browse.jinja', items=items, srn=SRN)


@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    token = request.cookies.get('token')
    if token is None:
        return redirect(url_for('login'))
    dec = jwt.decode(token, 'secret', algorithms=['HS256'])
    username = dec['sub']
    if request.method == 'GET':
        total = chk(username)
        return render_template('checkout.jinja', total=total,srn=SRN)
    else:
        resp = flask.make_response(redirect(url_for('browse')))
        return resp

@app.route("/payment", methods=['GET'])
def payment():
    token = request.cookies.get('token')
    if token is None:
        return redirect(url_for('login'))
    dec = jwt.decode(token, 'secret', algorithms=['HS256'])
    username = dec['sub']
    complete_checkout(username)
    return render_template('payment.jinja',srn=SRN)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

