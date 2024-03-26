import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGO_URL = os.environ.get('MONGODB_URL')
DB_NAME = os.environ.get('DB_NAME')

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/bucket', methods=['POST'])
def bucket_post():
    bucket_res = request.form['bucket_req']
    count = db.bucket.count_documents({})
    num = count + 1
    
    data = {
        'num': num,
        'bucket': bucket_res,
        'done': 0
    }
    
    db.bucket.insert_one(data)
    return ({'msg': 'Bucket saved!'})

@app.route('/bucket/done', methods=['POST'])
def bucket_done():
    num_req = request.form['num_req']
    db.bucket.update_one(
        {'num': int(num_req)},
        {'$set': {'done': 1}}
    )
    return ({'msg': 'Update done!'})

@app.route('/bucket', methods=['GET'])
def bucket_get():
    bucket_list = list(db.bucket.find({}, {'_id': False}))
    return jsonify({'data': bucket_list})

@app.route('/bucket/delete', methods=['DELETE'])
def bucket_delete():
    num_req = request.form['num_req']
    db.bucket.delete_one({'num': int(num_req)})
    return ({'msg': 'Deleted!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=3000, debug=True)