from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb+srv://swadha1111:Swadha%402801@cluster0.cf1vhz3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["webhookDB"]
collection = db["events"]

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True)  # force=True makes sure JSON is parsed
        if data:
            collection.insert_one(data)
            return jsonify({"message": "Webhook received"}), 200
        else:
            return jsonify({"error": "No JSON received"}), 400
    except Exception as e:
        print("Webhook error:", e)
        return jsonify({"error": str(e)}), 403  # this is where you're getting stuck

@app.route('/logs', methods=['GET'])
def logs():
    logs = list(collection.find({}, {"_id": 0}))
    return jsonify({"logs": logs})

if __name__ == '__main__':
    app.run(debug=True)
