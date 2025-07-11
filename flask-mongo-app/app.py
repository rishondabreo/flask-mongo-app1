from flask import Flask, render_template, request, redirect, url_for, jsonify
import pymongo
import json

app = Flask(__name__)

# ✅ MongoDB Atlas connection
MONGO_URI = "mongodb+srv://rishondeabreo:1234@cluster1.x1noseq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"
client = pymongo.MongoClient(MONGO_URI)
db = client["flask_db"]
collection = db["submissions"]          # for user info
todo_collection = db["todos"]           # separate collection for todo items

# 📄 API to serve JSON data
@app.route('/api')
def api():
    with open('data.json', 'r') as f:
        data = json.load(f)
    return jsonify(data)

# 🧾 User Info Form Route
@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            collection.insert_one({'name': name, 'email': email})
            return redirect(url_for('success'))
        except Exception as e:
            return render_template('form.html', error=str(e))
    return render_template('form.html')

# ✅ To-Do Submission Route
@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    try:
        item_name = request.form.get('itemName')
        item_desc = request.form.get('itemDescription')
        item_id = request.form.get('itemID') or None
        item_uuid = request.form.get('itemUUID') or None
        item_hash = request.form.get('itemHash') or None

        todo_data = {
            'itemName': item_name,
            'itemDescription': item_desc,
            'itemID': item_id,
            'itemUUID': item_uuid,
            'itemHash': item_hash
        }

        # remove None values
        todo_data = {k: v for k, v in todo_data.items() if v}

        todo_collection.insert_one(todo_data)
        return redirect(url_for('success'))
    except Exception as e:
        return render_template('form.html', error=f"To-Do Submit Error: {e}")

# ✅ Success Page
@app.route('/success')
def success():
    return render_template('success.html')

# 🏁 App Runner
if __name__ == '__main__':
    app.run(debug=True)
