from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, Friend!'


@app.route('/api/uploader', methods=['POST'])
def uploader():
    agg = request.form['aggregation']
    print(agg)
    data = request.files['data'].read().decode('utf-8')
    print(len(data))
    return ''
