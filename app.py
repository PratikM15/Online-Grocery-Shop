from flask import Flask, request, jsonify, render_template, redirect, session, url_for
from database import database
app = Flask(__name__)

app.secret_key = "DBMS$PROJECT#BY%BUG@MINER"

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    try:
        username = session['username']
        user = database.get_user(username)
    except:
        username = None
    if username == "PratikM":
        if request.method == "POST":
            name = request.form['name']
            price = request.form['price']
            url = request.form['url']
            category = request.form['category']
            total = request.form['total']
            msg = database.add_product(name, price, url, category, total)
            if msg == "success":
                return redirect("admin")
            return render_template('add_product.html', error="Some Error Occurred")
        vegetables = database.get_vegetables()
        fruits = database.get_fruits()
        return render_template('add_product.html', vegetables=vegetables, fruits=fruits)
    return redirect("/")

@app.route('/')
def home():
    try:
        username = session['username']
        user = database.get_user(username)
        fruits = database.get_fruits()
        return render_template('index.html', user=user, fruits=fruits)
    except Exception as e:
        print(e)
        return render_template('index.html')

@app.route('/signin',methods=['GET', 'POST'])
def signin():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = database.login_user(email, password)
        if user == "error":
            return render_template('login.html', error='Invalid Credentials.')
        session['username'] = user[4]
        return redirect('/')
    return render_template('login.html')

@app.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password2']
        msg = database.register_user(name, address, phone, username, email, password)
        if msg == "success":
            return redirect('signin')
        return render_template('register.html', error='Email Already Exists.')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect("/")

@app.route('/products')
def products():
    try:
        username = session['username']
        user = database.get_user(username)
    except:
        user = None
    vegetables = database.get_vegetables()
    fruits = database.get_fruits()
    return render_template('allprod.html', vegetables=vegetables, fruits=fruits, user=user)

@app.route('/add-to-cart/<id>')
def add_to_cart(id):
    try:
        username = session['username']
        user = database.get_user(username)
    except:
        return redirect('signin')
    if user:
        msg = database.add_cart(id, user[0])
        if msg == "success":
            return redirect(url_for('products'))
    return redirect('/')

@app.route('/cart')
def cart():
    try:
        username = session['username']
        user = database.get_user(username)
    except:
        return redirect('signin')
    try:
        cart = database.get_cart(user[0])
    except:
        cart = None
    subtotal = 0
    tax = 0
    total = 0
    if user!=None:
        if cart:
            for item in cart:
                subtotal += int(item[5])
            tax = round(0.18*subtotal)
            total = subtotal + tax
            return render_template('cart.html', cart=cart, address=user[2], subtotal=subtotal, tax=tax, total=total, user=user)
        return render_template('cart.html', msg="Your Cart is Empty.", user=user)
    return redirect('/')
    
@app.route('/checkout')
def checkout():
    try:
        username = session['username']
        user = database.get_user(username)
    except:
        return redirect('signin')
    try:
        cart = database.get_cart(user[0])
    except:
        cart = None
    subtotal = 0
    tax = 0
    total = 0
    if user!=None:
        if cart:
            for item in cart:
                subtotal += int(item[5])
            tax = round(0.18*subtotal)
            total = subtotal + tax
            receipt_id = database.create_receipt(user[0], total)
            if receipt_id == "error":
                return redirect('cart')
            for item in cart:
                msg = database.create_booking(item[1], user[0], item[0], receipt_id)
                if msg=="error":
                    return redirect('cart')
            booking = database.get_booking(receipt_id)
            return render_template('success.html', tax=tax, total=total, subtotal=subtotal, user=user, booking=booking, receipt_id=receipt_id)
    return redirect("/")

@app.route('/minus/<id>')
def minus(id):
    msg = database.minus_cart(id)
    return redirect(url_for('cart'))

@app.route('/addon/<id>')
def addon(id):
    msg = database.addon_cart(id)
    return redirect(url_for('cart'))

@app.route('/delete/<id>')
def delete(id):
    msg = database.delete_cart(id)
    return redirect(url_for('cart'))

@app.route('/delete-produvct/<id>')
def delete_product(id):
    msg = database.delete_product(id)
    return redirect(url_for('admin'))

@app.route('/my-orders')
def my_orders():
    try:
        username = session['username']
        user = database.get_user(username)
    except:
        return redirect('signin')
    try:
        receipt = database.get_receipt(user[0])
    except:
        receipt = None
    data = []
    if user!=None:
        if receipt:
            for order in receipt:
                items = []
                booking = database.get_booking(order[0])
                for item in booking:
                    items.append([item[4], item[5], item[6]])
                data.append([order[0], order[2], items])
            print(data)
            return render_template('booking.html', data=data, user=user)
        return render_template('booking.html', msg="Your have no orders.", user=user)
    return redirect('/')


    
    
if __name__ == "__main__":
    app.run(debug=True)
