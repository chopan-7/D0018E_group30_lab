<<<<<<< HEAD
#-*- coding: -utf-8 -*-
# installed libs
from flask import *
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

# created libs
=======
from flask import *
from flask_mysqldb import MySQL
from forms import RegistrationForm, LoginForm, ReviewForm
from werkzeug.security import generate_password_hash, check_password_hash
>>>>>>> osc
from SQLfunctions import *
<<<<<<< HEAD
from flask import json
=======
import datetime
>>>>>>> master


app = Flask(__name__)

app.config['SECRET_KEY'] = 'bdb878ef8ea259ef877a3686726cf4f9'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Choss!95'
app.config['MYSQL_DB'] = 'webshop'
<<<<<<< HEAD
app.config['MYSQL_HOST'] = 'localhost'
mysql = MySQL(app)



@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')


@app.route("/product")
def product():
    args = request.args
    item = getRow('products', 'prodID=' + args.get("id"))
    return render_template('productpage.html', item=item)
=======
>>>>>>> master

mysql = MySQL(app)

<<<<<<< HEAD
#TODO: Kontroll om användaren redan finns i databasen.
## REGISTER PAGE ##
=======
>>>>>>> osc
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        hashed_password = generate_password_hash(form.password.data)
        cur.execute('INSERT INTO customers (firstname,lastname,email, password, address, postcode, country, phoneno) VALUE(%s,%s,%s,%s,%s,%s,%s, %s)',(form.first_name.data, form.last_name.data, form.email.data, hashed_password, form.home_address.data,form.post_code.data, form.country.data, form.phone_number.data))
        mysql.connection.commit()
        flash('You Have Created An Account!', 'success')
        return redirect('/')
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        email = form.email.data
        cur.execute('SELECT * FROM customers WHERE email = %s', [email])
        data = cur.fetchall()

        if len(data) > 0:
            if check_password_hash(str(data[0][4]), form.password.data):
                session['userid'] = data[0][0]
<<<<<<< HEAD
                session['username'] = data[0][1]
=======
>>>>>>> osc
                flash('You Are Now Logged In!', 'success')
                return redirect('/')
            else:
                flash('Invalid Email Or Password', 'danger')
        else:
            flash('Invalid Email Or Password', 'danger')
    return render_template('login.html', form=form)

<<<<<<< HEAD

@app.route("/customerMypage")
def customerMypage():

    return render_template('customerMypage.html')


<<<<<<< HEAD
@app.route("/getcustomerMypage")
def getcustomerMypage():
    if 'userid' not in session:
        flash('Please log in or create an account.', 'danger')
        return redirect('/login')
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM customers WHERE custID = %s', [session['userid']])
    data = cur.fetchall()

    data_dict = []
    for x in data:
        x_dict = {
            'Firstname': x[1],
            'Lastname': x[2],
            'Email': x[3],
            'Address': x[5],
            'Postcode': x[6],
            'Country': x[7],
            'Phone': x[8]}
        data_dict.append(x_dict)
    return json.dumps(data_dict)


@app.route("/customerMypage")
def customerMypage():
    return render_template('customerMypage.html')
=======
=======
>>>>>>> osc
## INDEX PAGE ##
@app.route('/')
def index():
    # Fetch all rows from product-table
    prod = getTable('products')
    return render_template('index.html', prod = prod)


## PRODUCT PAGE ##
@app.route('/product', methods=['GET', 'POST'])
def product():
    form = ReviewForm()
    args = request.args
    item = getRow('products', 'prodID='+args.get("id"))
    rev = getTable('reviews WHERE prodID=%s'%(item[0]))
    ## SUBMITTING REVIEWS ##
    if request.method=='POST':
        prodID = item[0]
        custID = str(session['userid'])
        text = form.text.data
        date = '12'
        attr = 'prodID, custID, text, date'
        val = '%s, %s, "%s", %s' %(prodID, custID, text, date)
        insertTo('reviews', attr, val)
        flash('Thank you for leaving a review!', 'success')
        return redirect('/')
    return render_template('productpage.html', item = item, form=form, rev=rev)

>>>>>>> master

## ADD TO CART FUNCTION ##
@app.route('/addtocart')
def addtocart():
    # redirect user to login page if not logged in
    if 'userid' not in session:
        flash('Please log in or create an account.', 'danger')
        return redirect('/login')
    
    # attribute data for shoping cart
    custID = str(session['userid'])  # temporary customer ID (unregistred user)
    prodID = str(request.args.get('id')) # productID
    qty = str(request.args.get('qty'))   # quantity
    cond = 'custID = '+custID+' AND prodID = '+prodID   # insert/update condition
    
    # check if the product already exists in users cart
    if exist('cart', cond):
        inCart = getRow('cart', cond)
        # increase the quantity of existing product
        addqty = str(int(inCart[3])+int(qty))
        updateAll('cart', 'qty='+addqty, cond)
    else:
        # add new product to the cart
        attr = 'custID, prodID, qty'
        values = '%s, %s, %s' %(custID, prodID, qty)
        insertTo('cart', attr, values)

    flash('Product has been added to the shopping cart.', 'success')
<<<<<<< HEAD
    return redirect('/product?id=' + prodID)


## CART PAGE ##
@app.route('/cart')
def cart():
    # redirect user to login page if not logged in
    if 'userid' not in session:
        flash('Please log in or create an account.', 'danger')
        return redirect('/login')
    attr = 'cart.prodID, products.name, cart.qty'
    join = 'products ON cart.prodID = products.prodID'
    cond = 'cart.custID = 1891'
    cart = innerJoin('cart', attr, join, cond)
    lenofcart = len(cart)
    return render_template('cart.html', cart = cart, lenofcart=lenofcart)

## UPDATE CART FUNCTION ##
@app.route('/updatecart')
def updatecart():
    # redirect user to login page if not logged in
    if 'userid' not in session:
        flash('Please log in or create an account.', 'danger')
        return redirect('/login')

    custID = str(session['userid'])  # temporary customer ID (unregistred user)
    prodID = str(request.args.get('id')) # productID
    qty = str(request.args.get('qty'))   # quantity
    cond = 'custID = '+custID+' AND prodID = '+prodID   # insert/update condition
    updateIn('cart', 'qty', qty, cond)
    flash('The cart has been updated.', 'success')
    return redirect('/cart')

## CLEAR CART FUNCTION ##
@app.route('/clearcart')
def clearcart():
    # redirect user to login page if not logged in
    if 'userid' not in session:
        flash('Please log in or create an account.', 'danger')
        return redirect('/login')
    deleteFrom('cart', 'custID='+str(session['userid']))
    return redirect('/cart')


@app.route('/confirmclear')
def confirmclear():
    return redirect('/cart?confirm=True')



@app.route('/startadmin')
def startsess():
    session['userid'] = 1891
    session['username'] = 'admin'
    return redirect('/')
=======
    return redirect('/product?id='+prodID)

>>>>>>> master

#TODO: Bekräfta order funktion
## CART PAGE ##
@app.route('/cart')
def cart():
    # redirect user to login page if not logged in
    if 'userid' not in session:
        flash('Please log in or create an account.', 'danger')
        return redirect('/login')
    attr = 'cart.prodID, products.name, cart.qty'
    join = 'products ON cart.prodID = products.prodID'
<<<<<<< HEAD
    cond = 'cart.custID ='+str(session['userid'])
=======
    cond = 'cart.custID = '+str(session['userid'])
>>>>>>> cho
    cart = innerJoin('cart', attr, join, cond)
    lenofcart = len(cart)
    return render_template('cart.html', cart = cart, lenofcart=lenofcart)

<<<<<<< HEAD
## ADMIN PAGES ##
@app.route('/admin/customers')
def admin_customers():
    # denies access to admin pages if not admin
    if 'userid' not in session or session['userid'] != 1891:
        flash('Permission denied!', 'danger')
        return redirect('/')
    return render_template('admin/customers.html')


@app.route('/admin/products')
def admin_products():
    # denies access to admin pages if not admin
    if 'userid' not in session or session['userid'] != 1891:
        flash('Permission denied!', 'danger')
        return redirect('/')
    # product subpages
    page = request.args.get('page') # page-path
    res = getTable('products')      # product-start-page "shows all products"

    # page: showall
    if page == 'showall':
        res = getTable('products')
    return render_template('admin/productpage.html', prod=res)


@app.route('/admin/orders')
def admin_orders():
    # denies access to admin pages if not admin
    if 'userid' not in session or session['userid'] != 1891:
        flash('Permission denied!', 'danger')
        return redirect('/')
    return render_template('admin/orders.html')


=======
## UPDATE CART FUNCTION ##
@app.route('/updatecart')
def updatecart():
    # redirect user to login page if not logged in
    if 'userid' not in session:
        flash('Please log in or create an account.', 'danger')
        return redirect('/login')

    custID = str(session['userid'])  # temporary customer ID (unregistred user)
    prodID = str(request.args.get('id')) # productID
    qty = str(request.args.get('qty'))   # quantity
    cond = 'custID = '+custID+' AND prodID = '+prodID   # insert/update condition
    updateIn('cart', 'qty', qty, cond)
    flash('The cart has been updated.', 'success')
    return redirect('/cart')

## CLEAR CART FUNCTION ##
@app.route('/clearcart')
def clearcart():
    # redirect user to login page if not logged in
    if 'userid' not in session:
        flash('Please log in or create an account.', 'danger')
        return redirect('/login')
    deleteFrom('cart', 'custID='+str(session['userid']))
    return redirect('/cart')

@app.route('/confirmclear')
def confirmclear():
    return redirect('/cart?confirm=True')


# länk för att cleara session
>>>>>>> master
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# länk för att starta admin session
@app.route('/startadmin')
def startsess():
    session['userid'] = 1891
    session['username'] = 'admin'
    return redirect('/')

<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> master
if __name__ == '__main__':
    app.run(debug=True)
=======

## ADMIN - CUSTOMER PAGES ##
@app.route('/admin/customers')
def admin_customers():
    # denies access to admin pages if not admin
    if 'userid' not in session or session['userid'] != 1891:
        flash('Permission denied!', 'danger')
        return redirect('/')
    return render_template('admin/customers.html')

## ADMIN - PRODUCT PAGES ##
@app.route('/admin/products', methods=['GET', 'POST'])
def admin_products():
    # denies access to admin pages if not admin
    if 'userid' not in session or session['userid'] != 1891:
        flash('Permission denied!', 'danger')
        return redirect('/')

    # define page
    page = 'products'

    # initialize searchbar
    form = adminProdSearch()

    # seach by item number or product name
    if request.method=='POST':
        searchWord = str(form.search.data)
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM products WHERE name LIKE "%'+searchWord+'%" OR prodID LIKE "%'+searchWord+'%"')
        res = cur.fetchall()
        cur.close()
    else:
        res = getTable('products')      # default "show all products"

    # error message on search
    if len(res) == 0:
        flash('Your search "'+form.search.data+'" did not match any product(s).', 'warning')

    return render_template('admin/products.html', form=form, prod=res, p=page)

@app.route('/admin/product/edit', methods=['GET', 'POST'])
def admin_products_edit():
    # denies access to admin pages if not admin
    if 'userid' not in session or session['userid'] != 1891:
        flash('Permission denied!', 'danger')
        return redirect('/')
    
    # define page
    page = 'Edit'

    # initalize edit form
    editform = adminProdEdit()

    # update the product
    if request.method == 'POST':
        update = 'name="%s", desc="%s", price=%s, img="%s", stock=%s, category=%s, discount=%s' %(editform.name.data, editform.desc.data, editform.price.data, editform.img.data, editform.stock.data, editform.cat.data, editform.discount.data)
        cond = 'prodID = %s' %(request.args.get('prodID'))
        return updateAll('products', update, cond)
    # default show the product
    else:
        res = getRow('products', 'prodID ='+request.args.get('id'))

    return render_template('admin/products.html', p=page, form=editform, item=res)
    


## ADMIN - ORDER PAGES ##
@app.route('/admin/orders')
def admin_orders():
    # denies access to admin pages if not admin
    if 'userid' not in session or session['userid'] != 1891:
        flash('Permission denied!', 'danger')
        return redirect('/')

    return render_template('admin/orders.html')

if __name__ == "__main__":
	app.run(debug = True)
>>>>>>> cho
