# Craete an empty server
# then run while debug is true:
from flask import *
import pymysql

def db_connection():
    return pymysql.connect(host='localhost',user='root',password='',database='clesaa_electronics')
# start
app = Flask(__name__);

app.secret_key="ghdhsfkjahdfgjl jhfbg "

@app. route('/')
def home():
    # create db connection
    connection =db_connection()
    # structure a query tha will fetch
    sql="SELECT * FROM products WHERE product_category ='Netwoking' "
        # create a cursor
    cursor=connection.cursor()
    # execute the sql using cursor
    cursor.execute(sql)
    # fetch all the entries in the category electronics and put them in a variable
    Networking=cursor.fetchall()
    
    
    sql2="SELECT * FROM products WHERE product_category ='Satelitte' "
        # create a cursor
    cursor2=connection.cursor()
    # execute the sql using cursor
    cursor2.execute(sql2)
    # fetch all the entries in the category electronics and put them in a variable
    Satelite=cursor2.fetchall()



    sql3="SELECT * FROM products WHERE product_category ='Tv_Accessories' "
        # create a cursor
    cursor3=connection.cursor()
    # execute the sql using cursor
    cursor3.execute(sql3)
    # fetch all the entries in the category electronics and put them in a variable
    Tv_Accessories=cursor3.fetchall()


   

   


    return render_template('home.html',Networking=Networking,Satelite=Satelite,Tv_Accessories=Tv_Accessories)

# create a route:
# login
# register
@app. route('/login', methods =['POST', 'GET'])
def login():
    if request.method=='POST':
        email =request.form['email']
        password =request.form['password']
        
        connection = db_connection()
        cursor =connection.cursor()

        sql ="select * from users where email=%s and password=%s"
        data=(email,password)
        cursor.execute(sql,data)

        # check the user
        count=cursor.rowcount
        if count==0:
            return render_template('login.html', message1='Invalid Credentials')
       

        else:
            user = cursor.fetchone()
            session['key']=user[1]
            return redirect('/')
    else:
        return render_template('login.html',message2='Login Here')
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

    

 
@app.route('/register', methods=['POST', 'GET'])
def register():
    # Step1:Check whether its POST or GET
    if request.method=='POST':
        # step2: request data
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        confirm = request.form['confirm']

        # Database connection
        connection =db_connection()
        # cursor():give connection ability to run sql
        cursor = connection.cursor()
        sql = "insert into users(username,email,phone,password) values(%s, %s, %s, %s)"

        data = (username,email,phone,password)
        # password checks
        if password != confirm:
            return render_template('register.html', message='password dont match!')
        elif len(password)<8:
            return render_template('register.html', message='password less than 8 characters!')
        else:
            cursor.execute(sql,data)
            connection.commit()
            return render_template('register.html', success ='Register successfull')
    else:
        return render_template('login.html', message= 'Login Here')


# 4.Product upload
    
@app.route( '/upload', methods =['POST', 'GET'])
def upload():
    if request.method=='POST':
        # capture data from the form
        product_name=request.form['product_name']
        product_desc=request.form['product_desc']
        product_cost=request.form['product_cost']
        product_category=request.form['product_category']
        # files in your computer
        product_image1 =request.files['product_image1']
        product_image2 =request.files['product_image2']
        

        

        # SAVE THE 3 IMAGES IN YOUR APPLICATION
        # Static/images/
        product_image1.save('static/images/'+ product_image1.filename)
        product_image2.save('static/images/'+ product_image2.filename)
       
    
        
# database connection()
        connection = db_connection()
        cursor =connection.cursor()

        sql ="INSERT INTO `products`(`product_name`, `product_desc`, `product_cost`, `product_category`, `product_image1`, `product_image2`) VALUES (%s,%s,%s,%s,%s,%s)"
        data =(product_name, product_desc, product_cost, product_category,product_image1.filename, product_image2.filename,)

        cursor.execute(sql,data)
        connection.commit()
        cursor.close()
        connection.close()
        return render_template('upload.html',message1 = 'product added successfully')
  
    else:
        return render_template('upload.html',message2='please add the product')
    # single page
@app.route('/single/<product_id>')
def single(product_id):
    connection=db_connection()
    cursor_single=connection.cursor()

    sql ="select * from products where product_id = %s"
    cursor_single.execute(sql,product_id)
    single_record=cursor_single.fetchone()
    return render_template('single.html',single_record=single_record)
# Displaying all category from one category
# 1.networking
@app.route('/networking')
def networking():
    connection=db_connection()
    cursor_networking = connection.cursor()

    sql_networking="select * from products where product_category='networking' order by rand() limit 4"
    cursor_networking.execute(sql_networking)
    networking=cursor_networking.fetchall()
    return render_template('networking.html', networking=networking)

# 2.satelite
@app.route('/satelite')
def satelite():
    connection=db_connection()
    cursor_satelite = connection.cursor()

    sql_satelite="select * from products where product_category='satelite' order by rand() limit 4"
    cursor_satelite.execute(sql_satelite)
    satelite=cursor_satelite.fetchall()
    return render_template('satelite.html',satelite=satelite)


# 3.tv_accessories
@app.route('/tv_accessories')
def tv_accessories():
    connection=db_connection()
    cursor_tv_accessories = connection.cursor()

    sql_tv_accessories="select * from products where product_category='tv_accessories' order by rand() limit 4"
    cursor_tv_accessories.execute(sql_tv_accessories)
    tv_accessories=cursor_tv_accessories.fetchall()
    return render_template('tv_accessories.html',tv_accessories=tv_accessories)



@app.route('/mpesa', methods=['POST', 'GET'])
def payment():
    phone = request.form['phone']
    amount = request.form['amount']

    from mpesa import stk_push
    stk_push(phone,amount)

    return "Please Check Your Phone to complete Payment"
@app.route('/send_reviews', methods =['POST', 'GET'])
def send_reviews():
    connection = db_connection()
    cursor_reviews = connection.cursor()
    # request data
    message = request.form['message']
    name =request.form['name']
    email =request.form['email']

    sql = "insert into reviews(review_message, client_name, client_email)  values (%s, %s, %s)"
   
    data = (message, name, email)

    cursor_reviews.execute(sql,data)
    connection.commit()
    return render_template('reviews.html', message='Review Send')





@app.route('/customercare')
def customercare():
    return render_template('customercare.html')










app. run(debug=True)
# stop