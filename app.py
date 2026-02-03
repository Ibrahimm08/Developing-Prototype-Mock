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
def index():
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
            placeholders = ",".join(["%s"] * len(selected_brands))
            conditions.append(f"BrandID IN ({placeholders})")
            params.extend(selected_brands)

        # Min price
        if min_price:
            conditions.append("price >= %s")
            params.append(min_price)

        # Max price
        if max_price:
            conditions.append("price <= %s")
            params.append(max_price)

        if search:
            conditions.append("LOWER(Name) LIKE LOWER(%s)")
            params.append(search)
            
        # Combine conditions
        # If no conditions do 1=1 which returns everything
        where_clause = " AND ".join(conditions) if conditions else "1=1"

        query = f"SELECT * FROM Product WHERE {where_clause};"

        cursor.execute(query, params)
        products = cursor.fetchall()
            
        DisconnectDB()
        
        
        
    return render_template("products.html", products = products)




if __name__ == '__main__':
    app.run(debug=True)
