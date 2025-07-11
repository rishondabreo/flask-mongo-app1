from flask import Flask, render_template, request, redirect, url_for, jsonify
import pymongo
import json

app = Flask(__name__)

# ✅ Correct MongoDB URI here
MONGO_URI = "mongodb+srv://rishondeabreo:1234@cluster1.x1noseq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"
client = pymongo.MongoClient(MONGO_URI)
db = client["flask_db"]
collection = db["submissions"]

@app.route('/api')
def api():
    with open('data.json', 'r') as f:
        data = json.load(f)
    return jsonify(data)

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

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
