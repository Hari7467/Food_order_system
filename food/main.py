from flask import Flask, render_template, request, redirect, url_for, session
import os
import json
from werkzeug.utils import secure_filename
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb+srv://harivijayan2004:97041208@cluster0.jpzey.mongodb.net/?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true")
db = client['cloudmini']
food_collection = db["foodcollection"]

app = Flask(__name__)
app.secret_key = "food_ordering_secret_key"  # For session management

# Helper function to find food item by ID
def get_food_item_by_id(food_id):
    FOOD_ITEMS = list(food_collection.find({}, {"_id": 0}) )
    for item in FOOD_ITEMS:
        if item['id'] == food_id:
            return item
    return None

@app.route('/')
def welcome():
    """Welcome page with company info and order button"""
    return render_template('welcome.html')

@app.route('/menu')
def menu():
    """Home/Menu page showing all food items"""
    FOOD_ITEMS = list(food_collection.find({}, {"_id": 0}) )
    return render_template('menu.html', food_items=FOOD_ITEMS)

@app.route('/order/<int:food_id>')
def order(food_id):
    """Order page for a specific food item"""
    food_item = get_food_item_by_id(food_id)
    if not food_item:
        return redirect(url_for('menu'))
    
    return render_template('order.html', food=food_item)

@app.route('/place_order', methods=['POST'])
def place_order():
    """Process order form and redirect to confirmation"""
    food_id = int(request.form.get('food_id'))
    quantity = int(request.form.get('quantity', 1))
    
    food_item = get_food_item_by_id(food_id)
    if not food_item:
        return redirect(url_for('menu'))
    
    # Calculate total price
    total_price = food_item['price'] * quantity
    
    # Store order in session (in a real app, this would go to a database)
    order_data = {
        'food': food_item,
        'quantity': quantity,
        'total_price': total_price
    }
    session['order'] = order_data
    
    return redirect(url_for('confirmation'))

@app.route('/confirmation')
def confirmation():
    """Order confirmation page showing order details"""
    order_data = session.get('order', None)
    if not order_data:
        return redirect(url_for('menu'))
    
    # Clear session after showing confirmation
    # In a real app, keep the order information in the database
    # session.pop('order', None)
    
    return render_template('confirmation.html', order=order_data)

if __name__ == '__main__':
    app.run(debug=True)
