import sqlite3
import datetime

conn = sqlite3.connect('data.db')
conn.execute("""
CREATE TABLE IF NOT EXISTS customer(
  customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
  customer_name varchar(100) NOT NULL,
  address varchar(500) NOT NULL,
  contact varchar(100) NOT NULL,
  username varchar(100) NOT NULL,
  email varchar(100) NOT NULL UNIQUE,
  password varchar(100) NOT NULL
);
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS product(
  product_id INTEGER PRIMARY KEY AUTOINCREMENT,
  product_name varchar(100) NOT NULL,
  product_price varchar(50) NOT NULL,
  image_url varchar(100) NOT NULL,
  category varchar(50) NOT NULL,
  total_quantity int NOT NULL
);
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS cart(
  cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id int,
  customer_id int,
  product_name varchar(100) NULL,
  quantity varchar(50) NOT NULL,
  price varchar(50) NOT NULL,
  foreign key(product_id) references product(product_id),
  foreign key(customer_id) references customer(customer_id)
);
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS booking(
  order_id INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id int,
  customer_id int,
  receipt_id int,
  product_name varchar(100) NULL,
  quantity varchar(50) NOT NULL,
  price varchar(50) NOT NULL,
  foreign key(product_id) references product(product_id),
  foreign key(customer_id) references customer(customer_id),
  foreign key(receipt_id) references receipt(receipt_id)
);
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS receipt(
  receipt_id INTEGER PRIMARY KEY AUTOINCREMENT,
  customer_id int,
  total_amount varchar(50) NOT NULL,
  foreign key(customer_id) references customer(customer_id)
);
""")

conn.close()

def register_user(name, address, contact, username, email, password):
    try:
        conn = sqlite3.connect('data.db') 
        result = conn.execute("SELECT customer_name FROM customer").fetchall()
        id = len(result)+1
        name = "'"+name+"'"
        address = "'"+address+"'"
        contact = "'"+contact+"'"
        username = "'"+username+"'"
        email = "'"+email+"'"
        password = "'"+password+"'"
        query = "INSERT INTO customer VALUES ("+str(id)+", "+name+", "+address+", "+contact+", "+username+", "+email+", "+password+ ");"
        conn.execute(query)
        conn.commit()
        conn.close()
        return("success")
    except Exception as e:
        print(e)
        return("error")

def login_user(email, password):
    try:
        conn = sqlite3.connect('data.db') 
        email = "'"+email+"'"
        password = "'"+password+"'"
        query = "SELECT * FROM customer WHERE email="+email+" AND password="+password+" ;"
        user = conn.execute(query).fetchone()
        conn.close()
        if user != []:
            return user
        return("error")
    except:
        return("error")
    
def get_user(username):
    try:
        username = "'"+username+"'"
        conn = sqlite3.connect('data.db')
        query = "SELECT * FROM customer WHERE username="+username+" ;"
        user = conn.execute(query).fetchone()
        conn.close()
        return user
    except:
        return None
    
def get_vegetables():
    try:
        conn = sqlite3.connect('data.db')
        query = "SELECT * FROM product WHERE category='Vegetables' ;"
        vegetables = conn.execute(query).fetchall()
        conn.close()
        print(vegetables)
        return vegetables
    except Exception as e:
        print(e)
        return None
    
def get_fruits():
    try:
        conn = sqlite3.connect('data.db')
        query = "SELECT * FROM product WHERE category='Fruits' ;"
        fruits = conn.execute(query).fetchall()
        conn.close()
        return fruits
    except:
        return None
    
    
def add_product(name, price, url, category, total):
    try:
        conn = sqlite3.connect('data.db') 
        result = conn.execute("SELECT * FROM product").fetchall()
        cur = datetime.datetime.now()
        id = str(cur.year) + str(cur.month) + str(cur.day) + str(ord(name[0])) + str(ord(name[1])) + str(ord(name[2]))
        name = "'"+name+"'"
        price = "'"+price+"'"
        url = "{{url_for('static', filename='"+url+"')}}"
        url = '"'+url+'"'
        category = "'"+category+"'"
        total = "'"+total+"'"
        query = "INSERT INTO product VALUES ("+str(id)+", "+name+", "+price+", "+url+", "+category+", "+total+ ");"
        print(query)
        conn.execute(query)
        conn.commit()
        conn.close()
        return("success")
    except Exception as e:
        print(e)
        return("error")
    
def add_cart(product_id, user_id):
    try:
        conn = sqlite3.connect('data.db') 
        query = "SELECT * FROM cart WHERE customer_id="+str(user_id)+";"
        result = conn.execute(query).fetchall()
        cur = datetime.datetime.now()
        id = str(product_id) + str(user_id)
        query = "SELECT * FROM product WHERE product_id="+str(product_id)+";"
        prod = conn.execute(query).fetchone()
        product_name = prod[1]
        product_name = "'"+product_name+"'"
        quantity = 1
        price = prod[2]
        query = "INSERT INTO cart VALUES ("+str(id)+", "+str(product_id)+", "+str(user_id)+", "+product_name+", "+str(quantity)+", "+str(price)+ ");"
        conn.execute(query)
        conn.commit()
        conn.close()
        return("success")
    except Exception as e:
        print(e)
        return("error")
    
def get_cart(user_id):
    try:
        conn = sqlite3.connect('data.db')
        query = "SELECT * FROM cart WHERE customer_id="+str(user_id)+" ;"
        cart = conn.execute(query).fetchall()
        conn.close()
        return cart
    except:
        return None
    
def create_receipt(customer_id, total):
    try:
        conn = sqlite3.connect('data.db') 
        cur = datetime.datetime.now()
        id = str(cur.year) + str(cur.month) + str(cur.day) + str(cur.hour)+ str(cur.minute) + str(cur.second) + str(customer_id)
        query = "INSERT INTO receipt VALUES ("+str(id)+", "+str(customer_id)+", "+str(total)+ ");"
        conn.execute(query)
        conn.commit()
        conn.close()
        return(id)
    except Exception as e:
        print(e)
        return("error")

def create_booking(product_id, user_id, cart_id, receipt_id):
    try:
        conn = sqlite3.connect('data.db') 
        query = "SELECT * FROM booking WHERE customer_id="+str(user_id)+";"
        result = conn.execute(query).fetchall()
        cur = datetime.datetime.now()
        id = str(receipt_id) + str(user_id)
        query = "SELECT * FROM product WHERE product_id="+str(product_id)+";"
        prod = conn.execute(query).fetchone()
        product_name = prod[1]
        product_name = "'"+product_name+"'"
        query = "SELECT * FROM cart WHERE cart_id="+str(cart_id)+";"
        item = conn.execute(query).fetchone()
        quantity = item[4]
        price = item[5]
        query = "INSERT INTO booking VALUES ("+str(id)+", "+str(product_id)+", "+str(user_id)+", "+str(receipt_id)+", "+product_name+", "+str(quantity)+", "+str(price)+ ");"
        print(query)
        conn.execute(query)
        conn.commit()
        conn.close()
        return("success")
    except Exception as e:
        print(e)
        return("error")
    
def minus_cart(cart_id):
    try:
        conn = sqlite3.connect('data.db')
        query = "SELECT * FROM cart WHERE cart_id="+str(cart_id)+" ;"
        result = conn.execute(query).fetchone()
        prod_id = result[1]
        query = "SELECT * FROM product WHERE product_id="+str(prod_id)+" ;"
        prod = conn.execute(query).fetchone()
        price = int(prod[2])
        quantity = result[4]
        if quantity== "1":
            delete_cart(cart_id)
        else:
            quantity = int(quantity)-1
            price = price * int(quantity)
            query = "UPDATE cart SET quantity="+str(quantity)+", price="+str(price)+" WHERE cart_id="+str(cart_id)+" ;"
            cart = conn.execute(query)
            conn.commit()
            conn.close()
        return "success"
    except:
        return "error"
    
def addon_cart(cart_id):
    try:
        conn = sqlite3.connect('data.db')
        query = "SELECT * FROM cart WHERE cart_id="+str(cart_id)+" ;"
        result = conn.execute(query).fetchone()
        prod_id = result[1]
        query = "SELECT * FROM product WHERE product_id="+str(prod_id)+" ;"
        prod = conn.execute(query).fetchone()
        price = int(prod[2])
        quantity = result[4]
        quantity = int(quantity)+1
        price = price * int(quantity)
        query = "UPDATE cart SET quantity="+str(quantity)+", price="+str(price)+" WHERE cart_id="+str(cart_id)+" ;"
        cart = conn.execute(query)
        conn.commit()
        conn.close()
        return "success"
    except:
        return "error"
    
def delete_cart(cart_id):
    try:
        conn = sqlite3.connect('data.db')
        query = "DELETE FROM cart WHERE cart_id="+str(cart_id)+" ;"
        cart = conn.execute(query)
        conn.commit()
        conn.close()
        return "success"
    except:
        return "error"
    
def get_booking(receipt_id):
    try:
        conn = sqlite3.connect('data.db')
        query = "SELECT * FROM booking WHERE receipt_id="+str(receipt_id)+" ;"
        booking = conn.execute(query).fetchall()
        conn.close()
        return booking
    except:
        return None  
    
def get_receipt(customer_id):
    try:
        conn = sqlite3.connect('data.db')
        query = "SELECT * FROM receipt WHERE customer_id="+str(customer_id)+" ;"
        receipt = conn.execute(query).fetchall()
        conn.close()
        return receipt
    except:
        return None  
    
def delete_product(product_id):
    try:
        conn = sqlite3.connect('data.db')
        query = "DELETE FROM product WHERE product_id="+str(product_id)+" ;"
        cart = conn.execute(query)
        conn.commit()
        conn.close()
        return "success"
    except:
        return "error"
    