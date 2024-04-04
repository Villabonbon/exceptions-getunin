import pymongo
from bson import ObjectId, json_util
from datetime import datetime
from flask import Flask, request, jsonify 
from flask.json import JSONEncoder


app = Flask(__name__)
client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["exceptions_db"]
collection = database["exceptions"]

class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, (ObjectId, datetime)):
            return str(o)
        return super().default(o)

app.json_encoder = CustomJSONEncoder

def insert_exception(user_id, name):
    exception = {
        "exception_id": ObjectId(),
        "user_id": user_id,
        "name": name,
        "creation_date": datetime.now()
    }
    result = collection.insert_one(exception)
    print(f"Excepción insertada con ID: {result.inserted_id}")

def get_all_exceptions():
    exceptions = collection.find()
    return list(exceptions)

@app.route('/exceptions/list', methods=['GET'])
def get_all_exceptions_route():
    exceptions = get_all_exceptions()
    formatted_exceptions = json_util.dumps(exceptions, default=str)
    return jsonify({"exceptions": formatted_exceptions})


@app.route('/exceptions/create', methods=['POST'])
def create_exception_route():
    data = request.get_json()
    user_id = data.get('user_id')
    name = data.get('name')

    insert_exception(user_id, name)
    return jsonify({'message': 'Exception created successfully'})

# Otras rutas para actualizar y eliminar excepciones

if __name__ == '__main__':
    app.run(debug=True)