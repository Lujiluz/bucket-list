from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.gowux15.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client.dbsparta

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
    app.run('0.0.0.0', port=5000, debug=True)