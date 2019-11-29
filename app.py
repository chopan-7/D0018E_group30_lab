#-*- coding: -utf-8 -*-
# installed libs
from flask import *
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

# created libs
from forms import *
from SQLfunctions import *
import datetime


app = Flask(__name__)

app.config['SECRET_KEY'] = 'bdb878ef8ea259ef877a3686726cf4f9'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Choss!95'
app.config['MYSQL_DB'] = 'webshop'

mysql = MySQL(app)


#TODO: Kontroll om användaren redan finns i databasen.
## REGISTER PAGE ##
@app.route("/register", methods=['GET', 'POST'])
def register():  
    form = RegistrationForm()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        profile_pic = 'default.jpg'
        hashed_password = generate_password_hash(form.password.data)
        cur.execute('INSERT INTO customers (firstname,lastname,email, password, address, postcode, country, phoneno, profilepic)'
                    ' VALUE(%s,%s,%s,%s,%s,%s,%s, %s, %s)',(form.first_name.data, form.last_name.data, form.email.data,
                                                        hashed_password, form.home_address.data,form.post_code.data,
                                                        form.country.data, form.phone_number.data, profile_pic))
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
                session['username'] = data[0][1]

                flash('You Are Now Logged In!', 'success')
                return redirect('/')
            else:
                flash('Invalid Email Or Password', 'danger')
        else:
            flash('Invalid Email Or Password', 'danger')
    return render_template('login.html', form=form)

@app.route("/customerMypage")
def customerMypage():

    return render_template('customerMypage.html')

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

    ## GET REVIEWS ##
    attr = 'customers.firstname, reviews.date, reviews.text'
    join = 'customers ON reviews.custID = customers.custID'
    cond = 'reviews.prodID=%s' %(item[0])
    rev = innerJoin('reviews', attr, join, cond)

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
        return redirect('/product?id=%s' %item[0])
    return render_template('productpage.html', item = item, form=form, rev=rev)


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
    return redirect('/product?id='+prodID)


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
    cond = 'cart.custID ='+str(session['userid'])
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


# länk för att cleara session
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

#ADMIN - EDIT PRODUCT PAGE#
@app.route('/admin/product/edit', methods=['GET', 'POST'])
def admin_products_edit():
    # denies access to admin pages if not admin
    if 'userid' not in session or session['userid'] != 1891:
        flash('Permission denied!', 'danger')
        return redirect('/')
    
    # define page
    page = 'edit'

    # initalize edit form
    editform = adminProdEdit()

    res = getRow('products', 'prodID ='+request.args.get('id'))

    # update the product
    if request.method == 'POST':
        name = str(editform.name.data)
        desc = str(editform.desc.data) if str(editform.desc.data) != "" else str(res[2])
        price = str(editform.price.data)
        img = str(editform.img.data) if str(editform.img.data) != "" else str(res[4])
        stock = str(editform.stock.data)
        cat = str(editform.cat.data)
        disc = str(editform.discount.data)
        update = 'a.name="%s", a.desc="%s", a.price=%s, a.img="%s", a.stock=%s, a.category="%s", a.discount=%s' %(name, desc, price, img, stock, cat, disc)
        cond = 'prodID = %s' %(str(request.form.get('prodID')))
        updateAll('products as a', update, cond)
        flash('Update sucessfull!', 'success')
        return redirect('/admin/product/edit?id='+str(res[0]))
    return render_template('admin/products.html', p=page, form=editform, item=res)

## ADMIN - ADD PRODUCT PAGE ##
@app.route('/admin/product/add', methods=['GET', 'POST'])
def admin_products_add():
    # denies access to admin pages if not admin
    if 'userid' not in session or session['userid'] != 1891:
        flash('Permission denied!', 'danger')
        return redirect('/')
    
    # define page
    page = 'add'

    # initialize add-form (same as edit-form)
    addform = adminProdEdit()

    # add the product
    if request.method == 'POST':
        # from data
        name = str(addform.name.data)
        desc = addform.desc.data
        price = str(addform.price.data) if str(addform.price.data) != "" else '0'
        img = str(addform.img.data) if str(addform.img.data) !="" else 'noimg.jpg'
        stock = str(addform.stock.data) if str(addform.stock.data) != "" else '0'
        cat = str(addform.cat.data) if str(addform.cat.data) != "" else ''
        
        # product table attributes and values
        attr = '`name`, `price`, `stock`, `img`, `category`, `desc`, `discount`'
        val = '"%s", %s, %s, "%s", %s, "%s", 0' %(name, price, stock, img, cat, desc)
        res = insertTo('products', attr, val)

        # flash success to user
        flash('The product has been added!', 'success')
        return redirect(url_for('admin_products'))
    
    return render_template('admin/products.html', p=page, form=addform)

## ADMIN - DELETE PRODUCT FUNCTION ##
@app.route('/admin/product/delete')
def admin_products_delete():
    # denies access to admin pages if not admin
    if 'userid' not in session or session['userid'] != 1891:
        flash('Permission denied!', 'danger')
        return redirect('/')
    
    # delete the product and flash the user on success
    removeProd = request.args.get('id')
    deleteFrom('products', 'prodID='+removeProd)
    flash('Item# '+removeProd+' has been successfully removed!', 'success')
    return redirect(url_for('admin_products'))

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
