from flask import Flask, request, render_template, redirect, session
import mysql.connector
import sqlite3
import bcrypt

app = Flask(__name__)
# As prototype is not public a weak key is fine 
# Secret key is required when using sessions
app.secret_key = "SecretKey"  

# Our db filename
DB = "database.db"

# Connect to database
def ConnectToDB():
    global conn, cursor
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    
# Severe the Connection 
def DisconnectDB():
    cursor.close()
    conn.close()


# Check if we can connect to the database
try: 
    ConnectToDB()
    DisconnectDB()
except mysql.connector.Error as err:
    print("Error:", err)





    
@app.route("/")

@app.route("/index")
def Index():
    return render_template("index.html")



@app.route("/filter_products", methods=["GET", "POST"])
def Products(): 
    ConnectToDB()
    
    # Get all rows in Product to send to html to display
    products = cursor.execute("SELECT * FROM Product").fetchall()
    
    DisconnectDB()
    
    
    # For Debugging to see what is stored in products variable
    for row in products:
        print(row)
    
    if request.method == "GET":
        # Get value from form
        max_price = request.form.get["max-price"]
        min_price = request.form.get["min-price"]
        search = request.form.get["search"]
        
        # Brand checked for filtering
        selected_brands = request.form.getlist["brand"]
        
        conditions = []
        params = []

        ConnectToDB()

        # Brand filter
        if selected_brands:
            placeholders = ",".join(["?"] * len(selected_brands))
            conditions.append(f"BrandID IN ({placeholders})")
            params.extend(selected_brands)

        # Min price
        if min_price:
            conditions.append("price >= ?")
            params.append(min_price)

        # Max price
        if max_price:
            conditions.append("price <= ?")
            params.append(max_price)

        if search:
            conditions.append("LOWER(Name) LIKE LOWER(?)")
            params.append(search)
            
        # Combine conditions
        # If no conditions do 1=1 which returns everything
        where_clause = " AND ".join(conditions) if conditions else "1=1"

        query = f"SELECT * FROM Product WHERE {where_clause};"

        cursor.execute(query, params)
        products = cursor.fetchall()
            
        DisconnectDB()
        
        
    return render_template("products.html", products = products)

@app.route("/booking", methods=["GET", "POST"])
def Booking():
    return render_template("booking.html")

@app.route("/dashboard", methods=["GET", "POST"])
def Dashboard():
    return render_template("dashboard.html")

@app.route("/create", methods=["GET", "POST"])
def Sign_Up():
    if request.method == "POST":
        # Get form values
        firstname = request.form.get("firstname")
        surname = request.form.get("surname")
        
        email = request.form.get("email")
        # Hash password
        password = (request.form.get("password")).encode("utf-8")
        
        ConnectToDB()
        
        # Check if email does not already exist
        query = "Select * From Account Where LOWER(Email) = LOWER(?)"
        if cursor.execute(query, (email,)).fetchone():
            print("Email already in use")
        else:
            query = """
            INSERT INTO Account 
            (Firstname, Surname, Email, Password)
            VALUES (?, ?, ?, ?)
            """

            values = (firstname, surname, email, password)    

            cursor.execute(query, values)
            
            redirect("/login")
            
    return render_template("create.html")
    

@app.route("/login", methods=["GET", "POST"])
def Login():
    if request.method == "POST":
        
        username = request.form.get("username")
        password = request.form.get("password")
        
        ConnectToDB()
        
        # Check if Username exist
        query = "Select * From Account WHERE LOWER(Email) = LOWER(?)"
        user = cursor.execute(query, (username,)).fetchone()
        
        if user:
            stored_pass = user["Password"]
            
            #Compare hashed passwords
            if bcrypt.checkpw(password.encode("utf-8"), stored_pass):
                session["user"] = user["ID"]
                return redirect("/dashboard")
            # Check if bcrypted password match db password
            
        else:
            print("Username or Password is incorrect")
            
        
    return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True)
