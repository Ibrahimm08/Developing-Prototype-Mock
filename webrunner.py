from flask import Flask, request, render_template, jsonify, redirect, session
import mysql.connector
import sqlite3

app = Flask(__name__)
app.secret_key = "asdfawf"

db = "database.db"

try: 
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor() 
    cursor.close()
    conn.close()
except mysql.connector.Error as err:
    print("Error:", err)

@app.route("/") 
    
@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    # Get ID from cookie
    ingredientID = session.get("ing", {})
    equipmentID = session.get("equ", {})
    
    equipment = ""
    ingredient = ""
    
    # Get the name attribute from id to show in front end 
    if equipmentID:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        
        # Use ? placeholder and values to avoid SQL injection
        sql = """ 
            SELECT EquipmentName FROM EQUIPMENT WHERE EquipmentID = ?
        """
        values = equipmentID
        
        equipment = cursor.execute(sql, values).fetchone()[0]
                
        conn.commit()
        cursor.close()
        conn.close()
    
    if ingredientID:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        
        sql = """ 
            SELECT Name FROM INGREDIENTS WHERE IngredientID = ?
        """
        values = ingredientID
        
        ingredient = cursor.execute(sql, values).fetchone()[0]
             
        conn.commit()
        cursor.close()
        conn.close()
        
    # On button click to new form or submit 
    if request.method == 'POST':
        # Save entered values
        session["recipeSession"] = request.form.to_dict()

        # Check if we clicked a multi form button then move to that form 
        if request.form.get("addIngredient") == "addIng":
            return redirect("addIngredient")
        elif request.form.get("addEquipment") == "addEqu":
            return redirect("addEquipment")
        
        # Else get all the values from form
        title = request.form['title']
        created_by = request.form['createdBy']
        description = request.form['description']
        prep_time = request.form['preparationTime']
        cook_time = request.form['cookingTime']
        servings = request.form['servings']
        instructions = request.form['instructions']
        
        
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        # No need for insert ID as schema has AUTOINCREMENT
        sql = """
            INSERT INTO Recipes 
            (Title, Created_By, Description, PreparationTime, CookingTime, Servings, Instructions, EquipmentID, IngredientID)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        values = (title, created_by, description, prep_time, cook_time, servings, instructions, equipmentID, ingredientID)

        # Excecute query and insert values into db
        cursor.execute(sql, values)
        conn.commit()

        cursor.close()
        conn.close()
    
    # If user moves or refreshes page we can recover the entry fields
    saved = session.get("recipeSession", {})
    print(saved)

    # Load this page and assign these values to be used in HTML through jininja
    return render_template('index.html', saved=saved, ingredient=ingredient, equipment=equipment ) 


@app.route("/addEquipment", methods=['GET', 'POST'])
def get_equipment():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    # Return all rows
    equipment =  cursor.execute("SELECT * FROM EQUIPMENT").fetchall()
    
    # Debuging purposes
    for row in equipment:
        print(row)
    cursor.close()
    conn.close()
    # Get the ID from selected option and store in cookie
    if request.method == 'POST':
        session["equ"] = request.form["option"]
        print(request.form["option"])
        return redirect("add_recipe")
    
    # Send equipment to front end for dropdown
    return render_template("addEquipment.html", equipment = equipment)


# Same as addEquipment but for ingredients
@app.route("/addIngredient", methods=['GET', 'POST'])
def get_ingredient():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    ingredients =  cursor.execute("SELECT * FROM INGREDIENTS").fetchall()
    for row in ingredients:
        print(row)
    cursor.close()
    conn.close()
    
    if request.method == 'POST':
        session["ing"] = request.form["option"]
        print(request.form["option"])
        return redirect("add_recipe")
    return render_template("addIngredient.html", ingredients = ingredients)
   



if __name__ == '__main__':
    app.run(debug=True)
